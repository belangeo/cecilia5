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

import os, sys, wx, time, math, copy, codecs, shutil, json
import unicodedata
from subprocess import Popen
from .constants import *
from .API_interface import *
import Resources.Variables as vars
import wx.lib.agw.supertooltip as STT
import xmlrpc.client as xmlrpclib
from .Session import ChainSession, INSTANCE_KEYS, active_instance, instance_context, normalize_snapshot

session = ChainSession()


def callAfter(callback, *args, **kwargs):
    """Do not deliver queued GUI updates to retired editors or deleted windows."""
    owner = active_instance.get()
    target = getattr(callback, '__self__', None)

    def deliver():
        if owner is not None and owner.retired:
            return
        if isinstance(target, wx.Window) and (not target or target.IsBeingDeleted()):
            return
        with instance_context(owner):
            callback(*args, **kwargs)

    wx.CallAfter(deliver)

def moduleOwner():
    return active_instance.get() or session.selected

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
    owner = moduleOwner()
    if var in INSTANCE_KEYS and owner is not None:
        owner.state[var] = value
        if var == 'currentCeciliaFile':
            owner.path = os.path.abspath(value)
        return
    vars.CeciliaVar[var] = value
    if var == 'totalTime':
        for module in session.modules:
            grapher = module.state['grapher']
            if grapher is not None:
                with instance_context(module):
                    grapher.setTotalTime(value)
        frame = vars.CeciliaVar['interface']
        if frame is not None and hasattr(frame, 'controlPanel'):
            frame.controlPanel.durationSlider.SetValue(value)

def getVar(var, unicode=False):
    owner = moduleOwner()
    value = owner.state[var] if var in INSTANCE_KEYS and owner is not None else vars.CeciliaVar[var]
    return ensureNFD(value) if unicode else value

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
    owner = active_instance.get()
    if owner is not None and owner.inputs is not None:
        return owner.inputs
    return getVar('interface').getControlPanel()

def automationPath(name):
    owner = moduleOwner()
    if owner is not None:
        name = owner.id + '_' + name
    return os.path.join(AUTOMATION_SAVE_PATH, name)

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
        hue = (i / numlines) * 315
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

### Tooltips ###
class CECTooltip(STT.SuperToolTip):
    def __init__(self, tip):
        STT.SuperToolTip.__init__(self, tip)
        self.SetStartDelay(1.5)
        if getVar("useTooltips"):
            self.EnableTip(True)
        else:
            self.EnableTip(False)
        self.ApplyStyle("Gray")

    def OnMouseEvents(self, evt):
        if evt.ButtonDown() or evt.ButtonDClick():
            self.DoHideNow()
        evt.Skip()

    def update(self):
        if getVar("useTooltips"):
            self.EnableTip(True)
        else:
            self.EnableTip(False)

def setToolTip(obj, tip):
    pruneTooltips()
    if "\n" in tip:
        pos = tip.find("\n")
        header = tip[:pos]
        body = tip[pos+1:]
    else:
        header = "Documentation"
        body = tip
    tooltip = CECTooltip(body)
    tooltip.SetHeader(header)
    tooltip.SetTarget(obj)
    tooltip.SetDrawHeaderLine(True)
    getVar("tooltips").append(tooltip)
    obj.Bind(wx.EVT_MOUSE_EVENTS, tooltip.OnMouseEvents)

def pruneTooltips():
    tooltips = getVar('tooltips')
    tooltips[:] = [tooltip for tooltip in tooltips if tooltip.GetTarget()]


def updateTooltips():
    pruneTooltips()
    for tooltip in getVar("tooltips"):
        tooltip.update()

###### Start / Stop / Drivers ######
def startCeciliaSound(timer=True, rec=False):
    if not session.modules:
        showErrorDialog('No module loaded', 'Open a module to start a chain.')
        resetControls()
        return
    for index, instance in enumerate(session.modules):
        with instance_context(instance):
            for key, info in getVar('userInputs').items():
                if index > 0 and key == instance.primary_input:
                    continue
                if info.get('mode', 0) == 0 and not os.path.isfile(info.get('path', '')):
                    widget = getControlPanel().getCfileinFromName(key)
                    showErrorDialog('No input sound file', 'Stage %d (%s), "%s" needs a sound file.' %
                                    (index+1, instance.state['currentModuleName'], widget.label))
                    if not widget.onLoadFile():
                        resetControls()
                        return
    getControlPanel().resetMeter()
    getVar("audioServer").cleanup_module()
    getVar("audioServer").shutdown()
    getVar("audioServer").reinit()
    getVar("audioServer").boot()
    if getVar("currentModuleRef") is not None:
        if not getVar("audioServer").loadModule(getVar("currentModuleRef")):
            return
    else:
        showErrorDialog("Wow...!", "No module to load.")
        return
    getVar("grapher").toolbar.convertSlider.Hide()
    getVar("presetPanel").presetChoice.setEnable(False)
    getControlPanel().durationSlider.Disable()
    getVar("audioServer").start(timer=timer, rec=rec)
    from . import ChainUI
    ChainUI.playback_state(getVar('interface'), True)
    if getVar('showSpectrum'):
        getVar('mainFrame').openSpectrumWindow()
    getVar("grapher").toolbar.loadingMsg.SetForegroundColour(TITLE_BACK_COLOUR)
    callAfter(getVar("grapher").toolbar.loadingMsg.Refresh)

