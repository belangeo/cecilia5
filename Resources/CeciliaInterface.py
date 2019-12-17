# encoding: utf-8
"""
Copyright 2019 iACT, Universite de Montreal,
Jean Piche, Olivier Belanger, Jean-Michel Dumas

This file is part of Cecilia 5.

Cecilia 5 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cecilia 5 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cecilia 5.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx
import Resources.CeciliaLib as CeciliaLib
import Resources.Control as Control
import Resources.Preset as Preset
from .constants import *
from .Sliders import buildHorizontalSlidersBox
from .Grapher import getGrapher, buildGrapher
from .TogglePopup import buildTogglePopupBox
from .menubar import InterfaceMenuBar

class CeciliaInterface(wx.Frame):
    if CeciliaLib.getVar("systemPlatform").startswith('linux'):
        style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
                wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN | wx.WANTS_CHARS
    else:
        style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | \
                wx.SYSTEM_MENU | wx.CAPTION | wx.BORDER_SUNKEN | \
                wx.CLIP_CHILDREN | wx.WANTS_CHARS
    def __init__(self, parent, id=-1, title='', mainFrame=None,
                 pos=wx.DefaultPosition, size=wx.DefaultSize, style=style):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.ceciliaMainFrame = mainFrame
        self.menubar = InterfaceMenuBar(self, self.ceciliaMainFrame)
        self.SetMenuBar(self.menubar)

        self.box = wx.GridBagSizer(0, 0)

        self.controlBox = wx.BoxSizer(wx.VERTICAL)

        self.controlPanel = Control.CECControl(self, -1)
        togglePopupPanel, objs, tpsize = self.createTogglePopupPanel()
        slidersPanel, slPanelSize = self.createSlidersPanel()
        self.grapher = getGrapher(self)
        CeciliaLib.setVar("grapher", self.grapher)
        self.presetPanel = Preset.CECPreset(self)
        CeciliaLib.setVar("presetPanel", self.presetPanel)

        self.controlBox.Add(self.controlPanel, 1, wx.EXPAND | wx.RIGHT, -1)
        self.controlBox.Add(self.presetPanel, 0, wx.EXPAND | wx.TOP | wx.RIGHT, -1)
        self.controlBox.Add(togglePopupPanel, 0, wx.EXPAND | wx.TOP | wx.RIGHT, -1)

        self.box.Add(self.controlBox, (0, 0), span=(2, 1), flag=wx.EXPAND)
        self.box.Add(self.grapher, (0, 1), flag=wx.EXPAND)
        self.box.Add(slidersPanel, (1, 1), flag=wx.EXPAND | wx.TOP, border=-1)

        self.box.AddGrowableCol(1, 1)
        self.box.AddGrowableRow(0, 1)

        pos = CeciliaLib.getVar("interfacePosition")
        size = CeciliaLib.getVar("interfaceSize")
        pos, size = self.positionToClientArea(pos, size)

        self.SetSizer(self.box)
        self.SetSize(size)

        self.Bind(wx.EVT_CLOSE, self.onClose)

        if pos is None:
            self.Center()
        else:
            self.SetPosition(pos)

        self.Show()

        wx.CallLater(100, self.createGrapher)

    def positionToClientArea(self, pos, size):
        position = None
        screen = 0
        if pos is not None:
            for i in range(CeciliaLib.getVar("numDisplays")):
                off = CeciliaLib.getVar("displayOffset")[i]
                dispsize = CeciliaLib.getVar("displaySize")[i]
                Xbounds = [off[0], dispsize[0] + off[0]]
                Ybounds = [off[1], dispsize[1] + off[1]]
                if pos[0] >= Xbounds[0] and pos[0] <= Xbounds[1] and \
                   pos[1] >= Ybounds[0] and pos[1] <= Ybounds[1]:
                    position = pos
                    screen = i
                    break
        dispsize = CeciliaLib.getVar("displaySize")[screen]
        if size[0] <= dispsize[0] and size[1] <= dispsize[1]:
            newsize = size
        else:
            newsize = (dispsize[0] - 50, dispsize[1] - 50)
        return position, newsize

    def updateTitle(self, title):
        self.SetTitle(title)

    def createGrapher(self, evt=None):
        buildGrapher(self.grapher)
        for slider in CeciliaLib.getVar("userSliders"):
            slider.refresh()
        if CeciliaLib.getVar("presetToLoad") is not None:
            CeciliaLib.loadPresetFromFile(CeciliaLib.getVar("presetToLoad"))
            CeciliaLib.setVar("presetToLoad", None)

    def createTogglePopupPanel(self):
        panel = wx.Panel(self, -1, style=wx.BORDER_SIMPLE)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        widgets = CeciliaLib.getVar("interfaceWidgets")
        box, objs = buildTogglePopupBox(panel, widgets)
        panel.SetSizerAndFit(box)
        CeciliaLib.setVar("userTogglePopups", objs)
        size = panel.GetSize()
        return panel, objs, size

    def createSlidersPanel(self):
        panel = wx.Panel(self, -1, style=wx.BORDER_SIMPLE)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        widgets = CeciliaLib.getVar("interfaceWidgets")
        box, sl = buildHorizontalSlidersBox(panel, widgets)
        CeciliaLib.setVar("userSliders", sl)
        panel.SetSizerAndFit(box)
        size = panel.GetSize()
        return panel, size

    def onClose(self, event):
        CeciliaLib.setVar("interfaceSize", self.GetSize())
        CeciliaLib.setVar("interfacePosition", self.GetPosition())
        CeciliaLib.getVar("mainFrame").SetFocus()
        CeciliaLib.getVar("mainFrame").Hide()
        CeciliaLib.resetWidgetVariables()

        # Cleanup menubar
        self.menubar.frame = None
        self.Unbind(wx.EVT_MENU, handler=self.onUndo, id=ID_UNDO)
        self.Unbind(wx.EVT_MENU, handler=self.onRedo, id=ID_REDO)
        self.Unbind(wx.EVT_MENU, handler=self.onCopy, id=ID_COPY)
        self.Unbind(wx.EVT_MENU, handler=self.onPaste, id=ID_PASTE)
        self.Unbind(wx.EVT_MENU, handler=self.onSelectAll, id=ID_SELECT_ALL)
        self.Unbind(wx.EVT_CLOSE, handler=self.onClose)
        self.controlPanel.parent = None

        # Cleanup Grapher.plotter
        self.grapher.plotter.canvas.Unbind(wx.EVT_LEFT_DOWN, handler=self.grapher.plotter.OnMouseLeftDown)
        self.grapher.plotter.canvas.Unbind(wx.EVT_LEFT_UP, handler=self.grapher.plotter.OnMouseLeftUp)
        self.grapher.plotter.canvas.Unbind(wx.EVT_MOTION, handler=self.grapher.plotter.OnMotion)
        self.grapher.plotter.canvas.Unbind(wx.EVT_LEFT_DCLICK, handler=self.grapher.plotter.OnMouseDoubleClick)
        self.grapher.plotter.canvas.Unbind(wx.EVT_RIGHT_DOWN, handler=self.grapher.plotter.OnMouseRightDown)
        self.grapher.plotter.canvas.Unbind(wx.EVT_LEAVE_WINDOW, handler=self.grapher.plotter.OnLeave)
        self.grapher.plotter.canvas.Unbind(wx.EVT_PAINT, handler=self.grapher.plotter.OnPaint)
        self.grapher.plotter.canvas.Unbind(wx.EVT_SIZE, handler=self.grapher.plotter.OnSize)
        self.grapher.plotter.canvas.Unbind(wx.EVT_LEAVE_WINDOW, handler=self.grapher.plotter.OnLooseFocus)
        self.grapher.plotter.canvas.Unbind(wx.EVT_ENTER_WINDOW, handler=self.grapher.plotter.OnGrabFocus)
        self.grapher.plotter.canvas.Unbind(wx.EVT_CHAR, handler=self.grapher.plotter.OnKeyDown)
        self.grapher.plotter.Unbind(wx.EVT_CHAR, handler=self.grapher.plotter.OnKeyDown)
        self.grapher.plotter.Unbind(wx.EVT_SCROLL_THUMBTRACK, handler=self.grapher.plotter.OnScroll)
        self.grapher.plotter.Unbind(wx.EVT_SCROLL_PAGEUP, handler=self.grapher.plotter.OnScroll)
        self.grapher.plotter.Unbind(wx.EVT_SCROLL_PAGEDOWN, handler=self.grapher.plotter.OnScroll)
        self.grapher.plotter.Unbind(wx.EVT_SCROLL_LINEUP, handler=self.grapher.plotter.OnScroll)
        self.grapher.plotter.Unbind(wx.EVT_SCROLL_LINEDOWN, handler=self.grapher.plotter.OnScroll)
        if '__WXGTK__' in wx.PlatformInfo:
            self.grapher.plotter.canvas.Unbind(wx.EVT_WINDOW_CREATE, handler=self.grapher.plotter.doOnSize)
        self.grapher.plotter.parent = None
        self.grapher.plotter = None

        # Cleanup Grapher.toolbar
        self.grapher.toolbar.Unbind(wx.EVT_LEAVE_WINDOW, handler=self.grapher.toolbar.OnLooseFocus)
        self.grapher.toolbar.fakePanel.Unbind(wx.EVT_LEAVE_WINDOW, handler=self.grapher.toolbar.OnLooseFocus)
        self.grapher.toolbar.Unbind(wx.EVT_CHAR, handler=self.grapher.toolbar.OnKeyDown)
        self.grapher.toolbar.convertSlider.cecGrapher = None
        self.grapher.toolbar.radiotoolbox.outFunction = None
        self.grapher.toolbar.menu.outFunction = None
        self.grapher.toolbar.toolbox.outFunction = None
        self.grapher.toolbar.toolbox.parent = None
        self.grapher.toolbar.parent = None
        self.grapher.toolbar = None

        # Cleanup Grapher.cursorPanel
        self.grapher.cursorPanel.Unbind(wx.EVT_LEFT_DOWN, handler=self.grapher.cursorPanel.OnLeftDown)
        self.grapher.cursorPanel.Unbind(wx.EVT_LEAVE_WINDOW, handler=self.grapher.cursorPanel.OnLooseFocus)
        self.grapher.cursorPanel.Unbind(wx.EVT_PAINT, handler=self.grapher.cursorPanel.OnPaint)
        self.grapher.cursorPanel.parent = None
        self.grapher.cursorPanel = None

        # Cleanup PresetPanel
        self.presetPanel.presetChoice = None
        self.presetPanel.saveTool = None

        try:
            self.Destroy()
            CeciliaLib.setVar("interface", None)
        except:
            pass

    def getControlPanel(self):
        return self.controlPanel

    def onUndo(self, evt):
        self.grapher.plotter.undoRedo(1)

    def onRedo(self, event):
        self.grapher.plotter.undoRedo(-1)

    def onCopy(self, event):
        self.grapher.plotter.onCopy()

    def onPaste(self, event):
        self.grapher.plotter.onPaste()

    def onSelectAll(self, event):
        self.grapher.plotter.onSelectAll()

    def updateNchnls(self):
        self.controlPanel.updateNchnls()
