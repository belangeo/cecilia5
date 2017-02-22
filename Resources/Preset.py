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

import wx
import Resources.CeciliaLib as CeciliaLib
from .constants import *
from .Widgets import *

class CECPreset(wx.Panel):
    if CeciliaLib.getVar("systemPlatform") == "win32":
        BORDER = wx.DOUBLE_BORDER
    else:
        BORDER = wx.SIMPLE_BORDER
    def __init__(self, parent, id=-1, size=(-1, -1), style=BORDER):
        wx.Panel.__init__(self, parent, id, size=size, style=style)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parent = parent

        self.currentPreset = 'init'

        mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        mainSizer.Add(10, 1, 0)

        presetTextPanel = wx.Panel(self, -1, style=wx.NO_BORDER)
        presetTextPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        presetTextSizer = wx.FlexGridSizer(1, 1, 0, 0)
        presetText = wx.StaticText(presetTextPanel, -1, 'PRESETS')
        presetText.SetFont(wx.Font(SECTION_TITLE_FONT, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName=FONT_FACE))
        presetText.SetBackgroundColour(TITLE_BACK_COLOUR)
        presetText.SetForegroundColour(SECTION_TITLE_COLOUR)
        presetTextSizer.Add(presetText, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        presetTextSizer.AddGrowableCol(0)
        presetTextPanel.SetSizer(presetTextSizer)
        mainSizer.Add(presetTextPanel, 1, wx.EXPAND | wx.ALIGN_RIGHT | wx.ALL, 0)

        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.presetChoice = CustomMenu(self, choice=self.orderingPresetNames(),
                                       size=(150, 20), init=self.currentPreset,
                                       outFunction=self.onPresetSelect, colour=TR_BACK_COLOUR)
        self.presetChoice.SetToolTip(CECTooltip(TT_PRESET))
        lineSizer.Add(self.presetChoice, 0, wx.ALIGN_LEFT, 1)

        lineSizer.Add(10, 1, 0)

        saveTool = ToolBox(self, tools=['save', 'delete'], outFunction=[self.onSavePreset, self.onDeletePreset])
        lineSizer.Add(saveTool, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 2)

        mainSizer.Add(lineSizer, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 7)

        mainSizer.AddGrowableCol(0)
        self.SetSizer(mainSizer)

    def getPresets(self):
        return self.presetChoice.getChoice()

    def setLabel(self, label):
        if label in CeciliaLib.getVar("presets").keys():
            self.presetChoice.setLabel(label, False)

    def loadPresets(self):
        presets = self.orderingPresetNames()
        self.presetChoice.setChoice(presets, False)

    def orderingPresetNames(self):
        presets = list(CeciliaLib.getVar("presets").keys())
        presets.sort()
        presets.insert(0, 'init')
        return presets

    def onPresetSelect(self, idxPreset, newPreset):
        if newPreset in CeciliaLib.getVar("presets"):
            CeciliaLib.loadPresetFromDict(newPreset)
            for preset in CeciliaLib.getVar("presets"):
                if preset != newPreset:
                    CeciliaLib.getVar("presets")[preset]['active'] = False
            CeciliaLib.getVar("presets")[newPreset]['active'] = True
            self.currentPreset = newPreset
        elif newPreset == 'init':
            CeciliaLib.loadPresetFromDict("init")
            for preset in CeciliaLib.getVar("presets"):
                CeciliaLib.getVar("presets")[preset]['active'] = False
            self.currentPreset = "init"

    def onDeletePreset(self):
        if self.currentPreset in CeciliaLib.getVar("presets"):
            dlg2 = wx.MessageDialog(self,
                                    'Preset %s will be deleted. Are you sure?' % self.currentPreset,
                                    'Warning!', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            if dlg2.ShowModal() == wx.ID_NO: ok = False
            else: ok = True
            dlg2.Destroy()

            if ok:
                CeciliaLib.deletePreset(self.currentPreset)
                self.presetChoice.setChoice(self.orderingPresetNames(), False)
                self.presetChoice.setStringSelection("")

    def onSavePreset(self):
        dlg = wx.TextEntryDialog(self, 'Enter preset name:', 'Saving Preset', self.currentPreset)

        if dlg.ShowModal() == wx.ID_OK:
            newPreset = CeciliaLib.ensureNFD(dlg.GetValue())
        else:
            return
        dlg.Destroy()

        if newPreset == '':
            CeciliaLib.showErrorDialog('Failed saving preset', 'You must give a name to your preset!')
            return
        if newPreset == 'init':
            CeciliaLib.showErrorDialog('Failed saving preset', '"init" is reserved. You must give another name to your preset!')
            return
        if newPreset in CeciliaLib.getVar("presets").keys():
            dlg2 = wx.MessageDialog(self, 'The preset you entered already exists. Are you sure you want to overwrite it?',
                               'Existing preset!', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            if dlg2.ShowModal() == wx.ID_NO:
                return
            dlg2.Destroy()

        self.currentPreset = newPreset
        CeciliaLib.savePresetToDict(self.currentPreset)
        self.presetChoice.setChoice(self.orderingPresetNames(), False)
        self.presetChoice.setStringSelection(self.currentPreset)