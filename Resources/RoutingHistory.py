"""Routing snapshots and parked-editor lifecycle used by session history."""


class RoutingHistory:
    def __init__(self, session, limit=100):
        self.session, self.limit = session, limit
        self.undo_stack, self.redo_stack = [], []
        self.retained = set()
        self.replaying = False

    def snapshot(self):
        from . import CeciliaLib as lib
        state = dict(modules=list(self.session.modules), routing=self.session.routing_snapshot(),
                     selected=self.session.selected_id)
        if lib.getVar('interface') is not None:
            output = lib.captureSession()['output']
            state['effects'] = {key: output[key] for key in ('plugins', 'userGraph')}
        return state

    def collect(self):
        needed = set(self.session.modules)
        for _, before, after in self.undo_stack + self.redo_stack:
            needed.update(before['modules'])
            needed.update(after['modules'])
        for module in self.retained - needed:
            if module.editor:
                module.editor.destroy()
        self.retained = needed - set(self.session.modules)

    def clear(self):
        from . import CeciliaLib as lib
        frame = lib.getVar('interface')
        if frame is not None and hasattr(frame, 'grid'):
            frame.grid.drag = frame.grid.move_before = None
            if frame.grid.HasCapture():
                frame.grid.ReleaseMouse()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.collect()
        self.update_menu()

    def park(self, module):
        self.retained.add(module)
        module.retired = True
        editor = module.editor
        for window in (editor.graph, editor.sliders, editor.toggles, editor.presets, module.inputs.inputPanel):
            sizer = window.GetContainingSizer()
            if sizer:
                sizer.Detach(window)
            window.Hide()
        for widget in module.inputs.cfileinList:
            if widget.samplerFrame:
                widget.samplerFrame.Hide()

    def apply(self, target):
        from . import CeciliaLib as lib, ChainUI
        from .Session import ChainSession, instance_context
        proposed = ChainSession()
        proposed.modules = list(target['modules'])
        proposed.restore_routing(target['routing'])
        proposed.validate_graph()
        session, frame = self.session, lib.getVar('interface')
        previous = list(session.modules)
        lib.getVar('audioServer').cleanup_module()
        if previous and not target['modules']:
            with instance_context(previous[0]):
                frame.controlPanel.setPlugins({})
        for module in target['modules']:
            if module.retired and module.editor.graph.plotter.getTotalTime() != lib.getVar('totalTime'):
                with instance_context(module):
                    module.editor.graph.setTotalTime(lib.getVar('totalTime'))
            module.retired = False
        if previous and target['modules']:
            ChainUI.transfer_effect_graphs(previous[0], target['modules'][0])
        for module in previous:
            if module not in target['modules']:
                self.park(module)
        session.modules = list(target['modules'])
        session.restore_routing(target['routing'])
        session.selected_id = target['selected']
        if not previous and session.modules:
            with instance_context(session.modules[0]):
                frame.controlPanel.setPlugins(target.get('effects', {}).get('plugins', {}))
                lib.againForPluginKnobs(target.get('effects', {}))
        frame.grid.selected_edge = None
        ChainUI.refresh(frame)

