"""Chronological session history and property-scoped restoration.

Snapshots are used to calculate immutable changes at user-event boundaries;
replay merges only those changes into the current state, never an old session.
"""
import copy
import os
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from .RoutingHistory import RoutingHistory


def differences(before, after, path=()):
    if before == after:
        return []
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in before.keys() | after.keys():
            if key not in before or key not in after:
                result.append((path + (key,), key in before, copy.deepcopy(before.get(key)),
                               key in after, copy.deepcopy(after.get(key))))
            else:
                result.extend(differences(before[key], after[key], path + (key,)))
        return result
    # Curve point arrays are one property. Other fixed-size sequences (slider
    # value/mode/mappings, range ends, effect parameters) have independent fields.
    if (isinstance(before, list) and isinstance(after, list) and len(before) == len(after)
            and 'userGraph' not in path):
        return [change for i, (a, b) in enumerate(zip(before, after))
                for change in differences(a, b, path + (i,))]
    return [(path, True, copy.deepcopy(before), True, copy.deepcopy(after))]


def merge_changes(document, changes, redo):
    result = copy.deepcopy(document)
    for path, old_exists, old, new_exists, new in changes:
        parent = result
        for key in path[:-1]:
            parent = parent[key]
        exists, value = (new_exists, new) if redo else (old_exists, old)
        if exists:
            parent[path[-1]] = copy.deepcopy(value)
        else:
            parent.pop(path[-1], None)
    return result


@dataclass
class Action:
    label: str
    before: dict
    after: dict
    changes: tuple = ()
    target: dict = None
    stop: bool = True

    def __iter__(self):
        return iter((self.label, self.before, self.after))

    def __getitem__(self, index):
        return (self.label, self.before, self.after)[index]