def stopCeciliaSound():
    if getVar('spectrumFrame') is not None:
        try:
            getVar('spectrumFrame').onClose()
        except:
            getVar('interface').menubar.spectrumSwitch(False)
            setVar('showSpectrum', 0)
        finally:
            setVar('spectrumFrame', None)
    if getVar("audioServer").isAudioServerRunning():
        getVar("audioServer").stop()
        time.sleep(.25)
        getVar('audioServer').checkForAutomation()
        for instance in session.modules:
            with instance_context(instance):
                if getVar('currentModule') is not None:
                    getVar('currentModule')._checkForAutomation()
                    getVar('grapher').checkForAutomation()
    resetControls()

def resetControls():
    if getVar('interface') is not None:
        getControlPanel().transportButtons.setPlay(False)
        getControlPanel().transportButtons.setRecord(False)
        from . import ChainUI
        ChainUI.playback_state(getVar('interface'), False)
        getControlPanel().durationSlider.Enable()
        if getControlPanel().tmpTotalTime != getVar("totalTime"):
            getControlPanel().setTotalTime(getControlPanel().tmpTotalTime, True)
        callAfter(getControlPanel().vuMeter.reset)

def queryAudioMidiDrivers():
    inputs, inputIndexes, defaultInput, outputs, outputIndexes, \
    defaultOutput, midiInputs, midiInputIndexes, defaultMidiInput = getVar("audioServer").getAvailableAudioMidiDrivers()
    setVar("availableAudioOutputs", outputs)
    setVar("availableAudioOutputIndexes", outputIndexes)
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
    setVar("canGrabFocus", False)
    openDialog = wx.FileDialog(parent, message='Choose a file to %s' % type,
                                defaultDir=defaultPath, wildcard=wildcard,
                                style=wx.FD_OPEN | wx.FD_PREVIEW)
    if openDialog.ShowModal() == wx.ID_OK:
        filePath = ensureNFD(openDialog.GetPath())
        setVar("openAudioFilePath", os.path.split(filePath)[0])
    else:
        filePath = None
    openDialog.Destroy()
    setVar("canGrabFocus", True)
    return filePath

def saveFileDialog(parent, wildcard, type='Save'):
    if type == 'Save audio':
        defaultPath = getVar("saveAudioFilePath", unicode=True)
        ext = "." + getVar("audioFileType")
    else:
        defaultPath = getVar("saveFilePath", unicode=True)
        ext = ".c5"

    setVar("canGrabFocus", False)
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
    setVar("canGrabFocus", True)
    return filePath

def showErrorDialog(title, msg):
    setVar("canGrabFocus", False)
    if getVar("mainFrame") is not None:
        dlg = wx.MessageDialog(getVar("mainFrame"), msg, title, wx.OK)
    else:
        dlg = wx.MessageDialog(None, msg, title, wx.OK)
    dlg.ShowModal()
    dlg.Destroy()
    setVar("canGrabFocus", True)

###### External app calls ######
def loadPlayerEditor(app_type):
    if getVar("systemPlatform") == 'win32':
        wildcard = "Executable files (*.exe)|*.exe|"     \
                    "All files|*"
    elif getVar("systemPlatform") == 'darwin':
        wildcard = "Application files (*.app)|*.app|"     \
                    "All files|*"
    else:
        wildcard = "All files|*"

    setVar("canGrabFocus", False)
    path = ''
    dlg = wx.FileDialog(None, message="Choose a %s..." % app_type,
                        defaultDir=ensureNFD(os.path.expanduser('~')),
                        wildcard=wildcard, style=wx.FD_OPEN)

    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    dlg.Destroy()
    setVar("canGrabFocus", True)

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
        if getVar("systemPlatform") == 'darwin':
            cmd = 'open -a "%s" "%s"' % (app, soundfile)
            Popen(cmd, shell=True)
        elif getVar("systemPlatform") == 'win32':
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
        if getVar("systemPlatform") == 'darwin':
            cmd = 'open -a "%s" "%s"' % (app, soundfile)
            Popen(cmd, shell=True)
        elif getVar("systemPlatform") == 'win32':
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
        if getVar("systemPlatform") == 'darwin':
            cmd = 'open -a "%s" "%s"' % (app, os.path.join(os.getcwd(), curfile))
            Popen(cmd, shell=True, cwd=os.path.expanduser("~"))
        elif getVar("systemPlatform") == 'win32':
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
def importEmbeddedPresets(module):
    # Older .c5 files include presets in a reserved Python section. Import them
    # without rewriting source files or overwriting presets the user has edited.
    directory = os.path.join(PRESETS_PATH, module.state['currentModuleName'])
    os.makedirs(directory, exist_ok=True)
    for name, data in module.embedded_presets.items():
        if not isinstance(name, str) or os.path.basename(name) != name or name in ('', '.', '..'):
            raise ValueError('Invalid embedded preset name.')
        path = os.path.join(directory, name)
        if os.path.exists(path):
            continue
        data = copy.deepcopy(data)
        data['plugins'] = {str(key): value for key, value in data.get('plugins', {}).items()}
        with open(path, 'w', encoding='utf-8') as stream:
            stream.write(xmlrpclib.dumps((data,), allow_none=True))


