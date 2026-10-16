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
        if CeciliaLib.getVar('interface'):
            from .ChainUI import update_title
            update_title(CeciliaLib.getVar('interface'))

    def onShortPlayStop(self, event):
        self.onPlayStop(not CeciliaLib.getVar("audioServer").isAudioServerRunning())

    def onPlayStop(self, value):
        if value:
            if not CeciliaLib.session.modules:
                CeciliaLib.startCeciliaSound()
                return
            CeciliaLib.getControlPanel().nonZeroTime = 0
            CeciliaLib.setVar("toDac", True)
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.SetForegroundColour("#FFFFFF")
            CeciliaLib.getVar("grapher").toolbar.loadingMsg.Refresh()
            CeciliaLib.getControlPanel().transportButtons.setPlay(True)
            wx.CallLater(50, CeciliaLib.startCeciliaSound, True)
        else:
            CeciliaLib.stopCeciliaSound()

    def onBounceToDisk(self, event):
        if CeciliaLib.session.selected is None:
            return
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
            CeciliaLib.getVar("interface").destroySessionWindow()
            CeciliaLib.setVar("interface", None)

    def newRecent(self, file, remove=False):
        file = CeciliaLib.ensureNFD(os.path.abspath(file))
        try:
            with open(RECENT_FILE_PATH, encoding='utf-8') as stream:
                lines = [line.strip() for line in stream if line.strip()]
        except OSError:
            lines = []
        lines = [path for path in lines if path != file]
        if not remove:
            lines.insert(0, file)
        with open(RECENT_FILE_PATH, 'w', encoding='utf-8') as stream:
            stream.writelines(path + '\n' for path in lines[:10])
        for frame in (self, CeciliaLib.getVar('interface')):
            if frame is not None:
                frame.menubar.refreshRecentMenu()

    def openModuleFromMenu(self, path, builtin=False):
        return CeciliaLib.openCeciliaFile(
            self, path, builtin,
            new_session=not getattr(self, 'addingChainModule', False))

    def onOpen(self, event, builtin=False):
        if isinstance(event, wx.CommandEvent):
            CeciliaLib.openCeciliaFile(self)
        elif os.path.isfile(event):
            if event.lower().endswith('.c5chain'):
                CeciliaLib.openChainSession(self, event)
            else:
                self.openModuleFromMenu(event, builtin)

    def onOpenRandom(self, event):
        categories = [folder for folder in os.listdir(MODULES_PATH) if not folder.startswith(".")]
        category = random.choice(categories)
        files = [f for f in os.listdir(os.path.join(MODULES_PATH, category)) if f.endswith(FILE_EXTENSION)]
        file = random.choice(files)
        self.onOpen(os.path.join(MODULES_PATH, category, file), True)

    def openRecent(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id).GetItemLabelText().replace("\n", "").strip()
        if os.path.isfile(file):
            self.openModuleFromMenu(file)
        else:
            CeciliaLib.showErrorDialog("Error while trying to open a file!", "No such file : %s" % file[:-1])
            self.newRecent(file, remove=True)

    def onOpenBuiltin(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id)
        filename = file.GetItemLabelText()
        filedict = self.GetMenuBar().files
        for key in filedict.keys():
            if filename in filedict[key]:
                dirname = key
                break
        name = os.path.join(CeciliaLib.ensureNFD(MODULES_PATH), dirname, filename)
        self.openModuleFromMenu(name, True)

    def onOpenPrefModule(self, event):
        menu = self.GetMenuBar()
        id = event.GetId()
        file = menu.FindItemById(id)
        filename = file.GetItemLabelText()
        filedir = file.GetMenu().GetTitle()
        prefPath = CeciliaLib.getVar("prefferedPath")
        prefPaths = prefPath.split(';')
        prefBaseNames = [os.path.basename(path) for path in prefPaths]
        dirname = prefPaths[prefBaseNames.index(filedir)]
        if dirname:
            name = os.path.join(dirname, filename)
            self.openModuleFromMenu(name)

    def openModuleAsText(self, event):
        if CeciliaLib.session.selected is None:
            return
        CeciliaLib.openCurrentFileAsText(CeciliaLib.getVar("currentCeciliaFile"))

    def reloadCurrentModule(self, event):
        if CeciliaLib.session.selected is None:
            return
        CeciliaLib.openCeciliaFile(self, CeciliaLib.getVar("currentCeciliaFile"), replace=True)

    def onSaveAs(self, event):
        if CeciliaLib.session.selected is None:
            return
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
        if CeciliaLib.session.selected is not None:
            self.reloadCurrentModule(event)

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
        if not CeciliaLib.confirmSessionDiscard(CeciliaLib.getVar('interface') or self):
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
        if CeciliaLib.session.selected is None:
            return
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
