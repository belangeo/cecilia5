"""Explicit user-event boundaries for the session history.

Only UI handlers and user commit entrypoints are wrapped. General setters,
painting, MIDI/OSC updates and automation playback remain uninstrumented.
"""
from functools import wraps

_installed = False


def wrap(method, name):
    @wraps(method)
    def event(self, *args, **kwargs):
        import wx
        from . import CeciliaLib as lib
        history = lib.session.history
        if name == 'OnKeyDown' and args:
            key = args[0]
            # Modifier/shortcut/navigation keys are not editing gestures. In
            # particular, opening a burst for Ctrl disables the menu accelerator
            # before the following Z can invoke Undo.
            if (key.CmdDown() or key.AltDown() or key.GetKeyCode() not in
                    (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE, wx.WXK_BACK)):
                return method(self, *args, **kwargs)
        if name == 'onChar' and args and args[0].GetKeyCode() == wx.WXK_ESCAPE:
            self.new = ''
            self.selected = False
            self.Refresh()
            return
        if not hasattr(history, 'begin'):
            return method(self, *args, **kwargs)
        if not history.ready() and history.active is None:
            return method(self, *args, **kwargs)
        if name == 'MouseMotion' and history.active is None:
            return method(self, *args, **kwargs)
        value_before = self.GetValue() if hasattr(self, '_history_emit') else None
        finishing = name in ('MouseUp', 'OnMouseLeftUp', 'OnMouseRightUp')
        token = None
        target = {}
        owner = getattr(self, '_cecilia_owner', None)
        if owner is None:
            owner = lib.active_instance.get()
        if owner in lib.session.modules:
            target['module'] = owner.id
        control = getattr(self, 'cecslider', None)
        if control is not None:
            target['control'] = control.getName()
        if name == 'onPresetSelect':
            target['operation'] = 'preset'
        if name in ('onLoadFile', 'updateMenuFromPath', 'OnDropFiles'):
            target['operation'] = 'soundfile'
        if isinstance(self, wx.Window):
            parent = self.GetParent()
            while parent:
                panel = lib.getVar('interface').controlPanel
                if hasattr(parent, 'getKnobs') and parent in panel.plugins:
                    ids = history.effect_ids()
                    slot = panel.plugins.index(parent)
                    target.update(effect=ids[slot], effect_slot=slot)
                    if self is getattr(parent, 'choice', None):
                        target['operation'] = 'effect_selection'
                    break
                parent = parent.GetParent()
        label = {'entryReturn': 'Change value', 'onPresetSelect': 'Load preset',
                 'onLoadFile': 'Change soundfile', 'updateMenuFromPath': 'Change soundfile',
                 'OnLoad': 'Import curve', 'onReset': 'Reset curve',
                 'onPaste': 'Paste curve', 'replacePlugin': 'Replace effect',
                 'movePlugin': 'Move effect', 'OnApply': 'Apply settings',
                 'onApply': 'Apply settings'}.get(name, 'Edit ' + self.__class__.__name__)
        burst = name in ('OnMouseWheel', 'MouseWheel', 'OnKeyDown')
        if history.active and history.burst_target is not None and history.burst_target is not self:
            history.finish(history.active)
        if not finishing:
            token = history.begin(label, target)
        try:
            if name == 'LooseFocus' and getattr(self, 'new', '') and hasattr(self, '_history_emit'):
                try:
                    self.SetValue(eval(self.new))
                except (ValueError, SyntaxError, TypeError, NameError):
                    pass
                self.new = ''
            result = method(self, *args, **kwargs)
            if hasattr(self, '_history_emit') and self.GetValue() != value_before:
                self._history_emit()
        except Exception:
            history.finish(token, False)
            raise
        if finishing:
            if history.active and history.active.get('gesture') is self:
                capture = history.active.get('capture')
                if capture and capture.HasCapture():
                    capture.ReleaseMouse()
                history.finish(history.active)
        elif token is not None:
            capture = wx.Window.GetCapture()
            if name == 'OnMouseLeftDown' and hasattr(self, 'canvas') and capture is None:
                self.canvas.CaptureMouse()
                capture = self.canvas
            if name in ('MouseDown', 'MouseRightDown', 'OnMouseLeftDown', 'OnMouseRightDown') and capture:
                token['gesture'] = self
                token['capture'] = capture
                # Capture loss is also a completed gesture, including when the
                # application loses activation before receiving a mouse-up.
                if not getattr(capture, '_history_capture_bound', False):
                    def lost(evt):
                        active = history.active
                        if active and active.get('capture') is capture:
                            gesture = active.get('gesture')
                            if hasattr(gesture, 'canvas'):
                                gesture.point = gesture.curve = None
                                gesture.movingCurve = False
                            history.finish(active)
                        evt.Skip()
                    capture.Bind(wx.EVT_MOUSE_CAPTURE_LOST, lost)
                    capture._history_capture_bound = True
                history.update_menu()
            elif burst:
                history.burst_target = self
                if history.burst_timer:
                    history.burst_timer.Stop()
                history.burst_timer = wx.CallLater(300, history.finish, token)
            else:
                history.finish(token)
        elif burst and history.active and history.burst_target is self:
            if history.burst_timer:
                history.burst_timer.Stop()
            history.burst_timer = wx.CallLater(300, history.finish, history.active)
        return result
    event._session_history_event = True
    return event


