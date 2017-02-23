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

import os, sys, wx, time, math, copy, codecs
import pprint as pp
import unicodedata
from subprocess import Popen
from pyolib._wxwidgets import SpectrumDisplay
from .constants import *
from .API_interface import *
import Resources.Variables as vars

if sys.version_info[0] < 3:
    unicode_t = unicode
else:
    unicode_t = str

def buildFileTree():
    root = MODULES_PATH
    directories = []
    files = {}
    for dir in sorted(os.listdir(MODULES_PATH)):
        if not dir.startswith('.'):
            directories.append(dir)
            files[dir] = []
            for f in sorted(os.listdir(os.path.join(root, dir))):
                if not f.startswith('.'):
                    files[dir].append(f)
    return root, directories, files

def setVar(var, value):
    vars.CeciliaVar[var] = value

def getVar(var, unicode=False):
    if unicode:
        return ensureNFD(vars.CeciliaVar[var])
    else:
        return vars.CeciliaVar[var]

def setJackParams(client=None, inPortName=None, outPortName=None):
    if client is not None:
        vars.CeciliaVar['jack']['client'] = client
    if inPortName is not None:
        vars.CeciliaVar['jack']['inPortName'] = inPortName
    if outPortName is not None:
        vars.CeciliaVar['jack']['outPortName'] = outPortName

def setPlugins(x, pos):
    vars.CeciliaVar['plugins'][pos] = x

def getControlPanel():
    return getVar('interface').getControlPanel()

def writeVarToDisk():
    vars.writeCeciliaPrefsToFile()

def chooseColour(i, numlines):
    def clip(x):
        val = int(x * 255)
        if val < 0: val = 0
        elif val > 255: val = 255
        else: val = val
        return val

    def colour(i, numlines, sat, bright):
        hue = (i / float(numlines)) * 315
        segment = math.floor(hue / 60) % 6
        fraction = hue / 60 - segment
        t1 = bright * (1 - sat)
        t2 = bright * (1 - (sat * fraction))
        t3 = bright * (1 - (sat * (1 - fraction)))
        if segment == 0:
            r, g, b = bright, t3, t1
        elif segment == 1:
            r, g, b = t2, bright, t1
        elif segment == 2:
            r, g, b = t1, bright, t3
        elif segment == 3:
            r, g, b = t1, t2, bright
        elif segment == 4:
            r, g, b = t3, t1, bright
        elif segment == 5:
            r, g, b = bright, t1, t2
        return wx.Colour(clip(r), clip(g), clip(b))

    lineColour = colour(i, numlines, 1, 1)
    midColour = colour(i, numlines, .5, .5)
    knobColour = colour(i, numlines, .8, .5)
    sliderColour = colour(i, numlines, .5, .75)

    return [lineColour, midColour, knobColour, sliderColour]

def chooseColourFromName(name):
    def clip(x):
        val = int(x * 255)
        if val < 0: val = 0
        elif val > 255: val = 255
        else: val = val
        return val

    def colour(name):
        vals = COLOUR_CLASSES[name]
        hue = vals[0]
        bright = vals[1]
        sat = vals[2]
        segment = int(math.floor(hue / 60))
        fraction = hue / 60 - segment
        t1 = bright * (1 - sat)
        t2 = bright * (1 - (sat * fraction))
        t3 = bright * (1 - (sat * (1 - fraction)))
        if segment == 0:
            r, g, b = bright, t3, t1
        elif segment == 1:
            r, g, b = t2, bright, t1
        elif segment == 2:
            r, g, b = t1, bright, t3
        elif segment == 3:
            r, g, b = t1, t2, bright
        elif segment == 4:
            r, g, b = t3, t1, bright
        elif segment == 5:
            r, g, b = bright, t1, t2
        return wx.Colour(clip(r), clip(g), clip(b))

    lineColour = colour(name)
    midColour = colour(name)
    knobColour = colour(name)
    sliderColour = colour(name)

    return [lineColour, midColour, knobColour, sliderColour]

