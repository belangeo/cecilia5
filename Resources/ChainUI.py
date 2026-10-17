"""Persistent editors and the serial chain overview."""

import os
import wx
import wx.lib.scrolledpanel as scrolled
from . import CeciliaLib, Control, Preset
from .Grapher import getGrapher, buildGrapher
from .Session import ModuleInstance, instance_context
from .Widgets import CustomMenu, MainLabel
from .constants import BACKGROUND_COLOUR, CONTROLLABEL_BACK_COLOUR, CPOLY_COLOUR, LABEL_FONT, LABEL_LABEL_COLOUR, WIDGET_BORDER_COLOUR


class ModuleMenu(CustomMenu):
    """Use Cecilia's popup styling to open the categorized module menu."""
    def __init__(self, parent, openMenu):
        super().__init__(parent, choice=['Add Module...'], size=(120, 20),
                         colour=CONTROLLABEL_BACK_COLOUR)
        self.openMenu = openMenu

    def MouseDown(self, event):
        if self._enable:
            self.openMenu(event)


class ChainCard(wx.Panel):
    def __init__(self, parent, selected=False):
        super().__init__(parent)
        self.SetBackgroundColour(parent.GetBackgroundColour())
        self.borderColour = WIDGET_BORDER_COLOUR if selected else '#333333'
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.onSize)

    def onPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.SetPen(wx.Pen(self.borderColour))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        width, height = self.GetClientSize()
        dc.DrawRectangle(0, 0, width, height)

    def onSize(self, event):
        self.Refresh()
        event.Skip()