class SessionHistory(RoutingHistory):
    def __init__(self, session, limit=100):
        super().__init__(session, limit)
        self.active = None
        self.suspended = 0
        self.deferred = []
        self.take = None
        self.burst_timer = None
        self.burst_target = None

    @contextmanager
    def suspend(self):
        self.suspended += 1
        try:
            yield
        finally:
            self.suspended -= 1

    def effect_ids(self):
        from . import CeciliaLib as lib
        result = []
        for plugin in lib.getVar('plugins'):
            if plugin is None:
                result.append(None)
                continue
            if not hasattr(plugin, '_history_id'):
                plugin._history_id = uuid.uuid4().hex
            result.append(plugin._history_id)
        return result

    def snapshot(self):
        result = super().snapshot()
        result['effect_ids'] = self.effect_ids()
        return result

    def document(self):
        from . import CeciliaLib as lib
        raw = lib.captureSession()
        modules = {}
        for item, module in zip(raw['modules'], self.session.modules):
            modes = {slider.getName(): bool(slider.getRec()) for slider in module.state['userSliders']}
            for widget in module.inputs.cfileinList:
                if widget.name in item['settings']['userInputs'] and hasattr(widget, 'getSamplerInfo'):
                    item['settings']['userInputs'][widget.name]['xfadeshape'] = widget.samplerFrame.getXfadeShape()
            modules[module.id] = dict(settings=item['settings'], preset=item['preset'], recording=modes)
        output = raw['output']
        ids = self.effect_ids()
        output['effects'] = {ident: output['plugins'][str(i)] for i, ident in enumerate(ids) if ident}
        output['effect_order'] = ids
        del output['plugins']
        # Slot-derived graph names become stable effect/knob identities in history.
        curves = {}
        for i, plugin in enumerate(lib.getVar('plugins')):
            if plugin is not None:
                for k, knob in enumerate(plugin.getKnobs()):
                    key = knob.getName()
                    if key in output['userGraph']:
                        curves[ids[i] + ':' + str(k)] = output['userGraph'].pop(key)
        output['effect_curves'] = curves
        return dict(modules=modules, output=output)

    def ready(self):
        from . import CeciliaLib as lib
        frame = lib.getVar('interface')
        return (not self.replaying and not self.suspended
                and frame is not None and hasattr(frame, 'controlPanel')
                and lib.getVar('gainSlider') is not None
                and all(m.editor and m.inputs and m.state['presetPanel'] for m in self.session.modules))

    def begin(self, label, target=None):
        if not self.ready() or self.active is not None:
            return None
        self.active = dict(label=label, before=self.document(), target=target or {},
                           modules=list(self.session.modules), gesture=None)
        return self.active

    def flush(self):
        # Queued deliveries are idempotent, so their later wx delivery is harmless.
        while self.deferred:
            pending, self.deferred = self.deferred, []
            for callback in pending:
                callback()

    def finish(self, token, success=True):
        if token is None or self.active is not token:
            return
        try:
            self.flush()
            if success:
                self.record_edit(token['label'], token['before'], self.document(), token['target'], token['modules'])
        finally:
            self.active = None
            self.burst_target = None
            self.update_menu()

    @contextmanager
    def transaction(self, label, target=None):
        token = self.begin(label, target)
        try:
            yield
        except Exception:
            self.finish(token, False)
            raise
        else:
            self.finish(token)

    def append(self, action):
        self.undo_stack.append(action)
        self.undo_stack[:] = self.undo_stack[-self.limit:]
        self.redo_stack.clear()
        self.collect()
        self.update_menu()

    def record(self, label, before):
        if self.replaying:
            return
        after = self.snapshot()
        if before['modules'] == after['modules'] and before['routing'] == after['routing']:
            return
        target = {'view': 'graph' if label.startswith('Replace ') else 'chain'}
        changed = [m for m in after['modules'] if m not in before['modules']] or [m for m in before['modules'] if m not in after['modules']]
        if changed:
            target['node'] = changed[0].id
        else:
            for key in ('connections', 'output_connections'):
                old, new = before['routing'][key], after['routing'][key]
                delta = [item for item in new if item not in old] or [item for item in old if item not in new]
                if delta:
                    edge = tuple(delta[0]) if key == 'connections' else (delta[0], None)
                    target.update(edge=edge, node=edge[0])
                    break
            old_muted = set(before['routing'].get('muted_ids', []))
            new_muted = set(after['routing'].get('muted_ids', []))
            if old_muted != new_muted:
                target['node'] = next(iter(old_muted ^ new_muted))
            positions = after['routing']['positions']
            for node, point in positions.items():
                if before['routing']['positions'].get(node) != point:
                    target['node'] = node
                    break
        target.setdefault('node', after['selected'] or before['selected'])
        live_routing = (before['modules'] == after['modules'] and
                     {k: v for k, v in before['routing'].items() if k not in ('muted_ids', 'positions')} ==
                     {k: v for k, v in after['routing'].items() if k not in ('muted_ids', 'positions')})
        self.append(Action(label, before, after, target=target, stop=not live_routing))

    def record_edit(self, label, before, after, target=None, modules=None):
        changes = tuple(differences(before, after))
        if not changes:
            return
        refs = dict(modules=list(modules or self.session.modules))
        target = self.destination(changes, target or {})
        if label.startswith('Edit ') or label == 'Change value':
            if target.get('curve'):
                label = 'Edit curve ' + target['curve']
            elif target.get('control') or target.get('widget'):
                label = 'Change ' + target.get('control', target.get('widget', 'control'))
            elif target.get('input'):
                label = 'Change input ' + target['input']
            elif target.get('effect'):
                label = 'Change effect'
            elif target.get('output'):
                label = 'Change ' + {'totalTime': 'duration', 'gainSlider': 'gain'}.get(target['output'], target['output'])
        self.append(Action(label, refs, refs.copy(), changes, target, not self.live_safe(changes)))

    def finish_take(self):
        if self.take is None:
            return
        before, self.take = self.take, None
        after = self.document()
        def recorded(path):
            if path[:2] == ('output', 'effect_curves'):
                return True
            if len(path) > 2 and path[0] == 'modules' and path[2] == 'recording':
                return True
            if len(path) > 3 and path[0] == 'modules' and path[2:4] == ('settings', 'userGraph'):
                return True
            if len(path) > 5 and path[0] == 'modules' and path[2:4] == ('settings', 'userSliders') and path[5] == 1:
                return True
            if len(path) > 6 and path[0] == 'modules' and path[2:4] == ('settings', 'userInputs') and path[5] in ('loopIn', 'loopOut', 'loopX', 'gain', 'transp') and path[6] in (1, 2):
                return True
            return len(path) > 5 and path[:2] == ('output', 'effects') and path[3] == 2 and path[5] == 1
        changes = tuple(change for change in differences(before, after) if recorded(change[0]))
        if changes:
            refs = dict(modules=list(self.session.modules))
            target = self.destination(changes, {})
            self.append(Action('Record automation', refs, refs.copy(), changes, target, True))

    def destination(self, changes, target):
        target = target.copy()
        if target.get('operation') == 'preset':
            return dict(target, view='graph')
        # File selection may be nested inside a popup's gesture transaction.
        # Its dependent sampler changes must not turn navigation into a sampler edit.
        for path, *_ in changes:
            if (len(path) == 6 and path[0] == 'modules'
                    and path[2:4] == ('settings', 'userInputs') and path[5] == 'path'):
                return dict(target, module=path[1], input=path[4], sampler=False, view='graph')
        if target.get('operation') == 'soundfile':
            for path, *_ in changes:
                if len(path) > 4 and path[0] == 'modules' and path[2:4] == ('settings', 'userInputs'):
                    return dict(target, module=path[1], input=path[4], sampler=False, view='graph')
        for path, *_ in changes:
            if path[0] == 'modules':
                target.setdefault('module', path[1])
                if len(path) > 4 and path[2:4] == ('settings', 'userGraph'):
                    target.update(view='graph', curve=path[4])
                    break
                if len(path) > 4 and path[2:4] == ('settings', 'userSliders'):
                    target.setdefault('control', path[4])
                if len(path) > 4 and path[2:4] == ('settings', 'userInputs'):
                    target.setdefault('input', path[4])
                    if len(path) > 5:
                        target.setdefault('input_control', path[5])
                    target.setdefault('sampler', len(path) > 5 and path[5] not in ('path', 'mode', 'type'))
                if len(path) > 4 and path[2:4] == ('settings', 'userTogglePopups'):
                    target.setdefault('widget', path[4])
            elif path[:2] == ('output', 'effects') and len(path) > 2:
                target.setdefault('effect', path[2])
                if len(path) > 4 and path[3] == 1:
                    target.setdefault('knob', path[4])
            elif path[:2] == ('output', 'effect_curves') and len(path) > 2:
                ident, knob = path[2].rsplit(':', 1)
                target.update(effect=ident, knob=int(knob), view='graph', effect_curve=True)
            elif path[0] == 'output':
                target.setdefault('output', path[1])
        target.setdefault('view', 'graph')
        return target

    def live_safe(self, changes):
        from . import CeciliaLib as lib
        for path, *_ in changes:
            if path == ('output', 'gainSlider'):
                continue
            if path[:2] == ('output', 'effect_order'):
                # Reordering existing effects uses the engine's live move path.
                # Replacement also changes the effects dictionary and is unsafe.
                continue
            if len(path) >= 6 and path[0] == 'modules' and path[2:4] == ('settings', 'userSliders') and path[5] == 0:
                module = next((m for m in self.session.modules if m.id == path[1]), None)
                slider = next((s for s in module.state['userSliders'] if s.getName() == path[4]), None) if module else None
                if slider is not None and not slider.getUp():
                    continue
            if len(path) >= 5 and path[0] == 'modules' and path[2:4] == ('settings', 'userTogglePopups'):
                module = next((m for m in self.session.modules if m.id == path[1]), None)
                widget = next((w for w in module.state['userTogglePopups'] if w.getName() == path[4]), None) if module else None
                if widget is not None and getattr(widget, 'rate', None) == 'k':
                    continue
            if len(path) >= 5 and path[:2] == ('output', 'effects') and path[3] == 1 and path[4] < 3:
                continue
            if len(path) >= 6 and path[:2] == ('output', 'effects') and path[3] == 2 and path[5] == 0:
                continue
            return False
        return True

    def available(self):
        import wx
        from . import CeciliaLib as lib
        frame = lib.getVar('interface')
        return (frame is not None and not frame.grid.drag and self.active is None and not self.replaying
                and not any(isinstance(w, wx.Dialog) and w.IsModal() for w in wx.GetTopLevelWindows()))

    def clear(self):
        if self.burst_timer:
            self.burst_timer.Stop()
        if self.active:
            capture = self.active.get('capture')
            self.active = None
            if capture and capture.HasCapture():
                capture.ReleaseMouse()
        self.active = self.take = self.burst_target = None
        self.deferred.clear()
        super().clear()

    def apply(self, target):
        from . import CeciliaLib as lib
        current_routing = self.session.routing_snapshot()
        if (target['modules'] == self.session.modules and
                {k: v for k, v in current_routing.items() if k not in ('muted_ids', 'positions')} ==
                {k: v for k, v in target['routing'].items() if k not in ('muted_ids', 'positions')}):
            muted_ids = list(target['routing'].get('muted_ids', []))
            if self.session.muted_ids != muted_ids:
                self.session.muted_ids = muted_ids
                for module in self.session.modules:
                    lib.getVar('audioServer').setModuleMute(module.id, module.id in muted_ids)
            self.session.positions = copy.deepcopy(target['routing']['positions'])
            lib.getVar('interface').grid.rebuild()
            return
        for module in target['modules']:
            if module not in self.session.modules:
                for widget in module.inputs.cfileinList:
                    required = widget.name in module.auxiliary_inputs or (module.id in target['routing']['source_ids'] and widget.getMode() == 0)
                    if required and widget.filePath and not os.path.isfile(widget.filePath):
                        raise ValueError('Missing soundfile: ' + widget.filePath)
        super().apply(target)
        from . import CeciliaLib as lib
        for plugin, ident in zip(lib.getVar('plugins'), target.get('effect_ids', [])):
            if plugin is not None and ident:
                plugin._history_id = ident

    def preflight(self, document, changes):
        from . import CeciliaLib as lib
        for path, *_ in changes:
            if len(path) >= 5 and path[0] == 'modules' and path[2:4] == ('settings', 'userInputs'):
                info = document['modules'][path[1]]['settings']['userInputs'][path[4]]
                asset = info.get('path')
                if asset and not os.path.isfile(asset):
                    raise ValueError('Missing soundfile: ' + asset)
                if asset and not lib.getVar('audioServer').validateAudioFile(asset):
                    raise ValueError('Unreadable soundfile: ' + asset)

    def restore_document(self, document, changes):
        from . import CeciliaLib as lib
        from .Session import instance_context
        affected = {p[1] for p, *_ in changes if p[0] == 'modules'}
        for module in self.session.modules:
            if module.id not in affected:
                continue
            value = document['modules'][module.id]
            roots = {p[3] for p, *_ in changes if len(p) > 3 and p[:3] == ('modules', module.id, 'settings')}
            with instance_context(module):
                for root in roots:
                    data = value['settings'][root]
                    names = {p[4] for p, *_ in changes if len(p) > 4 and p[:4] == ('modules', module.id, 'settings', root)}
                    if root == 'userSliders':
                        for slider in module.state['userSliders']:
                            if not names or slider.getName() in names:
                                slider.setState(data[slider.getName()])
                                slider.writeToEntry(slider.getValue())
                    elif root == 'userTogglePopups':
                        for widget in module.state['userTogglePopups']:
                            if (not names or widget.getName() in names) and hasattr(widget, 'setValue'):
                                widget.setValue(data[widget.getName()], True)
                                if widget.type == 'toggle':
                                    widget.onToggle(widget.getValue())
                    elif root == 'userInputs':
                        for name in names or data.keys():
                            widget = module.inputs.getCfileinFromName(name)
                            info = copy.deepcopy(data[name])
                            if not info.get('path'):
                                widget.reset()
                            module.state['userInputs'][name] = info
                        lib.updateInputsFromDict()
                        for name in names or data.keys():
                            widget = module.inputs.getCfileinFromName(name)
                            if 'xfadeshape' in data[name]:
                                widget.samplerFrame.setXfadeShape(data[name]['xfadeshape'])
                            for key in ('loopX', 'loopIn', 'loopOut', 'gain', 'transp'):
                                value_list = data[name].get(key)
                                slider = getattr(widget.samplerFrame, key + 'Slider', None)
                                if slider and isinstance(value_list, list) and len(value_list) > 2:
                                    slider.setRec(value_list[2])
                    elif root == 'userGraph':
                        graph = module.editor.graph.plotter
                        for key in names or data.keys():
                            self.restore_curve(graph, key, data[key])
                        graph.draw()
                if any(p[:3] == ('modules', module.id, 'recording') for p, *_ in changes):
                    for slider in module.state['userSliders']:
                        slider.setRec(value['recording'][slider.getName()])
                if any(p == ('modules', module.id, 'preset') for p, *_ in changes):
                    module.editor.presets.setLabel(value['preset'])
        self.restore_output(document['output'], changes)

    @staticmethod
    def curve_key(line):
        name = line.getName()
        if line.slider is not None and line.slider.widget_type == 'range':
            return name + next(end for end in ('min', 'max') if line.getLabel().endswith(end))
        if line.slider is not None and line.slider.widget_type == 'splitter':
            return name + '_' + line.getLabel().rsplit(' ', 1)[-1]
        return name

    @classmethod
    def restore_curve(cls, graph, key, state):
        for line in graph.getData():
            if key == cls.curve_key(line):
                line.setLineState(state)
                return
        raise ValueError('Missing automation curve: ' + key)

    def restore_output(self, output, changes):
        from . import CeciliaLib as lib
        from .Session import instance_context
        panel = lib.getVar('interface').controlPanel
        keys = {p[1] for p, *_ in changes if p[0] == 'output'}
        if 'totalTime' in keys:
            panel.setTotalTime(output['totalTime'], True)
            panel.updateDurationSlider()
        if 'gainSlider' in keys:
            lib.getVar('gainSlider').SetValue(output['gainSlider'], propagate=False)
            panel.onChangeGain(output['gainSlider'])
        for key in keys & {'nchnls', 'audioFileType', 'sampSize', 'startOffset'}:
            lib.setVar(key, output[key])
        if keys & {'nchnls', 'audioFileType', 'sampSize'}:
            panel.updateNchnls()
        if 'output_path' in keys:
            panel.outputFilename = output['output_path']
            lib.setVar('outputFile', output['output_path'])
            panel.filenameLabel.setLabel(lib.shortenName(os.path.basename(output['output_path']), panel.charNumForLabel))
        if keys & {'effects', 'effect_order', 'effect_curves', 'userGraph'} and self.session.modules:
            with instance_context(self.session.modules[0]):
                if 'effect_order' in keys:
                    for i, ident in enumerate(output['effect_order']):
                        current = self.effect_ids()
                        if ident in current:
                            j = current.index(ident)
                            while j > i:
                                panel.movePlugin(j, -1)
                                j -= 1
                ids = self.effect_ids()
                affected = {p[2] for p, *_ in changes if len(p) > 2 and p[:2] == ('output', 'effects')}
                for i, ident in enumerate(output['effect_order']):
                    if ident is None:
                        if 'effect_order' in keys and lib.getVar('plugins')[i] is not None:
                            panel.replacePlugin(i, 'None')
                        continue
                    if 'effect_order' not in keys and ident not in affected:
                        continue
                    data = output['effects'][ident]
                    plugin = lib.getVar('plugins')[i]
                    if ids[i] != ident or plugin.getName() != data[0]:
                        panel.replacePlugin(i, data[0])
                        plugin = lib.getVar('plugins')[i]
                        plugin._history_id = ident
                    plugin.setParams(data[1])
                    plugin.setStates(data[2])
                    for k in range(3):
                        getattr(plugin, 'onChangeKnob' + str(k + 1))(data[1][k])
                    plugin.onChangePreset(data[1][3])
                graph = self.session.modules[0].editor.graph.plotter
                curve_keys = {p[2] for p, *_ in changes if len(p) > 2 and p[:2] == ('output', 'effect_curves')}
                for key, state in output.get('effect_curves', {}).items():
                    if 'effect_order' not in keys and key not in curve_keys:
                        continue
                    ident, knob = key.rsplit(':', 1)
                    ids = self.effect_ids()
                    if ident in ids:
                        plugin = lib.getVar('plugins')[ids.index(ident)]
                        self.restore_curve(graph, plugin.getKnobs()[int(knob)].getName(), state)
                for key, state in output.get('userGraph', {}).items():
                    self.restore_curve(graph, key, state)
                graph.draw()

    def step(self, redo=False):
        from . import CeciliaLib as lib
        if not self.available():
            return
        # A completed recording take is the next chronological action.
        if self.take is not None:
            lib.stopCeciliaSound()
        source, destination = (self.redo_stack, self.undo_stack) if redo else (self.undo_stack, self.redo_stack)
        if not source or not self.available():
            return
        action = source[-1]
        if action.stop and lib.getVar('audioServer').isAudioServerRunning():
            if lib.getVar('audioServer').timeOpened:
                lib.stopCeciliaSound()
            else:
                lib.getVar('audioServer').stop()
            return self.step(redo)
        self.replaying = True
        current = self.document() if action.changes else self.snapshot()
        try:
            if action.changes:
                target = merge_changes(current, action.changes, redo)
                self.preflight(target, action.changes)
                self.restore_document(target, action.changes)
            else:
                self.apply(action.after if redo else action.before)
        except Exception as error:
            try:
                if action.changes:
                    self.restore_document(current, action.changes)
                else:
                    self.apply(current)
            except Exception as rollback:
                lib.showErrorDialog('Could not restore session', str(error) + '\nRollback: ' + str(rollback))
            else:
                lib.showErrorDialog('Could not restore session', str(error))
        else:
            source.pop()
            destination.append(action)
            self.reveal(action, redo)
        finally:
            self.replaying = False
            self.collect()
            self.update_menu()

    def reveal(self, action, redo):
        import wx
        from . import CeciliaLib as lib, ChainUI
        frame = lib.getVar('interface')
        target = action.target or {}
        if not action.changes:
            state = action.after if redo else action.before
            module = next((m for m in self.session.modules if m.id == target.get('node')), self.session.selected)
            if module:
                ChainUI.select(frame, module, change_view=False, preserve_source=True)
            ChainUI.show_view(frame, target.get('view', 'chain'))
            window = frame.grid
            if target.get('view') == 'graph' and module:
                window = module.editor.sliders
        else:
            module = next((m for m in self.session.modules if m.id == target.get('module')), self.session.selected)
            if (target.get('effect') or 'effect_slot' in target) and self.session.modules:
                module = self.session.modules[0]
            if module:
                ChainUI.select(frame, module, change_view=False, preserve_source=not bool(target.get('input')))
            ChainUI.show_view(frame, 'graph')
            window = None
            if module and target.get('control'):
                slider = next((s for s in module.state['userSliders'] if s.getName() == target['control']), None)
                window = slider.slider if slider else None
            if module and target.get('curve'):
                graph = module.editor.graph.plotter
                for i, line in enumerate(graph.getData()):
                    if target['curve'] == self.curve_key(line):
                        line.setShow(True)
                        graph.setSelected(i)
                        module.editor.graph.toolbar.menu.setLabel(line.getLabel(), False)
                        break
                if graph._zoomed:
                    graph._zoomed = False
                    graph.last_draw = None
                graph.draw()
                window = graph.canvas
            if module and target.get('widget'):
                widget = next((w for w in module.state['userTogglePopups'] if w.getName() == target['widget']), None)
                if widget:
                    window = getattr(widget, 'popup', getattr(widget, 'toggle', getattr(widget, 'entry', None)))
            if module and target.get('input'):
                widget = module.inputs.getCfileinFromName(target['input'])
                if widget:
                    window = widget.fileMenu
                    if target.get('sampler') and widget.samplerFrame:
                        widget.samplerFrame.Show()
                        widget.samplerFrame.Raise()
                        window = getattr(widget.samplerFrame, {
                            'loopIn': 'loopInSlider', 'loopOut': 'loopOutSlider', 'loopX': 'loopXSlider',
                            'gain': 'gainSlider', 'transp': 'transpSlider'}.get(target.get('input_control'), ''), widget.samplerFrame)
                        window = getattr(window, 'slider', window)
            if target.get('effect') or 'effect_slot' in target:
                ids = self.effect_ids()
                ident = target.get('effect')
                slot = ids.index(ident) if ident in ids else target.get('effect_slot')
                if slot is not None and slot < len(ids):
                    plugin = lib.getVar('plugins')[slot] or frame.controlPanel.plugins[slot]
                    frame.controlPanel.onTogglePanels(1)
                    frame.controlPanel.sizerMain.Show(frame.controlPanel.pluginsPanel, True)
                    frame.controlPanel.Layout()
                    knob = plugin.getKnobs()[min(target.get('knob', 0), 2)]
                    window = plugin.choice if plugin.getName() == 'None' or target.get('operation') == 'effect_selection' else knob
                    if target.get('effect_curve'):
                        graph = module.editor.graph.plotter
                        for i, line in enumerate(graph.getData()):
                            if line.getName() == knob.getName():
                                graph.setSelected(i)
                                module.editor.graph.toolbar.menu.setLabel(line.getLabel(), False)
                                break
                        graph.draw()
                        window = graph.canvas
            if target.get('operation') == 'preset' and module:
                window = module.editor.presets.presetChoice
            if target.get('output'):
                window = {'totalTime': frame.controlPanel.durationSlider, 'gainSlider': lib.getVar('gainSlider'),
                          'output_path': frame.controlPanel.filenameLabel}.get(target['output'], window)
            if target.get('output') in ('audioFileType', 'sampSize'):
                main = lib.getVar('mainFrame')
                prefs = main.prefs
                if not prefs:
                    main.onPreferences(None)
                    prefs = main.prefs
                prefs.onPageChange(3)
                prefs.Show()
                prefs.Raise()
                prefs.choiceFileFormat.setStringSelection(lib.getVar('audioFileType'))
                from .constants import BIT_DEPTHS
                prefs.choiceBD.setStringSelection(next(k for k, v in BIT_DEPTHS.items() if v == lib.getVar('sampSize')))
                window = prefs.choiceFileFormat if target['output'] == 'audioFileType' else prefs.choiceBD
            if window is None:
                window = module.editor.sliders if module else frame.grid
        if isinstance(window, wx.Window) and window and not window.IsBeingDeleted():
            window.SetFocus()

    def update_menu(self):
        from . import CeciliaLib as lib
        from .constants import ID_UNDO, ID_REDO
        frame = lib.getVar('interface')
        if frame is None or not hasattr(frame, 'grid'):
            return
        for ident, verb, stack, shortcut in ((ID_UNDO, 'Undo', self.undo_stack, 'Ctrl+Z'),
                                             (ID_REDO, 'Redo', self.redo_stack, 'Shift+Ctrl+Z')):
            item = frame.menubar.FindItemById(ident)
            label = 'Record automation' if self.take is not None and ident == ID_UNDO else (stack[-1].label if stack else '')
            item.SetItemLabel(verb + (' ' + label if label else '') + '\t' + shortcut)
            item.Enable(bool(stack or (self.take is not None and ident == ID_UNDO)) and self.available() and not (self.take is not None and ident == ID_REDO))
