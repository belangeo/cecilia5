# -*- coding: utf-8 -*-

import wx, os
from constants import *
import CeciliaLib
from Widgets import *

class CECPreset(wx.Panel):
    def __init__(self, parent, id=-1, size=(-1,-1), style = wx.NO_BORDER):
        wx.Panel.__init__(self, parent, id, size=size, style=style)
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.parent = parent
        
        self.currentPreset = 'init'
        
        mainSizer = wx.FlexGridSizer(2,1)
        mainSizer.AddSpacer((10,1))
        
        presetTextPanel = wx.Panel(self, -1, style=wx.NO_BORDER)
        presetTextPanel.SetBackgroundColour(TITLE_BACK_COLOUR)
        presetTextSizer = wx.FlexGridSizer(1,1)
        presetText = wx.StaticText(presetTextPanel, -1, 'PRESETS')
        presetText.SetFont(wx.Font(SECTION_TITLE_FONT, wx.NORMAL, wx.NORMAL, wx.BOLD, face=FONT_FACE))
        presetText.SetBackgroundColour(TITLE_BACK_COLOUR)
        presetText.SetForegroundColour(SECTION_TITLE_COLOUR)
        presetTextSizer.Add(presetText, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        presetTextSizer.AddGrowableCol(0)
        presetTextPanel.SetSizer(presetTextSizer)
        mainSizer.Add(presetTextPanel, 1, wx.EXPAND| wx.ALIGN_RIGHT | wx.ALL, 0)
        
        lineSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.presetChoice = CustomMenu(self,
                                       choice=self.orderingPresetNames(),
                                       size=(150,20),
                                       init=self.currentPreset,
                                       outFunction=self.onPresetSelect,
                                       colour="#6F7F97")
        self.presetChoice.SetToolTip(CECTooltip(TT_PRESET))                               
        lineSizer.Add(self.presetChoice, 0, wx.ALIGN_LEFT | wx.TOP, 1)
        
        lineSizer.AddSpacer((10,1))
        
        saveTool = ToolBox(self, tools=['save', 'delete'],
                           outFunction = [self.onSavePreset, self.onDeletePreset])
        lineSizer.Add(saveTool, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 2)
        
        mainSizer.Add(lineSizer, 0, wx.ALIGN_CENTER | wx.ALL, 7)
        mainSizer.AddGrowableCol(0)
        self.SetSizer(mainSizer)

    def setLabel(self, label):
        if label in CeciliaLib.getVar("presets").keys():
            self.presetChoice.setLabel(label, False)

    def loadPresets(self):
        presets = self.orderingPresetNames()
        self.presetChoice.setChoice(presets, False)
        
    def orderingPresetNames(self):
        presets = CeciliaLib.getVar("presets").keys()
        presets.sort()
        presets.insert(0,'init')
        return presets
    
    def onPresetSelect(self, idxPreset, newPreset):
        if CeciliaLib.getVar("presets").has_key(newPreset):
            if newPreset != 'init':
                CeciliaLib.loadPresetFromDict(newPreset)
                for preset in CeciliaLib.getVar("presets"):
                    if preset != newPreset:
                        CeciliaLib.getVar("presets")[preset]['active'] = False
                CeciliaLib.getVar("presets")[newPreset]['active'] = True
                self.currentPreset = newPreset
        elif newPreset == 'init':
            CeciliaLib.getVar("mainFrame").onUpdateInterface(wx.MenuEvent())
                
    def onDeletePreset(self):
        if CeciliaLib.getVar("presets").has_key(self.currentPreset):
            dlg2 = wx.MessageDialog(self, 'Preset %s will be deleted. Are you sure?' % self.currentPreset,
                               'Warning!',
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            if dlg2.ShowModal() == wx.ID_NO: ok = False
            else: ok = True
            dlg2.Destroy()
            
            if ok:
                CeciliaLib.deletePreset(self.currentPreset)
                self.presetChoice.setChoice(self.orderingPresetNames(), False)
                self.presetChoice.setStringSelection("")
                
    def onSavePreset(self):
        dlg = wx.TextEntryDialog(self, 'Enter preset name:','Saving Preset', self.currentPreset)
        
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
                               'Existing preset!',
                               wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
            if dlg2.ShowModal() == wx.ID_NO: 
                return
            dlg2.Destroy()    
 
        self.currentPreset = newPreset
        CeciliaLib.savePresetToDict(self.currentPreset)
        self.presetChoice.setChoice(self.orderingPresetNames(), False)
        self.presetChoice.setStringSelection(self.currentPreset)
