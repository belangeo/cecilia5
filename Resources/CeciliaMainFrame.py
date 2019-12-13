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

import os, time, random
import wx
from .constants import *
import Resources.CeciliaLib as CeciliaLib
import Resources.PreferencePanel as PreferencePanel
import Resources.CeciliaInterface as CeciliaInterface
from .menubar import InterfaceMenuBar
from .Widgets import *
from .DocFrame import ManualFrame

class CeciliaMainFrame(wx.Frame):
    def __init__(self, parent, ID):
        wx.Frame.__init__(self, parent, ID)
        self.menubar = InterfaceMenuBar(self, self)
        self.SetMenuBar(self.menubar)
        self.prefs = None
        self.time = 0
        self.api_doc_frame = ManualFrame(kind="api")
        self.mod_doc_frame = ManualFrame(kind="modules")

    def setTime(self, curTime=0):
        self.time = curTime

    def updateTitle(self):
        title = os.path.split(CeciliaLib.getVar("currentCeciliaFile", unicode=True))[1]
        if CeciliaLib.getVar("interface"):
            CeciliaLib.getVar("interface").updateTitle('Cecilia5 - ' + title)

    def onShortPlayStop(self, event):
        self.onPlayStop(not CeciliaLib.getVar("audioServer").isAudioServerRunning())

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
        dlg = wx.ProgressDialog("Batch processing on sound folder", "", maximum=num_snds, parent=self,
                               style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        dlg.SetMinSize((600, -1))
        dlg.SetClientSize((600, 100))
        count = 0
        totaltime = CeciliaLib.getVar("totalTime")
        for snd in cfileins[0].fileMenu.choice:
            cfileins[0].onSelectSound(-1, snd)
            if CeciliaLib.getVar("useSoundDur"):
                cfileins[0].setTotalTime()
            path = os.path.split(cfileins[0].filePath)[0]
            name, ext = os.path.splitext(snd)
            lext = ext.lower()
            if lext in [".wav", ".wave"]:
                CeciliaLib.setVar('audioFileType', "wav")
            elif lext in [".aif", ".aiff", ".aifc"]:
                CeciliaLib.setVar('audioFileType', "aif")
            elif lext in [".ogg"]:
                CeciliaLib.setVar('audioFileType', "ogg")
            elif lext in [".flac"]:
                CeciliaLib.setVar('audioFileType', "flac")
            elif lext in [".au"]:
                CeciliaLib.setVar('audioFileType', "au")
            elif lext in [".sd2"]:
                CeciliaLib.setVar('audioFileType', "sd2")
            elif lext in [".caf"]:
                CeciliaLib.setVar('audioFileType', "caf")
            if not os.path.isdir(os.path.join(path, folderName)):
                os.mkdir(os.path.join(path, folderName))
            filename = os.path.join(path, folderName, "%s-%s%s" % (name, folderName, ext))
            count += 1
            (keepGoing, skip) = dlg.Update(count, "Exporting %s" % filename)
            CeciliaLib.getControlPanel().onBatchProcessing(filename)
            while (CeciliaLib.getVar("audioServer").isAudioServerRunning()):
                time.sleep(.1)
        if CeciliaLib.getVar("useSoundDur"):
            CeciliaLib.getControlPanel().setTotalTime(totaltime)
            CeciliaLib.getControlPanel().updateDurationSlider()

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
        dlg = wx.ProgressDialog("Batch processing on preset sequence",
                                "", maximum=num_presets, parent=self,
                                style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        dlg.SetMinSize((600, -1))
        dlg.SetClientSize((600, 100))
        if len(cfileins) > 0:
            filepath = cfileins[0].filePath
        count = 0
        for preset in presets:
            CeciliaLib.loadPresetFromFile(preset)
            if len(cfileins) == 0:
                path = os.path.join(os.path.expanduser("~"), "Desktop")
                name = "batch"
                ext = "." + CeciliaLib.getVar("audioFileType")
            else:
                cfileins[0].onLoadFile(filepath)
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
        f.CenterOnScreen()
        f.Show()

    def onUseSoundDuration(self, evt):
        CeciliaLib.setVar("useSoundDur", evt.GetInt())

    def onSelectOutputFilename(self):
        file = CeciliaLib.saveFileDialog(self, AUDIO_FILE_WILDCARD, type='Save audio')
        if file is not None:
            CeciliaLib.setVar("saveAudioFilePath", os.path.split(file)[0])
        return file

    def closeInterface(self):
        if CeciliaLib.getVar("interface") is not None:
            CeciliaLib.getVar("interface").onClose(None)
            CeciliaLib.setVar("interface", None)

    def newRecent(self, file, remove=False):
        if ".cecilia5" in file:
            return

        file = CeciliaLib.ensureNFD(file)
        filename = os.path.join(TMP_PATH, '.recent.txt')
        try:
            f = open(filename, "r")
            lines = [CeciliaLib.ensureNFD(line[:-1]) for line in f.readlines()]
            f.close()
        except:
            lines = []

        update = False
        if not remove:
            if file not in lines and 'Resources/modules/' not in file:
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
                self.menubar.openRecentMenu.Delete(item)
            for file in recentFiles:
                try:
                    self.menubar.openRecentMenu.Append(subId2, file)
                    subId2 += 1
                except:
                    pass

    def onOpen(self, event, builtin=False):
        if isinstance(event, wx.CommandEvent):
            CeciliaLib.openCeciliaFile(self)
        elif os.path.isfile(event):
            CeciliaLib.openCeciliaFile(self, event, builtin)

    def onOpenRandom(self, event):
        categories = [folder for folder in os.listdir(MODULES_PATH) if not folder.startswith(".")]
        category = random.choice(categories)
        files = [f for f in os.listdir(os.path.join(MODULES_PATH, category)) if f.endswith(FILE_EXTENSION)]
        file = random.choice(files)
        self.onOpen(os.path.join(MODULES_PATH, category, file), True)

    def openRecent(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id).GetLabel().replace("\n", "").strip()
        if os.path.isfile(file):
            CeciliaLib.openCeciliaFile(self, file)
        else:
            CeciliaLib.showErrorDialog("Error while trying to open a file!", "No such file : %s" % file[:-1])
            self.newRecent(file, remove=True)

    def onOpenBuiltin(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id)
        filename = file.GetLabel() # TODO: replace MenuItem.GetLabel --- deprecated.
        filedict = self.GetMenuBar().files
        for key in filedict.keys():
            if filename in filedict[key]:
                dirname = key
                break
        name = os.path.join(CeciliaLib.ensureNFD(MODULES_PATH), dirname, filename)
        CeciliaLib.openCeciliaFile(self, name, True)

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

    def openModuleAsText(self, event):
        CeciliaLib.openCurrentFileAsText(CeciliaLib.getVar("currentCeciliaFile"))

    def reloadCurrentModule(self, event):
        CeciliaLib.openCeciliaFile(self, CeciliaLib.getVar("currentCeciliaFile"))

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
        CeciliaLib.getVar("interface").menubar.editMenu.FindItemById(ID_REMEMBER).Check(event.GetInt())
        CeciliaLib.setVar("rememberedSound", event.GetInt())
        return

    def onUpdateInterface(self, event):
        if event is not None:
            snds = []
            if CeciliaLib.getVar("rememberedSound"):
                for key in CeciliaLib.getVar("userInputs").keys():
                    if CeciliaLib.getVar("userInputs")[key]['path'] != '':
                        snds.append(CeciliaLib.getVar("userInputs")[key]['path'])
        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            CeciliaLib.stopCeciliaSound()
        self.closeInterface()
        CeciliaLib.parseInterfaceText()
        title = os.path.split(CeciliaLib.getVar("currentCeciliaFile", unicode=True))[1]
        ceciliaInterface = CeciliaInterface.CeciliaInterface(None, title='Interface - %s' % title, mainFrame=self)
        ceciliaInterface.SetSize(CeciliaLib.getVar("interfaceSize"))
        ceciliaInterface.SetPosition(CeciliaLib.getVar("interfacePosition"))
        CeciliaLib.setVar("interface", ceciliaInterface)
        CeciliaLib.getVar("presetPanel").loadPresets()
        if event is not None:
            for i, cfilein in enumerate(CeciliaLib.getControlPanel().getCfileinList()):
                if i >= len(snds):
                    break
                cfilein.onLoadFile(snds[i])

    def onShowSpectrum(self, event):
        CeciliaLib.setVar('showSpectrum', event.GetInt())

    def openSpectrumWindow(self):
        if CeciliaLib.getVar('spectrumFrame') is None:
            f = SpectrumFrame(CeciliaLib.getVar("interface"))
            f.setAnalyzer(CeciliaLib.getVar("audioServer").spectrum)
            f.Center()
            f.Show()
            CeciliaLib.setVar('spectrumFrame', f)

    def onQuit(self, event):
        reallyQuit = False
        msg = "Do you really want to quit Cecilia ?"
        dlg = wx.MessageDialog(self, msg, "Quit Cecilia5...", style=wx.YES_NO | wx.STAY_ON_TOP)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            reallyQuit = True
        dlg.Destroy()

        if not reallyQuit:
            return

        try:
            self.prefs.onClose(event)
        except:
            pass

        if CeciliaLib.getVar("audioServer").isAudioServerRunning():
            CeciliaLib.getVar("audioServer").stop()
            time.sleep(.2)

        if CeciliaLib.getVar('spectrumFrame') is not None:
            try:
                CeciliaLib.getVar('spectrumFrame')._destroy(None)
            except:
                pass
            finally:
                CeciliaLib.setVar('spectrumFrame', None)

        self.api_doc_frame.Destroy()
        self.mod_doc_frame.Destroy()
        CeciliaLib.closeCeciliaFile(self)
        CeciliaLib.writeVarToDisk()
        self.Destroy()

    def onUseMidi(self, event):
        CeciliaLib.setVar("useMidi", event.GetInt())

    def onHelpAbout(self, evt):
        Y = CeciliaLib.getVar("displaySize")[0][1]
        about = AboutPopupFrame(self, Y // 5)
        about.Show()

    def onModuleAbout(self, evt):
        file = os.path.split(CeciliaLib.getVar("currentCeciliaFile"))[1]
        self.mod_doc_frame.Center()
        self.mod_doc_frame.openPage(file)

    def onDocFrame(self, evt):
        self.api_doc_frame.Center()
        self.api_doc_frame.Show()

    def onGraphFrame(self, evt):
        self.graph_doc_frame = wx.MessageDialog(self, TT_GRAPHER)
        self.graph_doc_frame.ShowModal()
        self.graph_doc_frame.Destroy()
