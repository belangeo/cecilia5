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

        from . import ChainUI
        ChainUI.initialize(self)

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

    def createTogglePopupPanel(self, parent=None):
        panel = wx.Panel(parent or self, -1, style=wx.BORDER_SIMPLE)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        widgets = CeciliaLib.getVar("interfaceWidgets")
        box, objs = buildTogglePopupBox(panel, widgets)
        panel.SetSizerAndFit(box)
        CeciliaLib.setVar("userTogglePopups", objs)
        size = panel.GetSize()
        return panel, objs, size

    def createSlidersPanel(self, parent=None):
        panel = wx.Panel(parent or self, -1, style=wx.BORDER_SIMPLE)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        widgets = CeciliaLib.getVar("interfaceWidgets")
        box, sl = buildHorizontalSlidersBox(panel, widgets)
        CeciliaLib.setVar("userSliders", sl)
        panel.SetSizerAndFit(box)
        size = panel.GetSize()
        return panel, size

    def onClose(self, event):
        # The interface is the session window. Closing it follows normal quit.
        self.ceciliaMainFrame.onQuit(event)

    def destroySessionWindow(self):
        from . import ChainUI
        CeciliaLib.setVar("interfaceSize", self.GetSize())
        CeciliaLib.setVar("interfacePosition", self.GetPosition())
        ChainUI.destroy_editors(self)
        self.Destroy()
        CeciliaLib.setVar("interface", None)

    def getControlPanel(self):
        return self.controlPanel

    def onUndo(self, evt):
        if self.grapher is not None:
            self.grapher.plotter.undoRedo(1)

    def onRedo(self, event):
        if self.grapher is not None:
            self.grapher.plotter.undoRedo(-1)

    def onCopy(self, event):
        if self.grapher is not None:
            self.grapher.plotter.onCopy()

    def onPaste(self, event):
        if self.grapher is not None:
            self.grapher.plotter.onPaste()

    def onSelectAll(self, event):
        if self.grapher is not None:
            self.grapher.plotter.onSelectAll()

    def updateNchnls(self):
        self.controlPanel.updateNchnls()