def install():
    global _installed
    if _installed:
        return
    _installed = True
    from . import Widgets, Sliders, TogglePopup, Control, Plugins, Grapher, Preset
    mouse = ('MouseDown', 'MouseRightDown', 'MouseMotion', 'MouseUp', 'DoubleClick', 'onChar', 'LooseFocus',
             'OnMouseWheel', 'MouseWheel', 'OnKeyDown')
    groups = [
        (Widgets, ('ControlSlider', 'CustomMenu', 'FolderPopup', 'Toggle', 'XfadeSwitcher',
                   'InputModeButton', 'EntryUnit', 'RangeEntryUnit', 'SplitterEntryUnit',
                   'ControlKnob', 'PlainSlider', 'Label'), mouse),
        (Sliders, ('Slider', 'HSlider', 'HRangeSlider', 'HSplitterSlider', 'PlayRecButtons'), mouse),
        (Sliders, ('CECSlider', 'CECRange', 'CECSplitter'), ('entryReturn', 'onLabelClick')),
        (Widgets, ('ListEntryPopupFrame', 'OSCPopupFrame', 'RandomFrame', 'WavesFrame', 'ProcessFrame'), ('OnApply',)),
        (Widgets, ('MySoundfileDropTarget',), ('OnDropFiles',)),
        (Widgets, ('Label',), ('OnLeftDown', 'OnRightDown')),
        (Control, ('SamplerControlSlider', 'SamplerPlayRecButtons'), mouse),
        (Control, ('CInputBase',), ('onLoadFile', 'updateMenuFromPath')),
        (Control, ('SamplerSlider',), ('onMidiLearn',)),
        (Control, ('CECControl',), ('onSelectOutputFilename', 'onReuseOutputFile', 'onFormatChange')),
        (Plugins, ('PluginKnob', 'PluginArrow'), mouse),
        (Grapher, ('Grapher',), ('OnMouseLeftDown', 'OnMouseLeftUp', 'OnMouseRightDown',
                                'OnMouseRightUp', 'OnMouseDoubleClick', 'OnKeyDown', 'onPaste')),
        (Grapher, ('CECGrapher',), ('OnLoad', 'onReset')),
        (Grapher, ('CursorPanel',), ('OnLeftDown',)),
        (Preset, ('CECPreset',), ('onPresetSelect',)),
    ]
    # Value delivery is independent of repaint and shared by pyo-based controls,
    # effect knobs, and the sliders used by curve-processing dialogs.
    def emit(self):
        if not getattr(self, '_history_initialized', False):
            return
        if self.outFunction:
            self.outFunction(self.GetValue())

    for cls in (Widgets.ControlSlider, Widgets.ControlKnob, Widgets.PlainSlider):
        cls._history_emit = emit
        original_init = cls.__init__
        def initialize(self, *args, _method=original_init, **kwargs):
            self._history_initialized = False
            _method(self, *args, **kwargs)
            self._history_initialized = True
        cls.__init__ = initialize

    for cls in (Sliders.Slider, Sliders.RangeSlider, Sliders.SplitterSlider):
        original_resize = cls.OnResize
        def resize(self, event, _method=original_resize):
            if self and all(dimension > 0 for dimension in self.GetSize()):
                return _method(self, event)
        cls.OnResize = resize

    for module, classes, methods in groups:
        for class_name in classes:
            cls = getattr(module, class_name, None)
            if cls is None:
                continue
            for name in methods:
                method = getattr(cls, name, None)
                if method is not None and not getattr(method, '_session_history_event', False):
                    setattr(cls, name, wrap(method, name))