class GridButton(MainLabel):
    """Clickable control using the same font, fill and border as polyphony labels."""
    def __init__(self, parent, label):
        font = wx.Font(LABEL_FONT, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc = wx.ClientDC(parent)
        dc.SetFont(font)
        width, height = dc.GetTextExtent(label)
        size = (max(68, width + 14), max(20, height + 6))
        super().__init__(parent, label, size=size, font=font, colour=CPOLY_COLOUR)
        self.SetMinSize(size)
        self.SetMaxSize((-1, size[1]))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetName(label)
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        self.pressed = False
        self.Bind(wx.EVT_LEFT_DOWN, self.onPress)
        self.Bind(wx.EVT_LEFT_UP, self.onRelease)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.onCaptureLost)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(self.backgroundBrush)
        dc.Clear()
        gc = wx.GraphicsContext_Create(dc)
        gc.SetPen(self.borderPen)
        gc.SetBrush(wx.Brush('#333333' if self.pressed else self.colour))
        width, height = self.GetClientSize()
        gc.DrawRoundedRectangle(0, 0, width - 1, height - 1, 3)
        dc.SetFont(self.font)
        dc.SetTextForeground(LABEL_LABEL_COLOUR if self.IsEnabled() else '#888888')
        dc.DrawLabel(self.label, wx.Rect(0, 0, width, height), wx.ALIGN_CENTER)

    def Enable(self, enable=True):
        result = super().Enable(enable)
        self.Refresh()
        return result

    def onPress(self, event):
        if self.IsEnabled():
            self.SetFocus()
            self.pressed = True
            self.CaptureMouse()
            self.Refresh()

    def onRelease(self, event):
        activate = self.pressed and self.IsEnabled() and self.GetClientRect().Contains(event.GetPosition())
        self.pressed = False
        if self.HasCapture():
            self.ReleaseMouse()
        self.Refresh()
        if activate:
            self.activate()

    def onCaptureLost(self, event):
        self.pressed = False
        self.Refresh()

    def onKey(self, event):
        if self.IsEnabled() and event.GetKeyCode() in (wx.WXK_SPACE, wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.activate()
        else:
            event.Skip()

    def activate(self):
        event = wx.CommandEvent(wx.EVT_BUTTON.typeId, self.GetId())
        event.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(event)


class ModuleInputs:
    """Module-owned input widgets with shared transport/output delegation."""
    getCfileinList = Control.CECControl.getCfileinList
    getCfileinFromName = Control.CECControl.getCfileinFromName

    def __init__(self, frame, module):
        self.shared = frame.controlPanel
        self.module = module
        module.inputs = self
        Control.CECControl.createInputPanel(self, parent=frame.controlPanel.inputPanel)
        self.inputPanel.Hide()

    def __getattr__(self, name):
        shared = self.__dict__.get('shared')
        if shared is not None:
            return getattr(shared, name)
        raise AttributeError(name)


class ModuleEditor:
    def __init__(self, frame, module):
        self.module = module
        module.editor = self
        with instance_context(module):
            CeciliaLib.importEmbeddedPresets(module)
            ModuleInputs(frame, module)
            self.graph = getGrapher(frame)
            self.graph.Reparent(frame.graphHost)
            # Parked editors may draw before wx delivers their first size event.
            self.graph.plotter._setSize()
            CeciliaLib.setVar('grapher', self.graph)
            self.sliders, _ = frame.createSlidersPanel(parent=frame.sliderHost)
            self.toggles, _, _ = frame.createTogglePopupPanel(parent=frame.moduleHost)
            self.presets = Preset.CECPreset(frame.moduleHost)
            CeciliaLib.setVar('presetPanel', self.presets)
            self.presets.loadPresets()
            buildGrapher(self.graph)
            for slider in module.state['userSliders']:
                slider.refresh()
            CeciliaLib.savePresetToFile('init')
        for window in (self.graph, self.sliders, self.toggles, self.presets):
            window.Hide()

    def destroy(self):
        with instance_context(self.module):
            for slider in self.module.state['userSliders']:
                slider.cleanup()
            inputs = self.module.inputs
            if inputs is not None:
                for widget in getattr(inputs, 'cfileinList', []):
                    if widget.samplerFrame is not None:
                        widget.samplerFrame.Destroy()
            windows = [getattr(self, name, None) for name in ('graph', 'sliders', 'toggles', 'presets')]
            if inputs is not None:
                windows.append(getattr(inputs, 'inputPanel', None))
            for window in windows:
                if window:
                    window.Destroy()
        self.module.editor = self.module.inputs = None
        self.module.retired = True


def initialize(frame):
    """Create the shared chrome once; each module retains its own editor."""
    CeciliaLib.setVar('interface', frame)
    frame.SetBackgroundColour(BACKGROUND_COLOUR)
    frame.box = wx.GridBagSizer()
    frame.controlBox = wx.BoxSizer(wx.VERTICAL)
    # Construct shared transport, output and effects without module inputs.
    empty = ModuleInstance('', type('EmptyModule', (), {}), [])
    with instance_context(empty):
        frame.controlPanel = Control.CECControl(frame, -1)
    frame.controlBox.Add(frame.controlPanel, 1, wx.EXPAND)
    frame.moduleHost = wx.Panel(frame)
    frame.moduleHost.SetSizer(wx.BoxSizer(wx.VERTICAL))
    frame.controlBox.Add(frame.moduleHost, 0, wx.EXPAND)
    frame.box.Add(frame.controlBox, (0, 0), span=(3, 1), flag=wx.EXPAND)

    toolbar = wx.Panel(frame)
    tools = wx.BoxSizer(wx.HORIZONTAL)
    frame.viewChoice = CustomMenu(
        toolbar, choice=['Graph', 'Chain'], init='Graph',
        outFunction=lambda index, label: show_view(frame, 'graph' if index == 0 else 'chain'),
        colour=CONTROLLABEL_BACK_COLOUR)
    tools.Add(frame.viewChoice, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
    add = ModuleMenu(toolbar, frame.menubar.showModuleMenu)
    tools.Add(add, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
    frame.addModuleButton = add
    frame.stageLabel = wx.StaticText(toolbar, label='No module loaded')
    frame.stageLabel.SetForegroundColour(wx.WHITE)
    tools.Add(frame.stageLabel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 4)
    toolbar.SetSizer(tools)
    frame.box.Add(toolbar, (0, 1), flag=wx.EXPAND)

    frame.graphHost = wx.Panel(frame)
    frame.graphHost.SetMinSize((100, 100))
    frame.graphHost.SetSizer(wx.BoxSizer(wx.VERTICAL))
    frame.grid = scrolled.ScrolledPanel(frame.graphHost)
    frame.grid.SetBackgroundColour(BACKGROUND_COLOUR)
    frame.grid.SetMinSize((100, 100))
    frame.grid.SetSizer(wx.GridSizer(cols=4, hgap=8, vgap=8))
    frame.grid.Bind(wx.EVT_SIZE, lambda event: grid_size(frame, event))
    frame.sliderHost = wx.Panel(frame)
    frame.sliderHost.SetSizer(wx.BoxSizer(wx.VERTICAL))
    frame.box.Add(frame.graphHost, (1, 1), flag=wx.EXPAND)
    frame.box.Add(frame.sliderHost, (2, 1), flag=wx.EXPAND)
    frame.box.AddGrowableCol(1)
    frame.box.AddGrowableRow(1)
    frame.grapher = frame.presetPanel = None
    frame.SetSizer(frame.box)
    for module in CeciliaLib.session.modules:
        ModuleEditor(frame, module)
    refresh(frame)


def refresh(frame):
    session = CeciliaLib.session
    first = session.modules[0] if session.modules else None
    # The shared top-left input panel always belongs to the first stage.
    inputSizer = frame.controlPanel.inputPanel.GetSizer()
    inputSizer.Clear(False)
    for index, module in enumerate(session.modules):
        panel = module.inputs.inputPanel
        if index == 0:
            if panel.GetParent() is not frame.controlPanel.inputPanel:
                panel.Reparent(frame.controlPanel.inputPanel)
            inputSizer.Add(panel, 0, wx.EXPAND)
        else:
            if panel.GetParent() is not frame.moduleHost:
                panel.Reparent(frame.moduleHost)
        panel.Hide()
        if module.inputs.inputTitle is not None:
            module.inputs.inputTitle.SetLabel('INPUT' if index == 0 else 'AUXILIARY FILES')
        for widget in module.inputs.cfileinList:
            downstream = index > 0 and widget.name == module.primary_input
            widget.Show(not downstream)
            widget.Enable(not downstream)
            if downstream and widget.samplerFrame is not None:
                widget.samplerFrame.Hide()
            if widget in module.state['userSamplers']:
                with instance_context(module):
                    module.editor.graph.setSamplerLineStates(widget.name, not downstream and widget.mode != 1)
            if index > 0 and widget.name in module.auxiliary_inputs:
                widget.modebutton.Hide()
                widget.onChangeMode(0)
            elif not downstream:
                widget.modebutton.Show()
    frame.controlPanel.cfileinList = first.inputs.cfileinList if first else []
    frame.controlPanel.pluginsPanel.Enable(first is not None)
    frame.controlPanel.transportButtons.Enable(first is not None)
    if first:
        first.inputs.inputPanel.Show()
    frame.controlPanel.inputPanel.InvalidateBestSize()
    frame.controlPanel.InvalidateBestSize()
    select(frame, session.selected, change_view=False)
    rebuild_grid(frame)
    show_view(frame, session.view)
    frame.controlPanel.Layout()
    frame.controlPanel.SetupScrolling(scroll_x=False)


def transfer_effect_graphs(previous, current):
    if previous is None or current is None or previous is current:
        return
    source, target = previous.editor.graph, current.editor.graph
    lines = [line for line in source.plotter.data
             if line.slider is not None and line.slider.widget_type == 'plugin_knob']
    if not lines:
        return
    labels = {line.getLabel() for line in lines}
    source.plotter.data[:] = [line for line in source.plotter.data if line not in lines]
    target.plotter.data.extend(lines)
    for line in lines:
        line._cecilia_owner = current
    source.toolbar.setPopupChoice([label for label in source.toolbar.getPopupChoice() if label not in labels])
    target.toolbar.setPopupChoice(target.toolbar.getPopupChoice() + [line.getLabel() for line in lines])
    for graph in (source, target):
        graph.plotter.selected = 0
        graph.plotter.draw()


def select(frame, module, change_view=True):
    session = CeciliaLib.session
    session.selected_id = module.id if module else None
    for host in (frame.graphHost, frame.sliderHost, frame.moduleHost):
        host.GetSizer().Clear(False)
    for item in session.modules:
        for window in (item.editor.graph, item.editor.sliders,
                       item.editor.presets, item.editor.toggles):
            window.Hide()
        if item is not session.modules[0]:
            item.inputs.inputPanel.Hide()
        # Close detached sampler windows when their module loses selection.
        if item is not module:
            for widget in item.inputs.cfileinList:
                if widget.samplerFrame is not None:
                    widget.samplerFrame.Hide()
    if module:
        editor = module.editor
        frame.grapher, frame.presetPanel = editor.graph, editor.presets
        frame.graphHost.GetSizer().Add(editor.graph, 1, wx.EXPAND)
        frame.sliderHost.GetSizer().Add(editor.sliders, 0, wx.EXPAND)
        frame.moduleHost.GetSizer().Add(editor.presets, 0, wx.EXPAND)
        if module is not session.modules[0] and module.auxiliary_inputs:
            frame.moduleHost.GetSizer().Add(module.inputs.inputPanel, 0, wx.EXPAND | wx.BOTTOM, 8)
            module.inputs.inputPanel.Show()
        frame.moduleHost.GetSizer().Add(editor.toggles, 0, wx.EXPAND)
        editor.presets.Show()
        editor.presets.loadPresets()
        editor.graph.plotter.updateUndoMenu()
        editor.toggles.Show()
        frame.stageLabel.SetLabel('Stage %d — %s' % (session.modules.index(module)+1, module.state['currentModuleName']))
        update_title(frame)
        editor.presets.presetChoice.setEnable(not CeciliaLib.getVar('audioServer').isAudioServerRunning())
    else:
        frame.grapher = frame.presetPanel = None
        frame.stageLabel.SetLabel('No module loaded')
        update_title(frame)
    frame.graphHost.GetSizer().Add(frame.grid, 1, wx.EXPAND)
    if change_view:
        session.view = 'graph'
    show_view(frame, session.view)
    frame.Layout()


def update_title(frame):
    session = CeciliaLib.session
    parts = ['Cecilia']
    if session.path:
        parts.append(os.path.basename(session.path))
    if session.selected:
        parts.append('%s (%d modules)' % (session.selected.state['currentModuleName'], len(session.modules)))
    frame.SetTitle(' — '.join(parts))


def show_view(frame, view):
    session = CeciliaLib.session
    if not session.modules:
        view = 'chain'
    session.view = view
    frame.viewChoice.setByIndex(0 if view == 'graph' else 1)
    frame.grid.Show(view == 'chain')
    if session.selected:
        session.selected.editor.graph.Show(view == 'graph')
        session.selected.editor.sliders.Show()
    frame.sliderHost.Show(session.selected is not None)
    frame.graphHost.Layout()
    frame.Layout()
    if view == 'chain':
        rebuild_grid(frame)


def grid_size(frame, event):
    # Narrow windows retain readable cards; serial order stays row-major.
    columns = max(1, min(4, (event.GetSize().width + 8) // 180))
    sizer = frame.grid.GetSizer()
    if sizer.GetCols() != columns:
        sizer.SetCols(columns)
        frame.grid.Layout()
        frame.grid.FitInside()
    event.Skip()


def rebuild_grid(frame):
    session = CeciliaLib.session
    sizer = frame.grid.GetSizer()
    sizer.Clear(True)
    frame.structuralButtons = []
    if not session.modules:
        sizer.Add(wx.StaticText(frame.grid, label='Open a module to start a chain.'), 0, wx.ALL, 16)
    for index, module in enumerate(session.modules):
        card = ChainCard(frame.grid, selected=session.selected is module)
        box = wx.BoxSizer(wx.VERTICAL)
        label = '%d. %s' % (index+1, module.state['currentModuleName'])
        title = wx.StaticText(card, label=label)
        title.SetForegroundColour(wx.WHITE)
        title.Wrap(150)
        box.Add(title, 0, wx.ALL, 8)
        status = 'Live stream input' if module.primary_input else 'First stage only'
        if index < len(session.modules)-1:
            status += '  → stage %d' % (index+2)
        else:
            status += '  → effects / output'
        statusLabel = wx.StaticText(card, label=status)
        statusLabel.SetForegroundColour(wx.WHITE)
        statusLabel.Wrap(150)
        box.Add(statusLabel, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)
        edit = lambda event, m=module: select(frame, m)
        for window in (card, title, statusLabel):
            window.Bind(wx.EVT_LEFT_DCLICK, edit)
        buttons = wx.GridSizer(cols=2, hgap=2, vgap=2)
        for caption, callback, structural, enabled in (
            ('Edit', edit, False, True),
            ('Remove', lambda event, m=module: CeciliaLib.removeChainModule(m), True, True),
            ('Move earlier', lambda event, m=module: CeciliaLib.moveChainModule(m, -1), True, index > 0),
            ('Move later', lambda event, m=module: CeciliaLib.moveChainModule(m, 1), True, index < len(session.modules)-1),
        ):
            button = GridButton(card, caption)
            button.Bind(wx.EVT_BUTTON, callback)
            button.Enable(enabled and (not structural or not CeciliaLib.getVar('audioServer').isAudioServerRunning()))
            buttons.Add(button, 0, wx.EXPAND | wx.ALL, 3)
            if structural:
                frame.structuralButtons.append((button, enabled))
        box.Add(buttons, 0, wx.ALL, 4)
        card.SetSizer(box)
        sizer.Add(card, 0, wx.EXPAND | wx.ALL, 4)
    frame.grid.Layout()
    frame.grid.SetupScrolling(scroll_x=False)


def playback_state(frame, running):
    frame.addModuleButton.setEnable(not running)
    for button, enabled in getattr(frame, 'structuralButtons', []):
        button.Enable(enabled and not running)
    for module in CeciliaLib.session.modules:
        module.editor.presets.presetChoice.setEnable(not running)
        for widget in module.inputs.cfileinList:
            widget.Enable(not running and not (module is not CeciliaLib.session.modules[0] and widget.name == module.primary_input))
    for item in frame.chainMenuItems:
        item.Enable(not running)


def destroy_editors(frame):
    for host in (frame.graphHost, frame.sliderHost, frame.moduleHost):
        host.GetSizer().Clear(False)
    frame.controlPanel.inputPanel.GetSizer().Clear(False)
    for module in CeciliaLib.session.modules:
        if module.editor:
            module.editor.destroy()
