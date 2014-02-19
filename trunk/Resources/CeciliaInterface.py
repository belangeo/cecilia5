# encoding: utf-8
"""
Copyright 2011 iACT, Universite de Montreal, Jean Piche, Olivier Belanger, Jean-Michel Dumas

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

import wx, os
import wx.aui
import CeciliaLib
from constants import *
from Sliders import buildHorizontalSlidersBox
from Grapher import buildGrapher
from TogglePopup import buildTogglePopupBox
import Control
import Preset
from menubar import InterfaceMenuBar

class CeciliaInterface(wx.Frame):
    if CeciliaLib.getVar("systemPlatform") == "linux2":
        style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | \
                wx.CLIP_CHILDREN | wx.WANTS_CHARS
    else:
        style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | \
                wx.NO_BORDER | wx.CLIP_CHILDREN | wx.WANTS_CHARS
    def __init__(self, parent, id=-1, title='', mainFrame=None, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=style): 
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.ceciliaMainFrame = mainFrame
        self.menubar = InterfaceMenuBar(self, self.ceciliaMainFrame)
        self.SetMenuBar(self.menubar)

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.hasScrollbar = False
        self.controlPanel = Control.CECControl(self, -1)

        togglePopupPanel, objs, tpsize = self.createTogglePopupPanel(self)        
        self.horizontalSlidersPanel, slPanelSize = self.createHorizontalSlidersPanel(self)
        self.grapher = self.createGrapher(self)
        presetPanel = Preset.CECPreset(self)
        CeciliaLib.setVar("presetPanel", presetPanel)

        self._mgr.AddPane(self.horizontalSlidersPanel, wx.aui.AuiPaneInfo().
                          Name("hslidersPanel").Caption("").
                          Bottom().Position(2).CloseButton(False).MaximizeButton(False).
                          Layer(1).MinSize(slPanelSize).CaptionVisible(False))

        self._mgr.AddPane(self.grapher, wx.aui.AuiPaneInfo().
                          Name("graphPanel").Caption("").
                          CloseButton(False).MaximizeButton(True).Center().
                          Layer(0))

        self._mgr.AddPane(presetPanel, wx.aui.AuiPaneInfo().Name("presetPanel").Fixed().
                          Left().Position(1).CloseButton(False).MaximizeButton(False).
                          Layer(2).CaptionVisible(False).BestSize((-1,60)))

        self._mgr.AddPane(togglePopupPanel, wx.aui.AuiPaneInfo().Name("togglePopup").Fixed().
                          Left().Position(2).CloseButton(False).MaximizeButton(False).
                          Layer(2).CaptionVisible(False).MaxSize(tpsize))

        self._mgr.AddPane(self.controlPanel, wx.aui.AuiPaneInfo().
                          Name("controlPanel").Left().Position(0).Fixed().
                          CloseButton(False).MaximizeButton(False).MinSize((230,-1)).
                          Layer(2).CaptionVisible(False))

        pos, size = self.positionToClientArea(CeciliaLib.getVar("interfacePosition"), CeciliaLib.getVar("interfaceSize"))

        self.SetSize(size)

        self._artProvider = wx.aui.AuiDefaultDockArt()
        self._artProvider.SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 0)
        self._artProvider.SetColour(wx.aui.AUI_DOCKART_BACKGROUND_COLOUR, BORDER_COLOUR)
        self._artProvider.SetColour(wx.aui.AUI_DOCKART_SASH_COLOUR, BORDER_COLOUR)
        self._artProvider.SetColour(wx.aui.AUI_DOCKART_BORDER_COLOUR, BORDER_COLOUR)
        self._artProvider.SetColour(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, TITLE_BACK_COLOUR)
        self._artProvider.SetColour(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR, TITLE_BACK_COLOUR)
        self._mgr.SetArtProvider(self._artProvider)
                
        # Update the frame using the manager
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        if pos == None:
            self.Center()
        else:
            self.SetPosition(pos)    

    def OnSize(self, evt):
        scrPt = {'win32': 1, 'cygwin': 1, 'linux2': 1, 'darwin': 0}
        minSz = {'win32': 250, 'cygwin': 250, 'linux2': 245, 'darwin': 245}
        platform = CeciliaLib.getVar("systemPlatform") 
        if CeciliaLib.getVar("interface") != None:
            if CeciliaLib.getControlPanel().GetScrollRange(wx.VERTICAL) <= scrPt[platform]:
                hasScrollbar = False
                self._mgr.GetPane('controlPanel').MinSize((230,-1))
            else:
                hasScrollbar = True
                self._mgr.GetPane('controlPanel').MinSize((minSz[platform],-1))

            if self.hasScrollbar != hasScrollbar:
                self.hasScrollbar = hasScrollbar

            wx.CallAfter(self._mgr.Update)
        evt.Skip()

    def positionToClientArea(self, pos, size):
        position = None
        screen = 0
        if pos != None:
            for i in range(CeciliaLib.getVar("numDisplays")):
                off = CeciliaLib.getVar("displayOffset")[i]
                dispsize = CeciliaLib.getVar("displaySize")[i]
                Xbounds = [off[0], dispsize[0]+off[0]]
                Ybounds = [off[1], dispsize[1]+off[1]]
                if pos[0] >= Xbounds[0] and pos[0] <= Xbounds[1] and pos[1] >= Ybounds[0] and pos[1] <= Ybounds[1]:
                    position = pos
                    screen = i
                    break
        dispsize = CeciliaLib.getVar("displaySize")[screen]
        if size[0] <= dispsize[0] and size[1] <= dispsize[1]:
            newsize = size
        else:
            newsize = (dispsize[0]-50, dispsize[1]-50)
        return position, newsize        
                 
    def updateTitle(self, title):
        self.SetTitle(title)

    def createTogglePopupPanel(self, parent, label='', size=(-1,-1), style=wx.SUNKEN_BORDER):
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box, objs = buildTogglePopupBox(panel, CeciliaLib.getVar("interfaceWidgets"))
        panel.SetSizerAndFit(box)
        CeciliaLib.setVar("userTogglePopups", objs)
        size = panel.GetSize()
        return panel, objs, size

    def createHorizontalSlidersPanel(self, parent, label='', size=(-1,-1), 
                                     style=wx.SUNKEN_BORDER, name=''):
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(BACKGROUND_COLOUR)
        box, sl = buildHorizontalSlidersBox(panel, CeciliaLib.getVar("interfaceWidgets"))
        CeciliaLib.setVar("userSliders", sl)
        panel.SetSizerAndFit(box)
        #panel.Bind(wx.EVT_SIZE, self.onChangeSlidersPanelSize)
        size = panel.GetSize()
        return panel, size

    def onChangeSlidersPanelSize(self, evt):
        self.horizontalSlidersPanel.Layout()
        self.horizontalSlidersPanel.Refresh()
        
    def createGrapher(self, parent, label='', size=(-1,-1), style=wx.SUNKEN_BORDER):
        graph = buildGrapher(self, CeciliaLib.getVar("interfaceWidgets"), CeciliaLib.getVar("totalTime"))
        CeciliaLib.setVar("grapher", graph)
        return graph

    def onClose(self, event):
        CeciliaLib.setVar("interfaceSize", self.GetSize())
        CeciliaLib.setVar("interfacePosition", self.GetPosition())
        CeciliaLib.resetWidgetVariables()
        try:
            self._mgr.UnInit()
            self.Destroy()
        except:
            pass
        CeciliaLib.getVar("mainFrame").SetFocus()
        CeciliaLib.getVar("mainFrame").Hide()
        
    def getControlPanel(self):
        return self.controlPanel
    
    def updateManager(self):
        self._mgr.Update()
    
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
