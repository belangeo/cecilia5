# encoding: utf-8
"""
Copyright 2011 iACT, Universite de Montreal, Jean Piche, Olivier Belanger,
Jean-Michel Dumas

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
    if CeciliaLib.getVar("systemPlatform") == "linux2":
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
        presetPanel = Preset.CECPreset(self)
        CeciliaLib.setVar("presetPanel", presetPanel)

        self.controlBox.Add(self.controlPanel, 1, wx.EXPAND | wx.RIGHT, -1)
        self.controlBox.Add(presetPanel, 0, wx.EXPAND | wx.TOP | wx.RIGHT, -1)
        self.controlBox.Add(togglePopupPanel, 0, wx.EXPAND | wx.TOP | wx.RIGHT, -1)

        self.box.Add(self.controlBox, (0, 0), span=(2, 1), flag=wx.EXPAND)
        self.box.Add(self.grapher, (0, 1), flag=wx.EXPAND)
        self.box.Add(slidersPanel, (1, 1), flag=wx.EXPAND|wx.TOP, border=-1)

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

        self.Show(True)

        wx.CallLater(200, buildGrapher, self.grapher)

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

    def createTogglePopupPanel(self):
        if CeciliaLib.getVar("systemPlatform") == "win32":
            BORDER = wx.DOUBLE_BORDER
        else:
            BORDER = wx.SIMPLE_BORDER
        panel = wx.Panel(self, -1, style=BORDER)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        widgets = CeciliaLib.getVar("interfaceWidgets")
        box, objs = buildTogglePopupBox(panel, widgets)
        panel.SetSizerAndFit(box)
        CeciliaLib.setVar("userTogglePopups", objs)
        size = panel.GetSize()
        return panel, objs, size

    def createSlidersPanel(self):
        if CeciliaLib.getVar("systemPlatform") == "win32":
            BORDER = wx.DOUBLE_BORDER
        else:
            BORDER = wx.SIMPLE_BORDER
        panel = wx.Panel(self, -1, style=BORDER)
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
        CeciliaLib.resetWidgetVariables()
        try:
            self.Destroy()
        except:
            pass
        CeciliaLib.getVar("mainFrame").SetFocus()
        CeciliaLib.getVar("mainFrame").Hide()

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