###### Start / Stop / Drivers ######
def startCeciliaSound(timer=True, rec=False):
    # Check if soundfile is loaded
    for key in getVar("userInputs").keys():
        if 'mode' not in getVar("userInputs")[key]:
            getVar("userInputs")[key]['mode'] = 0
        if getVar("userInputs")[key]['mode'] == 0:
            if not os.path.isfile(getVar("userInputs")[key]['path']):
                showErrorDialog('No input sound file!', 'In/Out panel, "%s" has no input sound file, please load one...' % getControlPanel().getCfileinFromName(key).label)
                ret = getControlPanel().getCfileinFromName(key).onLoadFile()
                if not ret:
                    resetControls()
                    getVar("grapher").toolbar.loadingMsg.SetForegroundColour(TITLE_BACK_COLOUR)
                    wx.CallAfter(getVar("grapher").toolbar.loadingMsg.Refresh)
                    return
    getControlPanel().resetMeter()
    if getVar('spectrumFrame') is not None:
        try:
            getVar('spectrumFrame')._destroy(None)
        except:
            getVar('interface').menubar.spectrumSwitch(False)
            setVar('showSpectrum', 0)
        finally:
            setVar('spectrumFrame', None)
    getVar("audioServer").shutdown()
    getVar("audioServer").reinit()
    getVar("audioServer").boot()
    if getVar("currentModuleRef") is not None:
        getVar("audioServer").loadModule(getVar("currentModuleRef"))
    else:
        showErrorDialog("Wow...!", "No module to load.")
    getVar("grapher").toolbar.convertSlider.Hide()
    getVar("presetPanel").presetChoice.setEnable(False)
    getVar("audioServer").start(timer=timer, rec=rec)
    if getVar('showSpectrum'):
        f = SpectrumDisplay(None, getVar("audioServer").spectrum)
        getVar("audioServer").spectrum._setViewFrame(f)
        setVar('spectrumFrame', f)
        f.Show()
    getVar("grapher").toolbar.loadingMsg.SetForegroundColour(TITLE_BACK_COLOUR)
    wx.CallAfter(getVar("grapher").toolbar.loadingMsg.Refresh)

def stopCeciliaSound():
    if getVar("audioServer").isAudioServerRunning():
        getVar("audioServer").stop()
        if getVar("currentModule") is not None:
            getVar("audioServer").checkForAutomation()
            getVar("currentModule")._checkForAutomation()
            getVar("grapher").checkForAutomation()
        time.sleep(.25)
    resetControls()

def resetControls():
    if getVar('interface') is not None:
        getControlPanel().transportButtons.setPlay(False)
        getControlPanel().transportButtons.setRecord(False)
        getVar("presetPanel").presetChoice.setEnable(True)
        if getControlPanel().tmpTotalTime != getVar("totalTime"):
            getControlPanel().setTotalTime(getControlPanel().tmpTotalTime, True)
        wx.CallAfter(getControlPanel().vuMeter.reset)

def queryAudioMidiDrivers():
    inputs, inputIndexes, defaultInput, outputs, outputIndexes, defaultOutput, midiInputs, midiInputIndexes, defaultMidiInput = getVar("audioServer").getAvailableAudioMidiDrivers()

    setVar("availableAudioOutputs",  outputs)
    setVar("availableAudioOutputIndexes",  outputIndexes)
    if getVar("audioOutput") not in outputIndexes:
        try:
            setVar("audioOutput", outputIndexes[outputs.index(defaultOutput)])
        except:
            setVar("audioOutput", 0)

    setVar("availableAudioInputs", inputs)
    setVar("availableAudioInputIndexes", inputIndexes)
    if getVar("audioInput") not in inputIndexes:
        try:
            setVar("audioInput", inputIndexes[inputs.index(defaultInput)])
        except:
            setVar("audioInput", 0)

    if midiInputs == []:
        setVar("useMidi", 0)
    else:
        setVar("useMidi", 1)
    setVar("availableMidiInputs", midiInputs)
    setVar("availableMidiInputIndexes", midiInputIndexes)
    if getVar("midiDeviceIn") not in midiInputIndexes:
        try:
            setVar("midiDeviceIn", midiInputIndexes[midiInputs.index(defaultMidiInput)])
        except:
            setVar("midiDeviceIn", 0)

