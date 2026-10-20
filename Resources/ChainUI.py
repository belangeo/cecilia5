"""Persistent editors and the audio routing graph."""

import os
import wx
from .RoutingGraph import RoutingGraph
from . import CeciliaLib, Control, Preset
from .Grapher import getGrapher, buildGrapher
from .Session import ModuleInstance, instance_context
from .Widgets import CustomMenu
from .constants import BACKGROUND_COLOUR, CONTROLLABEL_BACK_COLOUR, WIDGET_BORDER_COLOUR


class ModuleMenu(CustomMenu):
    """Use Cecilia's popup styling to open the categorized module menu."""
    def __init__(self, parent, openMenu):
        super().__init__(parent, choice=['Add Module...'], size=(120, 20),
                         colour=CONTROLLABEL_BACK_COLOUR)
        self.openMenu = openMenu

    def MouseDown(self, event):
        if self._enable:
            self.openMenu(event)


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
    # GTK themes can give BORDER_SIMPLE a multi-pixel appearance. Reserve
    # exactly one pixel outside the scrolling content for each border edge.
    controlBorder = wx.Panel(frame, style=wx.BORDER_NONE)
    controlBorder.SetBackgroundColour(WIDGET_BORDER_COLOUR)
    controlBorder.SetMinSize((232, -1))
    controlBorder.SetMaxSize((232, -1))
    borderSizer = wx.BoxSizer(wx.VERTICAL)
    # Construct shared transport, output and effects without module inputs.
    empty = ModuleInstance('', type('EmptyModule', (), {}), [])
    with instance_context(empty):
        frame.controlPanel = Control.CECControl(controlBorder, -1, style=wx.BORDER_NONE)
    borderSizer.Add(frame.controlPanel, 1, wx.EXPAND | wx.ALL, 1)
    controlBorder.SetSizer(borderSizer)
    frame.controlBox.Add(controlBorder, 1, wx.EXPAND)
    frame.moduleHost = wx.Panel(frame)
    frame.moduleHost.SetSizer(wx.BoxSizer(wx.VERTICAL))
    frame.controlBox.Add(frame.moduleHost, 0, wx.EXPAND)
    frame.box.Add(frame.controlBox, (0, 0), span=(3, 1), flag=wx.EXPAND)

    toolbar = wx.Panel(frame)
    tools = wx.BoxSizer(wx.HORIZONTAL)
    frame.viewChoice = CustomMenu(
        toolbar, choice=['Editor', 'Routing'], init='Editor',
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
    frame.grid = RoutingGraph(frame.graphHost, frame)
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
    # All source panels share the input host; only the reference source is shown.
    inputSizer = frame.controlPanel.inputPanel.GetSizer()
    inputSizer.Clear(False)
    for module in session.modules:
        is_source = module.id in session.source_ids
        panel = module.inputs.inputPanel
        parent = frame.controlPanel.inputPanel if is_source else frame.moduleHost
        if panel.GetParent() is not parent:
            panel.Reparent(parent)
        if is_source:
            inputSizer.Add(panel, 0, wx.EXPAND)
        panel.Hide()
        if module.inputs.inputTitle is not None:
            module.inputs.inputTitle.SetLabel('INPUT — ' + module.state['currentModuleName'] if is_source else 'AUXILIARY FILES')
        for widget in module.inputs.cfileinList:
            downstream = not is_source and widget.name == module.primary_input
            widget.Show(not downstream)
            widget.Enable(not downstream)
            if downstream and widget.samplerFrame is not None:
                widget.samplerFrame.Hide()
            if widget in module.state['userSamplers']:
                with instance_context(module):
                    module.editor.graph.setSamplerLineStates(widget.name, not downstream and widget.mode != 1)
            if not is_source and widget.name in module.auxiliary_inputs:
                widget.modebutton.Hide()
                widget.onChangeMode(0)
            elif not downstream:
                widget.modebutton.Show()
    frame.controlPanel.pluginsPanel.Enable(bool(session.modules))
    frame.controlPanel.transportButtons.Enable(bool(session.modules))
    select(frame, session.selected, change_view=False, preserve_source=True)
    rebuild_grid(frame)
    show_view(frame, session.view)
    frame.controlPanel.Layout()
    frame.controlPanel.SetupScrolling(scroll_x=False)


def show_source_inputs(frame):
    session = CeciliaLib.session
    for source in session.sources:
        source.inputs.inputPanel.Show(source is session.source)
    frame.controlPanel.cfileinList = session.source.inputs.cfileinList if session.source else []
    frame.controlPanel.inputPanel.InvalidateBestSize()
    frame.controlPanel.InvalidateBestSize()
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


def select(frame, module, change_view=True, preserve_source=False):
    session = CeciliaLib.session
    session.select(module, preserve_source=preserve_source)
    for host in (frame.graphHost, frame.sliderHost, frame.moduleHost):
        host.GetSizer().Clear(False)
    for item in session.modules:
        for window in (item.editor.graph, item.editor.sliders,
                       item.editor.presets, item.editor.toggles):
            window.Hide()
        if item.id not in session.source_ids:
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
        if module.id not in session.source_ids and module.auxiliary_inputs:
            frame.moduleHost.GetSizer().Add(module.inputs.inputPanel, 0, wx.EXPAND | wx.BOTTOM, 8)
            module.inputs.inputPanel.Show()
        frame.moduleHost.GetSizer().Add(editor.toggles, 0, wx.EXPAND)
        editor.presets.Show()
        editor.presets.loadPresets()
        editor.graph.plotter.updateUndoMenu()
        editor.toggles.Show()
        frame.stageLabel.SetLabel(module.state['currentModuleName'])
        update_title(frame)
        editor.presets.presetChoice.setEnable(not CeciliaLib.getVar('audioServer').isAudioServerRunning())
    else:
        frame.grapher = frame.presetPanel = None
        frame.stageLabel.SetLabel('No module loaded')
        update_title(frame)
    show_source_inputs(frame)
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


def rebuild_grid(frame):
    frame.structuralButtons = []
    frame.grid.rebuild()


def playback_state(frame, running):
    frame.addModuleButton.setEnable(not running)
    if running and frame.grid.drag and frame.grid.drag[0] == 'cable':
        frame.grid.drag = None
    frame.grid.running = running
    frame.grid.Refresh()
    for button, enabled in getattr(frame, 'structuralButtons', []):
        button.Enable(enabled and not running)
    for module in CeciliaLib.session.modules:
        module.editor.presets.presetChoice.setEnable(not running)
        for widget in module.inputs.cfileinList:
            # File samplers support changing sounds during playback. Only the
            # primary inputs supplied by an upstream stage are unavailable.
            widget.Enable(not (module.id not in CeciliaLib.session.source_ids and widget.name == module.primary_input))
    for item in frame.chainMenuItems:
        item.Enable(not running)


def destroy_editors(frame):
    for host in (frame.graphHost, frame.sliderHost, frame.moduleHost):
        host.GetSizer().Clear(False)
    frame.controlPanel.inputPanel.GetSizer().Clear(False)
    for module in CeciliaLib.session.modules:
        if module.editor:
            module.editor.destroy()
