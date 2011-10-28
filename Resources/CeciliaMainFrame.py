#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright 2009 iACT, universite de Montreal, Jean Piche, Olivier Belanger, Dominic Thibault

This file is part of Cecilia 4.

Cecilia 4 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Cecilia 4 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Cecilia 4.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx
import os, sys, time
from constants import *
import CeciliaLib
import PreferencePanel 
from menubar import InterfaceMenuBar
import CeciliaInterface
from Widgets import *

class CeciliaMainFrame(wx.Frame):
    def __init__(self, parent, ID):        
        wx.Frame.__init__(self, parent, ID)
        self.menubar = InterfaceMenuBar(self, self)
        self.SetMenuBar(self.menubar)
        self.updateTitle()
        self.prefs = None
        self.time = 0
        self.interfacePosition = wx.DefaultPosition
        self.interfaceSize = wx.DefaultSize

    def setTime(self,curTime=0):
        self.time = curTime

    def updateTitle(self, isModified=False):
        if CeciliaLib.getVar("builtinModule"):
            file = os.path.split(CeciliaLib.getVar("currentCeciliaFile", unicode=True))[1]
        else:
            file = CeciliaLib.getVar("currentCeciliaFile", unicode=True)
        title = os.path.split(CeciliaLib.getVar("currentCeciliaFile", unicode=True))[1]  
        if not isModified:
            if CeciliaLib.getVar("interface"):
                CeciliaLib.getVar("interface").updateTitle('Interface - ' + title)
        else:
            if CeciliaLib.getVar("interface"):
                CeciliaLib.getVar("interface").updateTitle('*** Interface - ' + title + ' ***')

    def onShortPlayStop(self, event):
        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            self.onPlayStop(0)
        else:
            self.onPlayStop(1)
                
    def onPlayStop(self, value):
        if value:
            CeciliaLib.setVar("outputFile", "dac")
            CeciliaLib.startCeciliaSound()
            CeciliaLib.getControlPanel().transportButtons.setPlay(True)      
        else:
            CeciliaLib.stopCeciliaSound()
        
    def onRec(self, value):
        if value:
            filename = self.onSelectOutputFilename()
            if filename == None:
                CeciliaLib.stopCeciliaSound()
                CeciliaLib.getControlPanel().transportButtons.setRecord(False)      
                CeciliaLib.getControlPanel().transportButtons.setPlay(False)      
            else:
                CeciliaLib.setVar("outputFile", filename)
                CeciliaLib.startCeciliaSound()  
                CeciliaLib.getControlPanel().transportButtons.setRecord(True)      
                CeciliaLib.getControlPanel().transportButtons.setPlay(True)      
        else:
            CeciliaLib.stopCeciliaSound()

    def onSelectOutputFilename(self):
        if CeciliaLib.getVar("audioFileType") == 'wav':
            wildcard = "Wave file|*.wav;*.wave;*.WAV;*.WAVE;*.Wav;*.Wave|" \
                       "All files|*.*"
        elif CeciliaLib.getVar("audioFileType") == 'aiff':
            wildcard = "AIFF file|*.aif;*.aiff;*.aifc;*.AIF;*.AIFF;*.Aif;*.Aiff|" \
                       "All files|*.*"
        
        file = CeciliaLib.saveFileDialog(self, wildcard, type='Save audio')
        if file != None:
            CeciliaLib.setVar("saveAudioFilePath", os.path.split(file)[0])
        return file

    def closeInterface(self):
        if CeciliaLib.getVar("interface"):
            self.interfaceSize = CeciliaLib.getVar("interface").GetSize()
            self.interfacePosition = CeciliaLib.getVar("interface").GetPosition()
            CeciliaLib.getVar("interface").onClose(None)
            CeciliaLib.setVar("interface", None)

    def newRecent(self, file):
        filename = os.path.join(TMP_PATH,'.recent.txt')
        try:
            f = open(filename, "r")
            lines = [line[:-1] for line in f.readlines()]
            f.close()
        except:
            lines = []
        if not file in lines and not 'Resources/modules/' in file:
            f = open(filename, "w")
            lines.insert(0, file)
            if len(lines) > 10:
                lines = lines[0:10]
            for line in lines:
                f.write(line + '\n')
            f.close()    

        subId2 = ID_OPEN_RECENT
        recentFiles = []
        f = open(filename, "r")
        for line in f.readlines():
            recentFiles.append(line)
        f.close()    
        if recentFiles:
            for item in self.menubar.openRecentMenu.GetMenuItems():
                self.menubar.openRecentMenu.DeleteItem(item)
            for file in recentFiles:
                self.menubar.openRecentMenu.Append(subId2, file)
                subId2 += 1

    def onOpen(self, event):
        if isinstance(event, wx.CommandEvent):
            CeciliaLib.openCeciliaFile(self)
        elif os.path.isfile(event):
            CeciliaLib.openCeciliaFile(self, event)
        self.updateTitle()

    def openRecent(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id).GetLabel()
        CeciliaLib.openCeciliaFile(self, file[:-1])
        self.updateTitle()
        
    def onOpenBuiltin(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id)
        filename = file.GetLabel()
        filedict = self.GetMenuBar().files
        for key in filedict.keys():
            if filename in filedict[key]:
                dirname = key
                break
        name = os.path.join(MODULES_PATH, dirname, filename)
        CeciliaLib.openCeciliaFile(self, name, True)
        self.updateTitle()

    def onOpenPrefModule(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id)
        filename = file.GetLabel()
        filedir = file.GetMenu().GetTitle()
        prefPath = CeciliaLib.getVar("prefferedPath")
        prefPaths = prefPath.split(';')
        prefBaseNames = [os.path.basename(path) for path in prefPaths]
        dirname = prefPaths[prefBaseNames.index(filedir)]
        if dirname:
            name = os.path.join(dirname, filename)
            CeciliaLib.openCeciliaFile(self, name)
            self.updateTitle()

    def reloadCurrentModule(self, event):
        CeciliaLib.openCeciliaFile(self, CeciliaLib.getVar("currentCeciliaFile"))
        self.updateTitle()

    def onSave(self, event):
        CeciliaLib.saveCeciliaFile(self, showDialog=False)
        self.updateTitle()

    def onSaveAs(self, event):
        CeciliaLib.saveCeciliaFile(self)
        self.updateTitle()

    def onPreferences(self, event):
        self.prefs = PreferencePanel.PreferenceFrame(self)
        self.prefs.Show()
        self.prefs.Center()

    def onRememberInputSound(self, event):
        if event.GetInt() == 1:
            CeciliaLib.getVar("interface").menubar.editMenu.FindItemById(ID_REMEMBER).Check(True)
            CeciliaLib.setVar("rememberedSound", True)
        else:
            CeciliaLib.getVar("interface").menubar.editMenu.FindItemById(ID_REMEMBER).Check(False)
            CeciliaLib.setVar("rememberedSound", False)

    def onUpdateInterface(self, event):
        if event != None:
            snds = []
            if CeciliaLib.getVar("rememberedSound"):
                for key in CeciliaLib.getVar("userInputs").keys():
                    if CeciliaLib.getVar("userInputs")[key]['path'] != '':
                        snds.append(CeciliaLib.getVar("userInputs")[key]['path'])
        self.closeInterface()
        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            CeciliaLib.stopCeciliaSound()
        CeciliaLib.parseInterfaceText()
        title = os.path.split(CeciliaLib.getVar("currentCeciliaFile", unicode=True))[1]
        ceciliaInterface = CeciliaInterface.CeciliaInterface(None, title='Interface - %s' % title, mainFrame=self)
        ceciliaInterface.SetSize(self.interfaceSize)
        ceciliaInterface.SetPosition(self.interfacePosition)
        ceciliaInterface.Show(True)
        CeciliaLib.setVar("interface", ceciliaInterface)
        if CeciliaLib.getVar("presets") != {}:
            CeciliaLib.getVar("presetPanel").loadPresets()
        if event != None:
            for i, cfilein in enumerate(CeciliaLib.getControlPanel().getCfileinList()):
                if i >= len(snds):
                    break
                cfilein.onLoadFile(snds[i])
        wx.CallAfter(ceciliaInterface.OnSize, wx.PaintEvent(wx.ID_ANY))

    def openManUseCecilia(self, event):
        self.manView = ManualPage(self, page=os.path.join(CEC_MAN_PATH, "usingCecilia.html"))
        self.manView.Show()
 
    def openManBuildCecilia(self, event):
        self.manView = ManualPage(self, page=os.path.join(CEC_MAN_PATH, "buildInterface.html"))
        self.manView.Show()

    def onQuit(self, event):
        if not CeciliaLib.closeCeciliaFile(self):
            return
        try:
            self.prefs.onClose(event)
        except:
            pass
        CeciliaLib.getVar("audioServer").stop()
        self.closeInterface()
        CeciliaLib.writeVarToDisk()
        self.Destroy()
        sys.exit()

    def onUseMidi(self, event):
        CeciliaLib.setVar("useMidi", event.GetInt())

    def onHelpAbout(self, evt):
        Y = CeciliaLib.getVar("displaySize")[0][1]
        about = AboutPopupFrame(self, Y/5)
        about.Show()

    def onUndo(self, evt):
        pass

    def onRedo(self, event):
        pass

    def onCopy(self, event):
        pass

    def onPaste(self, event):
        pass

class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    
    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            if os.path.isfile(file):    
                CeciliaLib.openCeciliaFile(self.window, file)
            else:
                pass
