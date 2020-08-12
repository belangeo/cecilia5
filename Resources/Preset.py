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

import wx, os
import Resources.CeciliaLib as CeciliaLib
from .constants import *
from .Widgets import *

class CECPreset(wx.Panel):
    def __init__(self, parent, id=-1, size=(-1, -1), style=wx.BORDER_SIMPLE):
        wx.Panel.__init__(self, parent, id, size=size, style=style)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parent = parent

        self.currentPreset = 'init'

        mainSizer = wx.FlexGridSizer(0, 1, 0, 0)
        mainSizer.Add(10, 1, 0)

        presetTextPanel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        presetTextPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        presetTextSizer = wx.FlexGridSizer(1, 1, 0, 0)
        presetText = wx.StaticText(presetTextPanel, -1, 'PRESETS')
        presetText.SetFont(wx.Font(SECTION_TITLE_FONT, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        presetText.SetBackgroundColour(TITLE_BACK_COLOUR)
        presetText.SetForegroundColour(SECTION_TITLE_COLOUR)
        presetTextSizer.Add(presetText, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        presetTextSizer.AddGrowableCol(0)
        presetTextPanel.SetSizer(presetTextSizer)
        mainSizer.Add(presetTextPanel, 1, wx.EXPAND, 0)

        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.presetChoice = CustomMenu(self, choice=self.orderingPresetNames(),
                                       size=(150, 20), init=self.currentPreset,
                                       outFunction=self.onPresetSelect, colour=TR_BACK_COLOUR)
        CeciliaLib.setToolTip(self.presetChoice, TT_PRESET)
        lineSizer.Add(self.presetChoice, 0, wx.ALIGN_LEFT, 1)

        lineSizer.Add(10, 1, 0)

        self.saveTool = ToolBox(self, tools=['save', 'delete'], outFunction=[self.onSavePreset, self.onDeletePreset])
        CeciliaLib.setToolTip(self.saveTool, TT_PRESET_TOOLS)
        lineSizer.Add(self.saveTool, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 2)

        mainSizer.Add(lineSizer, 0, wx.ALIGN_CENTER | wx.ALL, 7)

        mainSizer.AddGrowableCol(0)
        self.SetSizer(mainSizer)

    def cleanup(self):
        self.presetChoice.cleanup()
        self.saveTool.cleanup()

    def isPreset(self, preset):
        return os.path.isfile(os.path.join(PRESETS_PATH, CeciliaLib.getVar("currentModuleName"), preset))

    def getPresetPath(self, preset):
        return os.path.join(PRESETS_PATH, CeciliaLib.getVar("currentModuleName"), preset)

    def getPresets(self):
        return self.presetChoice.getChoice()

    def setLabel(self, label):
        if label in self.getPresets():
            self.presetChoice.setLabel(label, False)
            self.currentPreset = label

    def loadPresets(self):
        presets = self.orderingPresetNames()
        self.presetChoice.setChoice(presets, False)

    def orderingPresetNames(self):
        presets = []
        presetsDir = os.path.join(PRESETS_PATH, CeciliaLib.getVar("currentModuleName")) 
        if os.path.isdir(presetsDir):
            presets.extend(os.listdir(presetsDir))
        presets.sort()
        presets.insert(0, 'init')
        return presets

    def onPresetSelect(self, idxPreset, newPreset):
        if newPreset == 'init':
            CeciliaLib.loadPresetFromFile("init")
            self.currentPreset = "init"
        elif self.isPreset(newPreset):
            CeciliaLib.loadPresetFromFile(newPreset)
            self.currentPreset = newPreset

    def onDeletePreset(self):
        if self.isPreset(self.currentPreset):
            dlg = wx.MessageDialog(self,
                                    'Preset %s will be deleted. Are you sure?' % self.currentPreset,
                                    'Warning!', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            ok = dlg.ShowModal() != wx.ID_NO
            dlg.Destroy()

            if ok:
                os.remove(self.getPresetPath(self.currentPreset))
                self.presetChoice.setChoice(self.orderingPresetNames(), False)
                self.presetChoice.setStringSelection("")

    def onSavePreset(self):
        dlg = wx.TextEntryDialog(self, 'Enter preset name:', 'Saving Preset', self.currentPreset)

        if dlg.ShowModal() == wx.ID_OK:
            newPreset = CeciliaLib.ensureNFD(dlg.GetValue())
        else:
            newPreset = ''
        dlg.Destroy()

        if newPreset == '':
            CeciliaLib.showErrorDialog('Failed saving preset', 'You must give a name to your preset!')
            return
        if newPreset == 'init':
            CeciliaLib.showErrorDialog('Failed saving preset', '"init" is reserved. You must give another name to your preset!')
            return
        ok = True
        if newPreset in self.getPresets():
            dlg2 = wx.MessageDialog(self, 'The preset you entered already exists. Are you sure you want to overwrite it?',
                                    'Existing preset!', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            if dlg2.ShowModal() == wx.ID_NO:
                ok = False
            dlg2.Destroy()

        if ok:
            self.currentPreset = newPreset
            CeciliaLib.savePresetToFile(self.currentPreset)
            self.loadPresets()
            self.setLabel(self.currentPreset)