def loadPresetFromFile(preset):
    presetFile = os.path.join(PRESETS_PATH, getVar("currentModuleName"), preset)

    presetData = None
    if preset == "init":
        presetData = getVar("initPreset")
    elif os.path.isfile(presetFile):
        with open(presetFile, 'r') as f:
            try:
                result, method = xmlrpclib.loads(f.read())
                presetData = result[0]
            except:
                showErrorDialog("Preset corrupted...", "Failed to load preset '%s', reloading 'init'..." % preset)
                preset = "init"
                presetData = getVar("initPreset")

    if presetData is not None:
        restorePresetData(presetData, preset)


def restorePresetData(presetData, preset='init', restore_globals=None, force_inputs=False):
    owner = moduleOwner()
    if getVar("audioServer").isAudioServerRunning():
        showErrorDialog("Stop playback", "Stop playback before loading a preset.")
        return
    if restore_globals is None:
        restore_globals = len(session.modules) <= 1
    presetData = copy.deepcopy(presetData)
    if not restore_globals:
        for key in ('totalTime', 'nchnls', 'gainSlider', 'plugins'):
            presetData.pop(key, None)
        if 'userInputs' in presetData and not force_inputs:
            allowed = set(owner.auxiliary_inputs) if owner else set()
            presetData['userInputs'] = {key: value for key, value in presetData['userInputs'].items() if key in allowed}
    if presetData is not None:
        currentModule = getVar("currentModule")
        setVar("currentModule", None)

        for data in presetData.keys():
            if data == 'userInputs':
                if presetData[data] == {}:
                    continue
                inputData = presetData[data]
                if force_inputs or not getVar('rememberedSound'):
                    for name, info in inputData.items():
                        if name in getVar('userInputs'):
                            getVar('userInputs')[name].update(copy.deepcopy(info))
                    updateInputsFromDict()
                else:
                    for name, info in inputData.items():
                        widget = getControlPanel().getCfileinFromName(name)
                        if widget and not widget.filePath and os.path.isfile(info.get('path', '')):
                            getVar('userInputs')[name].update(copy.deepcopy(info))
                    updateInputsFromDict()
            elif data == 'userSliders':
                slidersDict = presetData[data]
                for slider in getVar("userSliders"):
                    if slider.getName() in slidersDict:
                        slider.setState(slidersDict[slider.getName()])
                del slidersDict
            elif data == 'plugins':
                pluginsDict = deepCopy(presetData[data])
                callAfter(getControlPanel().setPlugins, pluginsDict)
                del pluginsDict
            elif data == 'userTogglePopups':
                togDict = presetData[data]
                for widget in getVar("userTogglePopups"):
                    if widget.getName() in togDict and hasattr(widget, "setValue"):
                        widget.setValue(togDict[widget.getName()], True)
                del togDict
            else:
                continue
        if preset == "init" and not force_inputs:
            for line in getVar("grapher").getPlotter().getData():
                if not restore_globals and line.slider is not None and line.slider.widget_type == 'plugin_knob':
                    continue
                try:
                    line.reinit()
                except:
                    pass
        elif 'userGraph' in presetData:
            graphDict = deepCopy(presetData['userGraph'])
            ends = ['min', 'max']
            for line in graphDict:
                for i, graphLine in enumerate(getVar("grapher").getPlotter().getData()):
                    if not restore_globals and graphLine.slider is not None and graphLine.slider.widget_type == 'plugin_knob':
                        continue
                    if line == graphLine.getName():
                        graphLine.setLineState(graphDict[line])
                        break
                    else:
                        for end in ends:
                            if graphLine.getLabel().endswith(end) and line.endswith(end) and line.startswith(graphLine.getName()):
                                graphLine.setLineState(graphDict[line])
                                break
            del graphDict

        if restore_globals:
            setVar("totalTime", presetData["totalTime"])
            getControlPanel().updateDurationSlider()
            setVar("nchnls", presetData["nchnls"])
            updateNchnlsDevices()
            getVar("gainSlider").SetValue(presetData["gainSlider"])
            getVar("audioServer").setAmp(presetData["gainSlider"])
        getVar("presetPanel").setLabel(preset)
        getVar("grapher").getPlotter().draw()
        setVar("currentModule", currentModule)
        getVar("grapher").setTotalTime(getVar("totalTime"))

        if restore_globals:
            callAfter(_ownedPresetGraphs, owner, presetData)

def _ownedPresetGraphs(owner, data):
    if owner in session.modules and owner.editor is not None:
        with instance_context(owner):
            againForPluginKnobs(data)