def openAudioFileDialog(parent, wildcard, type='open', defaultPath=os.path.expanduser('~')):
    openDialog = wx.FileDialog(parent, message='Choose a file to %s' % type,
                                defaultDir=defaultPath, wildcard=wildcard,
                                style=wx.FD_OPEN | wx.FD_PREVIEW)
    if openDialog.ShowModal() == wx.ID_OK:
        filePath = ensureNFD(openDialog.GetPath())
        setVar("openAudioFilePath", os.path.split(filePath)[0])
    else:
        filePath = None
    openDialog.Destroy()
    return filePath

def saveFileDialog(parent, wildcard, type='Save'):
    if type == 'Save audio':
        defaultPath = getVar("saveAudioFilePath", unicode=True)
        ext = "." + getVar("audioFileType")
    else:
        defaultPath = getVar("saveFilePath", unicode=True)
        ext = ".c5"

    defaultFile = os.path.split(getVar("currentCeciliaFile", unicode=True))[1].split(".")[0]
    saveAsDialog = wx.FileDialog(parent, message="%s file as ..." % type,
                                 defaultDir=defaultPath, defaultFile=defaultFile + ext,
                                 wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if saveAsDialog.ShowModal() == wx.ID_OK:
        filePath = ensureNFD(saveAsDialog.GetPath())
        if type == 'Save audio':
            setVar("saveAudioFilePath", os.path.split(filePath)[0])
        else:
            setVar("saveFilePath", os.path.split(filePath)[0])
    else:
        filePath = None
    saveAsDialog.Destroy()
    return filePath

def saveBeforeClose(parent):
    if getVar("isModified"):
        saveBeforeCloseDialog = wx.MessageDialog(parent,
                        'This file has been modified since the last save point. \
                        Would you like to save the changes?',
                        'Save Changes?', wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT)
    else:
        return True

    answer = saveBeforeCloseDialog.ShowModal()
    if answer == wx.ID_YES:
        if saveCeciliaFile(parent, False):
            result =  True
        else:
            result =  False
    elif answer == wx.ID_NO:
        result =  True
    elif answer == wx.ID_CANCEL:
        result =  False

    saveBeforeCloseDialog.Destroy()
    return result

def showErrorDialog(title, msg):
    dlg = wx.MessageDialog(None, msg, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()

###### External app calls ######
def loadPlayerEditor(app_type):
    if getVar("systemPlatform")  == 'win32':
        wildcard =  "Executable files (*.exe)|*.exe|"     \
                    "All files|*"
    elif getVar("systemPlatform")  == 'darwin':
        wildcard =  "Application files (*.app)|*.app|"     \
                    "All files|*"
    else:
        wildcard = "All files|*"

    path = ''
    dlg = wx.FileDialog(None, message="Choose a %s..." % app_type,
                        defaultDir=ensureNFD(os.path.expanduser('~')),
                        wildcard=wildcard, style=wx.FD_OPEN)

    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    dlg.Destroy()

    if path:
        if app_type == 'soundfile player':
            setVar("soundfilePlayer", path)
        elif app_type == 'soundfile editor':
            setVar("soundfileEditor", path)
        elif app_type == 'text editor':
            setVar("textEditor", path)

def listenSoundfile(soundfile):
    if getVar("soundfilePlayer") == '':
        showErrorDialog("Preferences not set", "Choose a soundfile player first.")
        loadPlayerEditor('soundfile player')
    if os.path.isfile(soundfile):
        app = getVar("soundfilePlayer")
        if getVar("systemPlatform")  == 'darwin':
            cmd = 'open -a "%s" "%s"' % (app, soundfile)
            Popen(cmd, shell=True)
        elif getVar("systemPlatform")  == 'win32':
            try:
                Popen([app, soundfile], shell=False)
            except (OSError, OSError2):
                print('Unable to open desired software:\n' + app)
        else:
            cmd = '"%s" "%s"' % (app, soundfile)
            try:
                Popen(cmd, shell=True)
            except (OSError, OSError2):
                print('Unable to open desired software:\n' + app)

def editSoundfile(soundfile):
    if getVar("soundfileEditor") == '':
        showErrorDialog("Preferences not set", "Choose a soundfile editor first.")
        loadPlayerEditor('soundfile editor')
    if os.path.isfile(soundfile):
        app = getVar("soundfileEditor")
        if getVar("systemPlatform")  == 'darwin':
            cmd = 'open -a "%s" "%s"' % (app , soundfile)
            Popen(cmd, shell=True)
        elif getVar("systemPlatform")  == 'win32':
            try:
                Popen([app, soundfile], shell=False)
            except (OSError, OSError2):
                print('Unable to open desired software:\n' + app)
        else:
            cmd = '%s %s' % (app, soundfile)
            try:
                Popen(cmd, shell=True)
            except (OSError, OSError2):
                print('Unable to open desired software:\n' + app)

def openCurrentFileAsText(curfile):
    if getVar("textEditor") == '':
        showErrorDialog("Preferences not set", "Choose a text editor first.")
        loadPlayerEditor('text editor')
    if os.path.isfile(curfile):
        app = getVar("textEditor")
        if getVar("systemPlatform")  == 'darwin':
            cmd = 'open -a "%s" "%s"' % (app, os.path.join(os.getcwd(), curfile))
            Popen(cmd, shell=True, cwd=os.path.expanduser("~"))
        elif getVar("systemPlatform")  == 'win32':
            try:
                Popen([app, curfile], shell=False)
            except (OSError, OSError2):
                print('Unable to open desired software:\n' + app)
        else:
            cmd = '%s %s' % (app, curfile)
            try:
                Popen(cmd, shell=True)
            except (OSError, OSError2):
                print('Unable to open desired software:\n' + app)

###### Preset functions ######
def deletePreset(preset):
    del vars.CeciliaVar['presets'][preset]

def loadPresetFromDict(preset):
    currentModule = getVar("currentModule")
    setVar("currentModule", None)
    if preset in getVar("presets") or preset == "init":
        if preset == "init":
            presetData = getVar("initPreset")
        else:
            presetData = getVar("presets")[preset]

        for data in presetData.keys():
            if data == 'userInputs':
                if presetData[data] == {}:
                    continue
                ok = True
                prekeys = presetData[data].keys()
                for key in prekeys:
                    if not os.path.isfile(presetData[data][key]['path']):
                        ok = False
                        break
                if not getVar("rememberedSound"):
                    if ok:
                        setVar("userInputs", copy.deepcopy(presetData[data]))
                        updateInputsFromDict()
                    else:
                        for input in getVar("userInputs"):
                            cfilein = getControlPanel().getCfileinFromName(input)
                            cfilein.reset()
                            cfilein.reinitSamplerFrame()
                else:
                    if ok:
                        setVar("userInputs", copy.deepcopy(presetData[data]))
                        updateInputsFromDict()
                    else:
                        for input in getVar("userInputs"):
                            cfilein = getControlPanel().getCfileinFromName(input)
                            cfilein.reinitSamplerFrame()
            elif data == 'userSliders':
                slidersDict = presetData[data]
                for slider in getVar("userSliders"):
                    if slider.getName() in slidersDict:
                        slider.setState(slidersDict[slider.getName()])
                del slidersDict
            elif data == 'plugins':
                pluginsDict = copy.deepcopy(presetData[data])
                wx.CallAfter(getControlPanel().setPlugins, pluginsDict)
                del pluginsDict
            elif data == 'userTogglePopups':
                togDict = presetData[data]
                for widget in getVar("userTogglePopups"):
                    if widget.getName() in togDict:
                        widget.setValue(togDict[widget.getName()], True)
                del togDict
            else:
                continue
        if preset == "init":
            for line in getVar("grapher").getPlotter().getData():
                try:
                    line.reinit()
                except:
                    pass
        elif 'userGraph' in presetData:
            graphDict = presetData['userGraph']
            ends = ['min', 'max']
            for line in graphDict:
                for i, graphLine in enumerate(getVar("grapher").getPlotter().getData()):
                    if line == graphLine.getName():
                        graphLine.setLineState(copy.deepcopy(graphDict[line]))
                        break
                    else:
                        for end in ends:
                            if graphLine.getLabel().endswith(end) and line.endswith(end) and line.startswith(graphLine.getName()):
                                graphLine.setLineState(copy.deepcopy(graphDict[line]))
                                break
            del graphDict

        setVar("totalTime", presetData["totalTime"])
        getControlPanel().updateDurationSlider()
        setVar("nchnls", presetData["nchnls"])
        updateNchnlsDevices()
        getVar("gainSlider").SetValue(presetData["gainSlider"])
        getVar("presetPanel").setLabel(preset)
        getVar("grapher").getPlotter().draw()
        setVar("currentModule", currentModule)
        getVar("grapher").setTotalTime(getVar("totalTime"))

        wx.CallAfter(againForPluginKnobs, presetData)

### This is a hack to ensure that plugin knob automations are drawn in the grapher.
### Called within a wx.CallAfter to be executed after wx.CallAfter(getControlPanel().setPlugins).
def againForPluginKnobs(presetData):
    if 'userGraph' in presetData:
        graphDict = presetData['userGraph']
        for line in graphDict:
            for i, graphLine in enumerate(getVar("grapher").getPlotter().getData()):
                if line == graphLine.getName():
                    graphLine.setLineState(copy.deepcopy(graphDict[line]))
                    break
        del graphDict
        getVar("grapher").getPlotter().draw()
        getVar("grapher").setTotalTime(getVar("totalTime"))

def savePresetToDict(presetName):
    presetDict = dict()
    presetDict['nchnls'] = getVar("nchnls")
    presetDict['totalTime'] = getVar("totalTime")
    presetDict['gainSlider'] = getVar("gainSlider").GetValue()
    if getVar("interface"):
        presetDict['userInputs'] = completeUserInputsDict()

        sliderDict = dict()
        for slider in getVar("userSliders"):
            sliderDict[slider.getName()] = slider.getState()
        presetDict['userSliders'] = copy.deepcopy(sliderDict)
        del sliderDict

        widgetDict = dict()
        plugins = getVar("plugins")
        for i, plugin in enumerate(plugins):
            if plugin is None:
                widgetDict[i] = ['None', [0, 0, 0, 0], [[0, 0, None], [0, 0, None], [0, 0, None]]]
            else:
                widgetDict[i] = [plugin.getName(), plugin.getParams(), plugin.getStates()]
        presetDict['plugins'] = copy.deepcopy(widgetDict)
        del widgetDict

        widgetDict = dict()
        for widget in getVar("userTogglePopups"):
            widgetDict[widget.getName()] = widget.getValue()
        presetDict['userTogglePopups'] = copy.deepcopy(widgetDict)
        del widgetDict

        graphDict = dict()
        for line in getVar("grapher").getPlotter().getData():
            if line.slider is None:
                graphDict[line.getName()] = line.getLineState()
            else:
                outvalue = line.slider.getValue()
                if line.slider.widget_type in ["slider", "plugin_knob"]:
                    graphDict[line.getName()] = line.getLineState()
                elif line.slider.widget_type == "range":
                    ends = ['min', 'max']
                    for i in range(len(outvalue)):
                        if line.getLabel().endswith(ends[i]):
                            graphDict[line.getName() + ends[i]] = line.getLineState()
                            break
                elif line.slider.widget_type == "splitter":
                    for i in range(len(outvalue)):
                        if line.getLabel().endswith("%d" % i):
                            graphDict[line.getName() + "_%d" % i] = line.getLineState()
                            break
        presetDict['userGraph'] = copy.deepcopy(graphDict)
        del graphDict

    if presetName == "init":
        setVar("initPreset", copy.deepcopy(presetDict))
    else:
        getVar("presets")[presetName] = copy.deepcopy(presetDict)
        setVar("isModified", True)

def completeUserInputsDict():
    for i in getVar("userInputs"):
        getVar("userInputs")[i]['mode'] = 0
        if getVar("userInputs")[i]['type'] == 'csampler':
            cfilein = getControlPanel().getCfileinFromName(i)
            getVar("userInputs")[i]['off' + cfilein.getName()] = cfilein.getOffset()
            getVar("userInputs")[i]['loopMode'] = cfilein.getSamplerInfo()['loopMode']
            getVar("userInputs")[i]['startFromLoop'] = cfilein.getSamplerInfo()['startFromLoop']
            getVar("userInputs")[i]['loopX'] = cfilein.getSamplerInfo()['loopX']
            getVar("userInputs")[i]['loopIn'] = cfilein.getSamplerInfo()['loopIn']
            getVar("userInputs")[i]['loopOut'] = cfilein.getSamplerInfo()['loopOut']
            getVar("userInputs")[i]['gain'] = cfilein.getSamplerInfo()['gain']
            getVar("userInputs")[i]['transp'] = cfilein.getSamplerInfo()['transp']
        elif getVar("userInputs")[i]['type'] == 'cfilein':
            cfilein = getControlPanel().getCfileinFromName(i)
            getVar("userInputs")[i]['off' + cfilein.getName()] = cfilein.getOffset()
    return copy.deepcopy(getVar("userInputs"))

def updateInputsFromDict():
    for input in getVar("userInputs"):
        cfilein = getControlPanel().getCfileinFromName(input)
        if cfilein and os.path.isfile(getVar("userInputs")[input]['path']):
            inputDict = getVar("userInputs")[input]
            cfilein.updateMenuFromPath(inputDict['path'])
            for k in inputDict:
                if k == 'loopMode':
                    cfilein.getSamplerFrame().setLoopMode(inputDict[k])
                elif k == 'loopX':
                    cfilein.getSamplerFrame().setLoopX(inputDict[k])
                elif k == 'loopIn':
                    cfilein.getSamplerFrame().setLoopIn(inputDict[k])
                elif k == 'loopOut':
                    cfilein.getSamplerFrame().setLoopOut(inputDict[k])
                elif k == 'gain':
                    cfilein.getSamplerFrame().setGain(inputDict[k])
                elif k == 'transp':
                    cfilein.getSamplerFrame().setTransp(inputDict[k])
                elif k == 'startFromLoop':
                    cfilein.getSamplerFrame().setStartFromLoop(inputDict[k])
                elif k == ('off' + input):
                    cfilein.setOffset(inputDict[k])
                elif k == 'path':
                    pass

###### Open / Save / Close ######
def saveCeciliaFile(parent, showDialog=True):
    if getVar("builtinModule") or showDialog:
        wildcard = "Cecilia file (*.%s)|*.%s" % (FILE_EXTENSION, FILE_EXTENSION)
        fileToSave = saveFileDialog(parent, wildcard, 'Save')
        if not fileToSave:
            return False
        else:
            if not fileToSave.endswith(FILE_EXTENSION):
                fileToSave = "%s.%s" % (fileToSave, FILE_EXTENSION)
    else:
        fileToSave = getVar("currentCeciliaFile", unicode=True)

    savePresetToDict("last save")

    curfile = codecs.open(getVar("currentCeciliaFile", unicode=True), "r", encoding="utf-8")
    curtext = curfile.read()
    curfile.close()
    delimiter = curtext.find(PRESETS_DELIMITER)
    if delimiter != -1:
        curtext = curtext[:delimiter]

    try:
        file = codecs.open(fileToSave, "w", encoding="utf-8")
    except IOError:
        dlg = wx.MessageDialog(parent, 'Please verify permissions and write access on the file and try again.',
                            '"%s" could not be opened for writing' % (fileToSave), wx.OK | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            return

    file.write(curtext.rstrip())
    file.write("\n\n\n")
    file.write(PRESETS_DELIMITER)
    file.write("\n\n")
    preset = pp.pformat(getVar("presets"), width=160)
    preset = "CECILIA_PRESETS = " + preset
    preset = ensureNFD(preset)
    file.write(preset)

    file.close()

    setVar("builtinModule", False)
    setVar("currentCeciliaFile", fileToSave)
    setVar("isModified", False)

    return True

def openCeciliaFile(parent, openfile=None, builtin=False):
    if not openfile:
        wildcard = "Cecilia file (*.%s)|*.%s" % (FILE_EXTENSION, FILE_EXTENSION)
        defaultPath = getVar("openFilePath", unicode=True)
        openDialog = wx.FileDialog(parent, message='Choose a Cecilia file to open...',
                                    defaultDir=defaultPath, wildcard=wildcard, style=wx.FD_OPEN)
        if openDialog.ShowModal() == wx.ID_OK:
            cecFilePath = openDialog.GetPath()
            setVar("openFilePath", (os.path.split(cecFilePath)[0]))
        else:
            cecFilePath = None
        openDialog.Destroy()

        if cecFilePath is None:
            return

    else:
        cecFilePath = openfile

    if getVar("audioServer").isAudioServerRunning():
        stopCeciliaSound()

    snds = []
    if getVar("rememberedSound") and getVar("interfaceWidgets") and getVar("userInputs"):
        names = [d['name'] for d in getVar("interfaceWidgets")]
        keys = getVar("userInputs").keys()
        sortlist = list(zip([names.index(k) for k in keys], keys))
        sortlist.sort()
        index, keys = list(zip(*sortlist))
        for key in keys:
            if getVar("userInputs")[key]['path'] != '':
                snds.append(getVar("userInputs")[key]['path'])

    if not closeCeciliaFile(parent):
        return

    getVar("mainFrame").Hide()

    setVar("builtinModule", builtin)
    setVar("currentCeciliaFile", cecFilePath)
    parent.newRecent(cecFilePath)

    setVar("isModified", False)

    getVar("audioServer").openCecFile(cecFilePath)

    if getVar("interface"):
        for i, cfilein in enumerate(getControlPanel().getCfileinList()):
            if i >= len(snds):
                break
            cfilein.onLoadFile(snds[i])

    savePresetToDict("init")

    if "last save" in getVar("presets"):
        loadPresetFromDict("last save")

    wx.CallAfter(getVar("interface").Raise)

def closeCeciliaFile(parent):
    if not saveBeforeClose(parent):
        return False
    getVar("mainFrame").closeInterface()
    setVar("currentCeciliaFile", '')
    if getVar("interface"):
        getVar("interface").onClose(wx.EVT_CLOSE)
        setVar("interface", None)
        setVar("presets", {})
    wx.CallLater(200, setVar, "isModified", False)
    return True

###### Interface creation utilities ######
def resetWidgetVariables():
    setVar("gainSlider", None)
    setVar("userInputs", {})
    setVar("userSliders", [])
    setVar("userSamplers", [])
    setVar("userTogglePopups", [])
    setVar("samplerSliders", [])
    setVar("grapher", None)
    setVar("presetPanel", None)

def parseInterfaceText():
    interfaceWidgets = getVar("interfaceWidgets")
    return interfaceWidgets

def updateNchnlsDevices():
    try:
        getVar("interface").updateNchnls()
    except:
        pass

###### Utility functions #######
def removeDuplicates(seq):
   result = []
   for item in seq:
       if item not in result:
           result.append(item)
   return result

def autoRename(path, index=0, wrap=False):
    if os.path.exists(path):
        file = ensureNFD(os.path.split(path)[1])
        if wrap:
            name = ensureNFD(file.rsplit('.', 1)[0])[:-4]
        else:
            name = ensureNFD(file.rsplit('.', 1)[0])
        ext = file.rsplit('.', 1)[1]

        if len(name) >= 5:
            try:
                if name[-4] == '_' and type(eval(name[-3:])) == int:
                    name = name[:-4]
            except:
                pass
        root = os.path.split(path)[0]
        filelist = os.listdir(root)
        num = index
        for f in filelist:
            f = ensureNFD(f)
            if name in f and ext in f:
                num += 1
        newName = name + '_%03d' % num + '.' + ext
        newPath = os.path.join(root, newName)
        return autoRename(newPath, index + 1, True)
    else:
        newPath = path
    return newPath

def shortenName(name, maxChar):
    name = ensureNFD(name)
    if len(name) > maxChar:
        shortenChar = '...'
        addSpace = 0
        charSpace = (maxChar - len(shortenChar)) // 2
        if (maxChar - 5) % 2 != 0:
            addSpace = 1
        name = name[:charSpace + addSpace] + shortenChar + name[len(name) - charSpace:]
    return name

def ensureNFD(unistr):
    if getVar("systemPlatform").startswith('linux') or sys.platform == 'win32':
        encodings = [DEFAULT_ENCODING, ENCODING,
                     'cp1252', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    else:
        encodings = [DEFAULT_ENCODING, ENCODING,
                     'macroman', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    decstr = unistr
    if type(decstr) != unicode_t:
        for encoding in encodings:
            try:
                decstr = decstr.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
            except:
                decstr = "UnableToDecodeString"
                print("Unicode encoding not in a recognized format...")
                break
    if decstr == "UnableToDecodeString":
        return unistr
    else:
        return unicodedata.normalize(format, decstr)

def toSysEncoding(unistr):
    try:
        if getVar("systemPlatform") == "win32":
            unistr = unistr.encode(ENCODING)
        else:
            unistr = unicode(unistr)
    except:
        pass
    return unistr