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
import os, sys, time, random
from constants import *
import CeciliaLib
import PreferencePanel 
from menubar import InterfaceMenuBar
import CeciliaInterface
from Widgets import *
from DocFrame import ManualFrame

class CeciliaMainFrame(wx.Frame):
    def __init__(self, parent, ID):        
        wx.Frame.__init__(self, parent, ID)
        self.menubar = InterfaceMenuBar(self, self)
        self.SetMenuBar(self.menubar)
        self.updateTitle()
        self.prefs = None
        self.time = 0
        self.gauge = None
        self.doc_frame = ManualFrame()
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
            CeciliaLib.getControlPanel().nonZeroTime = 0
            CeciliaLib.setVar("toDac", True)
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.SetForegroundColour("#FFFFFF")
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.Refresh()
            CeciliaLib.getControlPanel().transportButtons.setPlay(True)
            wx.CallLater(50, CeciliaLib.startCeciliaSound, True)
        else:
            CeciliaLib.stopCeciliaSound()

    def onBounceToDisk(self, event):
        CeciliaLib.getControlPanel().onBounceToDisk()

    def applyBatchProcessingFolder(self, value):
        folderName = value
        if folderName == "":
            return 
        old_file_type = CeciliaLib.getVar("audioFileType")
        cfileins = CeciliaLib.getControlPanel().getCfileinList()
        num_snds = len(cfileins[0].fileMenu.choice)
        dlg = wx.ProgressDialog("Batch processing on sound folder", "", maximum = num_snds, parent=self,
                               style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        if CeciliaLib.getVar("systemPlatform") == "win32":
            dlg.SetSize((600, 125))
        else:
            dlg.SetSize((600,100))
        count = 0
        for snd in cfileins[0].fileMenu.choice:
            cfileins[0].onSelectSound(-1, snd)
            path, dump = os.path.split(cfileins[0].filePath)
            name, ext = os.path.splitext(snd)
            if ext in [".wav", ".wave", ".WAV", ".WAVE", ".Wav", ".Wave"]:
                CeciliaLib.setVar('audioFileType', "wav")
            else:
                CeciliaLib.setVar('audioFileType', "aif")
            if not os.path.isdir(os.path.join(path, folderName)):
                os.mkdir(os.path.join(path, folderName))
            filename = os.path.join(path, folderName, "%s-%s%s" % (name, folderName, ext))
            count += 1
            (keepGoing, skip) = dlg.Update(count, "Exporting %s" % filename)
            CeciliaLib.getControlPanel().onBatchProcessing(filename)
            while (CeciliaLib.getVar("audioServer").isAudioServerRunning()):
                time.sleep(.1)
        dlg.Destroy()
        CeciliaLib.setVar('audioFileType', old_file_type)

    def applyBatchProcessingPreset(self, value):
        folderName = value
        if folderName == "":
            return
        cfileins = CeciliaLib.getControlPanel().getCfileinList()
        presets = CeciliaLib.getVar("presetPanel").getPresets()
        if "init" in presets:
            presets.remove("init")
        if "last save" in presets:
            presets.remove("last save")
        num_presets = len(presets)
        dlg = wx.ProgressDialog("Batch processing on preset sequence", "", maximum = num_presets, parent=self,
                               style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        if CeciliaLib.getVar("systemPlatform") == "win32":
            dlg.SetSize((600, 125))
        else:
            dlg.SetSize((600,100))
        count = 0
        for preset in presets:
            CeciliaLib.loadPresetFromDict(preset)
            path, fname = os.path.split(cfileins[0].filePath)
            name, ext = os.path.splitext(fname)
            if not os.path.isdir(os.path.join(path, folderName)):
                os.mkdir(os.path.join(path, folderName))
            filename = os.path.join(path, folderName, "%s-%s%s" % (name, preset, ext))
            count += 1
            (keepGoing, skip) = dlg.Update(count, "Exporting %s" % filename)
            CeciliaLib.getControlPanel().onBatchProcessing(filename)
            while (CeciliaLib.getVar("audioServer").isAudioServerRunning()):
                time.sleep(.1)
        dlg.Destroy()

    def onBatchProcessing(self, event):
        if event.GetId() == ID_BATCH_FOLDER:
            f = BatchPopupFrame(self, self.applyBatchProcessingFolder) 
        else:
            f = BatchPopupFrame(self, self.applyBatchProcessingPreset) 
        f.MakeModal(True)
        f.CenterOnScreen()
        f.Show()

    def onSelectOutputFilename(self):
        if CeciliaLib.getVar("audioFileType") == 'wav':
            wildcard = "Wave file|*.wav;*.wave;*.WAV;*.WAVE;*.Wav;*.Wave|" \
                       "All files|*.*"
        else:
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

    def newRecent(self, file, remove=False):
        filename = os.path.join(TMP_PATH,'.recent.txt')
        try:
            f = open(filename, "r")
            lines = [line[:-1] for line in f.readlines()]
            f.close()
        except:
            lines = []

        update = False
        if not remove:
            if not file in lines and not 'Resources/modules/' in file:
                lines.insert(0, file)
                update = True
        else:
            if file in lines:
                lines.remove(file)
                update = True

        if update:
            f = open(filename, "w")
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

    def onOpen(self, event, builtin=False):
        if isinstance(event, wx.CommandEvent):
            CeciliaLib.openCeciliaFile(self)
        elif os.path.isfile(event):
            CeciliaLib.openCeciliaFile(self, event, builtin)
        self.updateTitle()

    def onOpenRandom(self, event):
        categories = [folder for folder in os.listdir(MODULES_PATH) if not folder.startswith(".")]
        category = random.choice(categories)
        files = [f for f in os.listdir(os.path.join(MODULES_PATH, category)) if f.endswith(FILE_EXTENSION)]
        file = random.choice(files)
        self.onOpen(os.path.join(MODULES_PATH, category, file), True)

    def openRecent(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id).GetLabel()
        if os.path.isfile(file[:-1]):
            CeciliaLib.openCeciliaFile(self, file[:-1])
            self.updateTitle()
        else:
            CeciliaLib.showErrorDialog("Error while trying to open a file!", "No such file : %s" % file[:-1])
            self.newRecent(file[:-1], remove=True)
        
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

    def openModuleAsText(self, event):
        CeciliaLib.openCurrentFileAsText(CeciliaLib.getVar("currentCeciliaFile"))
        
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

    def onQuit(self, event):
        if not CeciliaLib.closeCeciliaFile(self):
            return
        try:
            self.prefs.onClose(event)
        except:
            pass
        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            CeciliaLib.getVar("audioServer").stop()
            time.sleep(.1)
        self.doc_frame.Destroy()
        self.closeInterface()
        CeciliaLib.writeVarToDisk()
        self.Destroy()

    def onUseMidi(self, event):
        CeciliaLib.setVar("useMidi", event.GetInt())

    def onHelpAbout(self, evt):
        Y = CeciliaLib.getVar("displaySize")[0][1]
        about = AboutPopupFrame(self, Y/5)
        about.Show()

    def onModuleAbout(self, evt):
        Y = CeciliaLib.getVar("displaySize")[0][1]
        info = CeciliaLib.getVar("currentModuleRef").__doc__
        if info == None:
            info = "No module's info yet..."
        elif "DOCSTRING PLACEHOLDER" in info or info == "":
            info = "No module's info yet..."
        f = TextPopupFrame(self, info)
        f.CenterOnScreen()
        f.Show()

    def onDocFrame(self, evt):
        self.doc_frame.Show()

    def onUndo(self, evt):
        pass

    def onRedo(self, event):
        pass

    def onCopy(self, event):
        pass

    def onPaste(self, event):
        pass