### This is a hack to ensure that plugin knob automations are drawn in the grapher.
### Called within a wx.CallAfter to be executed after callAfter(getControlPanel().setPlugins).
def againForPluginKnobs(presetData):
    if 'userGraph' in presetData:
        graphDict = presetData['userGraph']
        for line in graphDict:
            for i, graphLine in enumerate(getVar("grapher").getPlotter().getData()):
                if line == graphLine.getName():
                    graphLine.setLineState(graphDict[line])
                    break
        del graphDict
        getVar("grapher").getPlotter().draw()
        getVar("grapher").setTotalTime(getVar("totalTime"))

def capturePresetData():
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
                widgetDict[str(i)] = ['None', [0, 0, 0, 0], [[0, 0, None], [0, 0, None], [0, 0, None]]]
            else:
                widgetDict[str(i)] = [plugin.getName(), plugin.getParams(), plugin.getStates()]
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

    return presetDict


def savePresetToFile(presetName):
    presetDict = capturePresetData()
    if getVar("interface"):
        if presetName == "init":
            setVar("initPreset", deepCopy(presetDict))
        else:
            with open(os.path.join(PRESETS_PATH, getVar('currentModuleName'), presetName), "w") as presetFile:        
                msg = xmlrpclib.dumps((presetDict, ), allow_none=True)
                presetFile.write(msg)

def completeUserInputsDict():
    for i in getVar("userInputs"):
        try:
            getVar("userInputs")[i]['mode'] = getControlPanel().getCfileinFromName(i).getMode()
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
        except:
            pass
    return copy.deepcopy(getVar("userInputs"))

def updateInputsFromDict():
    for name, info in list(getVar('userInputs').items()):
        widget = getControlPanel().getCfileinFromName(name)
        if widget is None:
            continue
        saved = copy.deepcopy(info)
        if os.path.isfile(saved.get('path', '')):
            widget.updateMenuFromPath(saved['path'])
        widget.onChangeMode(saved.get('mode', 0))
        frame = widget.getSamplerFrame()
        if saved.get('path') or saved.get('mode', 0) != 0:
            for key, setter in (('loopMode', 'setLoopMode'), ('loopX', 'setLoopX'),
                                ('loopIn', 'setLoopIn'), ('loopOut', 'setLoopOut'),
                                ('gain', 'setGain'), ('transp', 'setTransp'),
                                ('startFromLoop', 'setStartFromLoop')):
                if key in saved and hasattr(frame, setter):
                    getattr(frame, setter)(saved[key])
            if 'off' + name in saved:
                widget.setOffset(saved['off' + name])
        # Input initialization callbacks update the dict; retain the saved settings.
        getVar('userInputs')[name].update(saved)

###### Open / Save / Close ######
def saveCompileBackupFile(cecFilePath):
    with open(cecFilePath, "r") as f:
        _module = f.read()
    with open(MODULE_COMPILE_BACKUP_PATH, "w") as f:
        f.write(_module)

def saveRuntimeBackupFile(cecFilePath):
    with open(cecFilePath, "r") as f:
        _module = f.read()
    with open(MODULE_RUNTIME_BACKUP_PATH, "w") as f:
        f.write(_module)

def saveCeciliaFile(parent):
    wildcard = "Cecilia file (*.%s)|*.%s" % (FILE_EXTENSION, FILE_EXTENSION)
    fileToSave = saveFileDialog(parent, wildcard, 'Save')
    if not fileToSave:
        return
    else:
        if not fileToSave.endswith(FILE_EXTENSION):
            fileToSave = "%s.%s" % (fileToSave, FILE_EXTENSION)

    savePresetToFile("last save")

    curfile = codecs.open(getVar("currentCeciliaFile", unicode=True), "r", encoding="utf-8")
    curtext = curfile.read()
    curfile.close()

    try:
        file = codecs.open(fileToSave, "w", encoding="utf-8")
    except IOError:
        setVar("canGrabFocus", False)
        dlg = wx.MessageDialog(parent, 'Please verify permissions and write access on the file and try again.',
                            '"%s" could not be opened for writing' % (fileToSave), wx.OK | wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.Destroy()
            setVar("canGrabFocus", True)
            return

    file.write(curtext.rstrip())
    file.close()

    oldModuleName = os.path.split(getVar("currentCeciliaFile"))[1]
    oldModuleName = os.path.splitext(oldModuleName)[0]
    newModuleName = os.path.split(fileToSave)[1]
    newModuleName = os.path.splitext(newModuleName)[0]
    if not os.path.isdir(os.path.join(PRESETS_PATH, newModuleName)):
        os.mkdir(os.path.join(PRESETS_PATH, newModuleName))
    for f in os.listdir(os.path.join(PRESETS_PATH, oldModuleName)):
        shutil.copyfile(os.path.join(PRESETS_PATH, oldModuleName, f), os.path.join(PRESETS_PATH, newModuleName, f))

    setVar("builtinModule", False)
    setVar('currentModuleName', newModuleName)
    setVar("currentCeciliaFile", fileToSave)
    setVar("lastCeciliaFile", fileToSave)

    if getVar("mainFrame") is not None:
        getVar("mainFrame").newRecent(fileToSave)

    saveCompileBackupFile(fileToSave)

def confirmFirstStageInsertion(parent, candidate):
    name = candidate.state['currentModuleName']
    with wx.MessageDialog(parent or getVar('interface'),
                          '%s needs a compatible live stream input to run downstream. '
                          'Insert it as the first stage of this chain?' % name,
                          'Insert module as first stage?',
                          wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) as dialog:
        dialog.SetYesNoLabels('Insert as first stage', 'Cancel')
        return dialog.ShowModal() == wx.ID_YES


def confirmFirstStageReplacement(parent, current, candidate):
    with wx.MessageDialog(parent or getVar('interface'),
                          '%s and %s can only run as the first stage. '
                          'Replace %s with %s and keep the rest of the chain?' %
                          (current.state['currentModuleName'], candidate.state['currentModuleName'],
                           current.state['currentModuleName'], candidate.state['currentModuleName']),
                          'Replace first stage?',
                          wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) as dialog:
        dialog.SetYesNoLabels('Replace first stage', 'Cancel')
        return dialog.ShowModal() == wx.ID_YES


def openCeciliaFile(parent, openfile=None, builtin=False, replace=False, new_session=False):
    if not openfile:
        wildcard = "Cecilia file (*.%s)|*.%s" % (FILE_EXTENSION, FILE_EXTENSION)
        with wx.FileDialog(parent, message='Choose a Cecilia module to add…',
                           defaultDir=getVar('openFilePath'), wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() != wx.ID_OK:
                return False
            openfile = dialog.GetPath()
            setVar('openFilePath', os.path.dirname(openfile))
    server = getVar('audioServer')
    if server.isAudioServerRunning():
        if replace:
            showErrorDialog('Stop playback', 'Stop playback before reloading a module.')
            return False
        stopCeciliaSound()
    old = session.selected if replace else None
    old_snapshot = None
    insert_first = False
    if old:
        with instance_context(old):
            old_snapshot = capturePresetData()
    try:
        candidate = server.compileModule(openfile, builtin, old.id if old else None)
        proposed = ([candidate] if new_session else
                    [candidate if m is old else m for m in session.modules] if old else session.modules + [candidate])
        if not new_session and old is None and session.modules and candidate.primary_input is None:
            first = session.modules[0]
            if first.primary_input is None:
                proposed = [candidate] + session.modules[1:]
                session.validate_order(proposed)
                if not confirmFirstStageReplacement(parent, first, candidate):
                    return False
                old = first
            else:
                session.validate_order([candidate] + session.modules)
                if not confirmFirstStageInsertion(parent, candidate):
                    return False
                proposed = [candidate] + session.modules
                insert_first = True
        session.validate_order(proposed)
    except Exception as error:
        showErrorDialog('Could not add module', str(error))
        return False
    if new_session and session.modules:
        if captureSession() == session.saved_snapshot:
            with wx.MessageDialog(parent, 'Close the current session and open this module in a new session?',
                                  'Open module', wx.OK | wx.CANCEL | wx.ICON_QUESTION) as dialog:
                if dialog.ShowModal() != wx.ID_OK:
                    return False
        elif not confirmSessionDiscard(parent, 'Close the current session and open this module in a new session?\nSave changes before closing?'):
            return False
    remembered = []
    if getVar('rememberedSound') and session.modules:
        remembered = [w.filePath for w in session.modules[0].inputs.cfileinList if w.filePath]
    server.cleanup_module()
    frame = getVar('interface')
    previous_modules, previous_selected = list(session.modules), session.selected_id
    try:
        os.makedirs(os.path.join(PRESETS_PATH, candidate.state['currentModuleName']), exist_ok=True)
        if frame is not None:
            from .ChainUI import ModuleEditor
            ModuleEditor(frame, candidate)
        # Commit only after compilation, routing validation and editor creation.
        if new_session:
            session.modules = []
            session.selected_id = None
            session.append(candidate)
        elif old:
            session.replace(old, candidate)
        else:
            session.append(candidate, first=insert_first)
        if frame is None:
            from .CeciliaInterface import CeciliaInterface
            frame = CeciliaInterface(None, mainFrame=getVar('mainFrame'))
        else:
            from . import ChainUI
            ChainUI.refresh(frame)
        if new_session:
            frame.controlPanel.setPlugins({})
        with instance_context(candidate):
            if candidate is session.modules[0]:
                for widget, path in zip(candidate.inputs.cfileinList, remembered):
                    widget.onLoadFile(path)
            if old_snapshot is None and os.path.isfile(os.path.join(PRESETS_PATH, candidate.state['currentModuleName'], 'last save')):
                loadPresetFromFile('last save')
            if old_snapshot is not None:
                # Reload keeps the existing values that still match the interface.
                restorePresetData(old_snapshot, 'reload', False, True)
        if insert_first:
            ChainUI.transfer_effect_graphs(previous_modules[0], candidate)
        if old:
            if previous_modules and old is previous_modules[0]:
                ChainUI.transfer_effect_graphs(old, candidate)
            old.editor.destroy()
        elif len(session.modules) == 1:
            for plugin in getVar('plugins'):
                if plugin is not None:
                    frame.controlPanel.createGrapherLines(plugin)
        if new_session:
            from . import ChainUI
            for previous in previous_modules:
                previous.editor.destroy()
            session.path = session.saved_snapshot = None
            session.view = 'graph'
            ChainUI.refresh(frame)
        setVar('lastCeciliaFile', candidate.path)
        getVar('mainFrame').newRecent(candidate.path)
        getVar('mainFrame').Hide()
        frame.Raise()
        return True
    except Exception as error:
        # UI initialization failures are reported without replacing an existing chain.
        session.modules, session.selected_id = previous_modules, previous_selected
        if frame is not None:
            from . import ChainUI
            ChainUI.refresh(frame)
        if candidate.editor:
            candidate.editor.destroy()
        showErrorDialog('Could not create module editor', str(error))
        return False


def closeCeciliaFile(parent):
    frame = getVar('interface')
    if frame is not None:
        if session.selected is not None:
            with instance_context(session.selected):
                savePresetToFile('last save')
        getVar('audioServer').cleanup_module()
        frame.destroySessionWindow()
    session.modules = []
    session.selected_id = None
    vars.CeciliaVar['currentCeciliaFile'] = ''


def _stopped():
    if getVar('audioServer').isAudioServerRunning():
        showErrorDialog('Stop playback', 'Stop playback before changing the chain.')
        return False
    return True


def _rememberFirstInput(previous, current):
    if previous is current or not getVar('rememberedSound'):
        return
    paths = [widget.filePath for widget in previous.inputs.cfileinList
             if os.path.isfile(widget.filePath)]
    with instance_context(current):
        for widget, path in zip(current.inputs.cfileinList, paths):
            widget.onLoadFile(path)


def removeChainModule(module):
    if not _stopped():
        return
    from . import ChainUI
    previous_first = session.modules[0]
    try:
        session.validate_order([m for m in session.modules if m is not module])
    except ValueError as error:
        showErrorDialog('Cannot remove stage', str(error))
        return
    getVar('audioServer').cleanup_module()
    if len(session.modules) == 1:
        getVar('interface').controlPanel.setPlugins({})
    session.remove(module)
    if session.modules:
        _rememberFirstInput(previous_first, session.modules[0])
        ChainUI.transfer_effect_graphs(previous_first, session.modules[0])
    ChainUI.refresh(getVar('interface'))
    module.editor.destroy()


def moveChainModule(module, direction):
    if not _stopped():
        return
    from . import ChainUI
    previous_first = session.modules[0]
    try:
        session.move(module, direction)
    except ValueError as error:
        showErrorDialog('Cannot move stage', str(error))
        return
    getVar('audioServer').cleanup_module()
    _rememberFirstInput(previous_first, session.modules[0])
    ChainUI.transfer_effect_graphs(previous_first, session.modules[0])
    ChainUI.refresh(getVar('interface'))


def captureSession():
    modules = []
    plugins = {}
    effect_graphs = {}
    for module in session.modules:
        with instance_context(module):
            settings = capturePresetData()
            if module is session.modules[0]:
                plugins = settings['plugins']
            for key in ('plugins', 'totalTime', 'nchnls', 'gainSlider'):
                settings.pop(key, None)
            # Shared effects automation lives on the first editor's graph.
            for line in module.state['grapher'].plotter.getData():
                if line.slider is not None and line.slider.widget_type == 'plugin_knob':
                    effect_graphs[line.getName()] = settings['userGraph'].pop(line.getName(), None)
            modules.append({'id': module.id, 'module_path': module.path,
                            'builtin': module.state['builtinModule'],
                            'preset': module.state['presetPanel'].currentPreset,
                            'settings': settings})
    snapshot = {'modules': modules, 'selected_id': session.selected_id, 'view': session.view,
            'output': {'totalTime': getVar('totalTime'), 'nchnls': getVar('nchnls'),
                       'gainSlider': getVar('gainSlider').GetValue() if getVar('gainSlider') else 0,
                       'audioFileType': getVar('audioFileType'), 'sampSize': getVar('sampSize'),
                       'output_path': getControlPanel().outputFilename if getVar('interface') else '',
                       'startOffset': getVar('startOffset'),
                       'plugins': plugins, 'userGraph': effect_graphs}}
    # Normalize tuples from legacy widget states to the JSON representation.
    return normalize_snapshot(json.loads(json.dumps(snapshot, allow_nan=False)))


def rememberChainSession(path):
    path = os.path.abspath(path)
    try:
        with open(RECENT_SESSION_PATH, encoding='utf-8') as stream:
            paths = [line.strip() for line in stream if line.strip()]
    except OSError:
        paths = []
    paths = [path] + [entry for entry in paths if entry != path]
    with open(RECENT_SESSION_PATH, 'w', encoding='utf-8') as stream:
        stream.writelines(entry + '\n' for entry in paths[:10])
    for frame in (getVar('mainFrame'), getVar('interface')):
        if frame is not None:
            frame.menubar.refreshRecentSessionMenu()
    if getVar('interface') is not None:
        from .ChainUI import update_title
        update_title(getVar('interface'))


def saveChainSession(parent, path=None):
    from .Session import write_session
    if path is None:
        path = session.path
    if not path:
        with wx.FileDialog(parent, message='Save Cecilia chain', wildcard='Cecilia chain (*.c5chain)|*.c5chain',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dialog:
            if dialog.ShowModal() != wx.ID_OK:
                return False
            path = dialog.GetPath()
    if not path.endswith('.c5chain'):
        path += '.c5chain'
    try:
        snapshot = captureSession()
        write_session(path, snapshot)
    except Exception as error:
        showErrorDialog('Could not save session', str(error))
        return False
    session.path = path
    session.saved_snapshot = snapshot
    rememberChainSession(path)
    return True


def confirmSessionDiscard(parent, message='Save changes to the chain session?'):
    if not session.modules and session.saved_snapshot is None:
        return True
    if captureSession() == session.saved_snapshot:
        return True
    with wx.MessageDialog(parent, message, 'Unsaved session',
                          wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION) as dialog:
        answer = dialog.ShowModal()
    if answer == wx.ID_CANCEL:
        return False
    return answer == wx.ID_NO or saveChainSession(parent)


def newChainSession(parent):
    if not _stopped() or not confirmSessionDiscard(parent):
        return False
    getVar('audioServer').cleanup_module()
    frame = getVar('interface')
    if frame is not None:
        from . import ChainUI
        if session.modules:
            frame.controlPanel.setPlugins({})
        ChainUI.destroy_editors(frame)
        session.modules = []
        session.selected_id = None
        session.view = 'chain'
        session.path = session.saved_snapshot = None
        ChainUI.refresh(frame)
    else:
        session.modules = []
        session.selected_id = None
        session.view = 'chain'
        session.path = session.saved_snapshot = None
    return True


def _restoreSessionOutput(frame, output):
    setVar('totalTime', float(output['totalTime']))
    setVar('nchnls', int(output['nchnls']))
    setVar('audioFileType', output.get('audioFileType', 'aif'))
    setVar('sampSize', output.get('sampSize', 0))
    setVar('startOffset', output.get('startOffset', 0.0))
    filename = output.get('output_path', '')
    setVar('outputFile', filename)
    frame.controlPanel.outputFilename = filename
    frame.controlPanel.filenameLabel.setLabel(shortenName(os.path.basename(filename), frame.controlPanel.charNumForLabel))
    getVar('gainSlider').SetValue(output['gainSlider'])
    getVar('audioServer').setAmp(output['gainSlider'])
    frame.controlPanel.tmpTotalTime = getVar('totalTime')
    frame.controlPanel.updateDurationSlider()
    frame.controlPanel.updateNchnls()
    if session.modules:
        with instance_context(session.modules[0]):
            frame.controlPanel.setPlugins(output['plugins'])
            againForPluginKnobs(output)


def openChainSession(parent, path=None):
    from .Session import read_session
    from . import ChainUI
    if not _stopped():
        return False
    if path is None:
        with wx.FileDialog(parent, message='Open Cecilia chain', wildcard='Cecilia chain (*.c5chain)|*.c5chain',
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() != wx.ID_OK:
                return False
            path = dialog.GetPath()
    # Compile and validate the whole document before touching the active session.
    candidates = []
    try:
        document = read_session(path)
        errors = []
        for entry in document['modules']:
            if not os.path.isfile(entry['module_path']):
                errors.append('Missing module: ' + entry['module_path'])
                continue
            module = getVar('audioServer').compileModule(entry['module_path'], entry.get('builtin', False), entry['id'])
            candidates.append(module)
            for name, info in entry['settings'].get('userInputs', {}).items():
                required = name in module.auxiliary_inputs or (len(candidates) == 1 and info.get('mode', 0) == 0)
                if required and info.get('path') and not os.path.isfile(info['path']):
                    errors.append('Missing asset: ' + info['path'])
        if errors:
            raise ValueError('\n'.join(errors))
        session.validate_order(candidates)
        if document.get('selected_id') not in {m.id for m in candidates} and candidates:
            raise ValueError('Selected module is missing from the session.')
        output = document['output']
        if not 0 < float(output['totalTime']) <= 3600 or int(output['nchnls']) < 1:
            raise ValueError('Invalid output duration or channel count.')
        if document.get('view') not in ('graph', 'chain'):
            raise ValueError('Invalid session view.')
    except Exception as error:
        showErrorDialog('Could not open session', str(error))
        return False
    if not confirmSessionDiscard(parent):
        return False
    frame = getVar('interface')
    previous = list(session.modules)
    previous_selected, previous_view = session.selected_id, session.view
    previous_output = captureSession()['output']
    try:
        if frame is None:
            from .CeciliaInterface import CeciliaInterface
            frame = CeciliaInterface(None, mainFrame=getVar('mainFrame'))
        for module in candidates:
            os.makedirs(os.path.join(PRESETS_PATH, module.state['currentModuleName']), exist_ok=True)
            ChainUI.ModuleEditor(frame, module)
        # Restore values into parked editors before committing them to the grid.
        for module, entry in zip(candidates, document['modules']):
            with instance_context(module):
                restorePresetData(entry['settings'], entry.get('preset', 'init'), False, True)
        getVar('audioServer').cleanup_module()
        if not candidates and session.modules:
            frame.controlPanel.setPlugins({})
        session.modules = candidates
        session.selected_id = document.get('selected_id')
        session.view = document.get('view', 'graph')
        _restoreSessionOutput(frame, output)
        ChainUI.refresh(frame)
        snapshot = captureSession()
        for module in previous:
            module.editor.destroy()
        session.path = path
        session.saved_snapshot = snapshot
        rememberChainSession(path)
        frame.Raise()
        getVar('mainFrame').Hide()
        return True
    except Exception as error:
        session.modules, session.selected_id, session.view = previous, previous_selected, previous_view
        _restoreSessionOutput(frame, previous_output)
        for module in candidates:
            if module.editor:
                module.editor.destroy()
        ChainUI.refresh(frame)
        showErrorDialog('Could not restore session', str(error))
        return False


###### Interface creation utilities ######
def resetWidgetVariables():
    setVar("gainSlider", None)
    setVar("plugins", [None] * NUM_OF_PLUGINS)
    setVar("userInputs", {})
    for slider in getVar("userSliders"):
        slider.cleanup()
    setVar("userSliders", [])
    setVar("userSamplers", [])
    setVar("userTogglePopups", [])
    setVar("samplerSliders", [])
    setVar("samplerTogglePopup", [])
    getVar("presetPanel").cleanup()
    getVar("presetPanel").parent = None
    setVar("presetPanel", None)
    getVar("grapher").parent = None
    setVar("grapher", None)
    setVar("tooltips", [])

def parseInterfaceText():
    interfaceWidgets = getVar("interfaceWidgets")
    return interfaceWidgets

def updateNchnlsDevices():
    try:
        getVar("interface").updateNchnls()
    except:
        pass

def deepCopy(ori):
    if type(ori) is dict:
        new = {}
        for key in ori:
            new[key] = deepCopy(ori[key])
        return new
    elif type(ori) is list:
        new = []
        for data in ori:
            new.append(deepCopy(data))
        return new
    elif type(ori) is tuple:
        new = []
        for data in ori:
            new.append(deepCopy(data))
        return new
    else:
        return ori
    return new

###### Conversion functions #######
def interpFloat(t, v1, v2):
    "interpolator for a single value; interprets t in [0-1] between v1 and v2"
    return (v2 - v1) * t + v1

def tFromValue(value, v1, v2):
    "returns a t (in range 0-1) given a value in the range v1 to v2"
    return (value - v1) / (v2 - v1)

def clamp(v, minv, maxv):
    "clamps a value within a range"
    if v < minv: v = minv
    if v > maxv: v = maxv
    return v

def toLog(t, v1, v2):
    v1 = float(v1)
    return math.log10(t / v1) / math.log10(v2 / v1)

def toExp(t, v1, v2):
    return math.pow(10, t * (math.log10(v2) - math.log10(v1)) + math.log10(v1))

###### Utility functions #######
def autoRename(path, index=0, wrap=False):
    if os.path.exists(path):
        file = ensureNFD(os.path.split(path)[1])
        if wrap:
            name = ensureNFD(file.rsplit('.', 1)[0])[:-4]
        else:
            name = ensureNFD(file.rsplit('.', 1)[0])
        ext = file.rsplit('.', 1)[1]

        if len(name) >= 5:
            if name[-4] == '_' and name[-3:].isdigit():
                name = name[:-4]
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

def checkForPresetsInCeciliaFile(filepath):
    PRESETS_DELIMITER = "####################################\n" \
                        "##### Cecilia reserved section #####\n" \
                        "#### Presets saved from the app ####\n" \
                        "####################################\n"

    mylocals = {}
    rewrite = False

    with open(filepath, "r") as f:
        text = f.read()
        if PRESETS_DELIMITER in text:
            rewrite = True
            newtext = text[:text.find(PRESETS_DELIMITER) - 1]
            text = text[text.find(PRESETS_DELIMITER) + len(PRESETS_DELIMITER) + 1:]
            if text.strip() != "":
                exec(text, globals(), mylocals)

                presetsDir = os.path.join(PRESETS_PATH, getVar("currentModuleName")) 
                if not os.path.isdir(presetsDir):
                    os.mkdir(presetsDir)

                for preset in mylocals["CECILIA_PRESETS"]:
                    for key in list(mylocals["CECILIA_PRESETS"][preset]["plugins"]):
                        mylocals["CECILIA_PRESETS"][preset]["plugins"][str(key)] = mylocals["CECILIA_PRESETS"][preset]["plugins"][key]
                        del mylocals["CECILIA_PRESETS"][preset]["plugins"][key]
                    msg = xmlrpclib.dumps((mylocals["CECILIA_PRESETS"][preset], ), allow_none=True)
                    with open(os.path.join(presetsDir, preset), "w") as fw:
                        fw.write(msg)
    if rewrite:
        with open(filepath, "w") as f:
            f.write(newtext)
