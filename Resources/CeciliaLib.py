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

import os, sys, wx, re, time, math, copy, codecs, ast
from types import UnicodeType, ListType, TupleType, IntType
import pprint as pp
from constants import *
import Variables as vars
from API_interface import *
import unicodedata
from subprocess import Popen

def setVar(var, value):
    vars.CeciliaVar[var] = value

def getVar(var, unicode=False):
    if unicode:
        return ensureNFD(vars.CeciliaVar[var])
    else:
        return vars.CeciliaVar[var]

def setJackParams(client = None, inPortName = None, outPortName = None):
    if not client==None:
        vars.CeciliaVar['jack']['client'] = client
    if not inPortName==None:
        vars.CeciliaVar['jack']['inPortName'] = inPortName
    if not outPortName==None:
        vars.CeciliaVar['jack']['outPortName'] = outPortName

def setPlugins(x, pos):
    vars.CeciliaVar['plugins'][pos] = x

def getDayTime():
    time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

def getControlPanel():
    return getVar('interface').getControlPanel()

def writeVarToDisk():
    vars.writeCeciliaPrefsToFile()

###### Start / Stop / Drivers ######
def startCeciliaSound(timer=True):
    # Check if soundfile is loaded
    # if 0: # no sound...
    #     showErrorDialog('No input sound file!', 'Please load one...')
    #     for key in getVar("userInputs").keys():
    #         if not os.path.isfile(getVar("userInputs")[key]['path']):
    #             getControlPanel().getCfileinFromName(key).onLoadFile()
    #     stopCeciliaSound()
    #     return
    getControlPanel().resetMeter()
    getVar("audioServer").shutdown()
    getVar("audioServer").reinit()
    getVar("audioServer").boot()
    if getVar("currentModuleRef") != None:
        getVar("audioServer").loadModule(getVar("currentModuleRef"))
    else:
        showErrorDialog("Wow...!", "No module to load.")
    getVar("grapher").toolbar.convertSlider.Hide()
    getVar("presetPanel").presetChoice.setEnable(False)
    getControlPanel().durationSlider.setEnable(False)
    getVar("audioServer").start(timer=timer)
    getVar("grapher").toolbar.loadingMsg.SetForegroundColour(TITLE_BACK_COLOUR)

def stopCeciliaSound():
    getVar("audioServer").stop()
    if getVar("currentModule") != None:
        getVar("audioServer").checkForAutomation()
        getVar("currentModule")._checkForAutomation()
        getVar("grapher").checkForAutomation()
    time.sleep(.25)
    if getVar('interface') != None:
        getControlPanel().transportButtons.setPlay(False)
        getControlPanel().transportButtons.setRecord(False)
        getVar("presetPanel").presetChoice.setEnable(True)
        getControlPanel().durationSlider.setEnable(True)
        wx.CallAfter(getControlPanel().vuMeter.reset)

def resetControls():
    if getVar('interface') != None:
        getControlPanel().transportButtons.setPlay(False)
        getControlPanel().transportButtons.setRecord(False)
        getVar("presetPanel").presetChoice.setEnable(True)
        wx.CallAfter(getControlPanel().vuMeter.reset)
    
def audioServerIsRunning(state):
    if state == 1:
        if getVar("interface"):
            getControlPanel().transportButtons.setPlay(True)

def queryAudioMidiDrivers():
    inputs, selectedInput, outputs, selectedOutput, midiInputs, selectedMidiInput = getVar("audioServer").getAvailableAudioMidiDrivers()

    setVar("availableAudioOutputs",  outputs)
    if getVar("audioOutput") < len(outputs):
        setVar("audioOutput", getVar("audioOutput"))
    else:
        try:
            setVar("audioOutput", outputs.index(selectedOutput))
        except:
            setVar("audioOutput", 0)

    setVar("availableAudioInputs", inputs)
    if getVar("audioInput") < len(inputs):
        setVar("audioInput", getVar("audioInput"))
    else:
        try:
            setVar("audioInput", inputs.index(selectedInput))
        except:
            setVar("audioInput", 0)

    if midiInputs == []:
        setVar("useMidi", 0)
    else:
        setVar("useMidi", 1)
    setVar("availableMidiInputs", midiInputs)
    if getVar("midiDeviceIn") <= len(midiInputs):
        setVar("midiDeviceIn", getVar("midiDeviceIn"))
    else:
        try:
            setVar("midiDeviceIn", midiInputs.index(selectedMidiInput))
        except:
            setVar("midiDeviceIn", 0)

###### Dialogs ######
def openDirDialog(parent, path='/'):
    dirDialog = wx.DirDialog(parent, message='Choose folder', defaultPath=path, style=wx.DD_DEFAULT_STYLE)
    if dirDialog.ShowModal() == wx.ID_OK:
        dirPath = dirDialog.GetPath()
    else:
        dirPath = None
    dirDialog.Destroy()
    return dirPath

def openAudioFileDialog(parent, wildcard, type='open', defaultPath='/'):
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
                                 defaultDir=defaultPath, defaultFile=defaultFile+ext,
                                 wildcard=wildcard, style=wx.SAVE | wx.FD_OVERWRITE_PROMPT)
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
                    "All files (*.*)|*.*"
    elif getVar("systemPlatform")  == 'darwin':
        wildcard =  "Application files (*.app)|*.app|"     \
                    "All files (*.*)|*.*"
    else:
        wildcard = "All files (*.*)|*.*"
    
    path = ''
    dlg = wx.FileDialog(None, message="Choose a soundfile %s..." % app_type,
                             defaultDir=os.path.expanduser('~'),
                             wildcard=wildcard, style=wx.OPEN)

    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()   
    dlg.Destroy()

    if path:
        if app_type == 'player':
            setVar("soundfilePlayer", path)
        elif app_type == 'editor':
            setVar("soundfileEditor", path)

def listenSoundfile(soundfile):
    if getVar("soundfilePlayer") == '':
        showErrorDialog("Preferences not set", "Choose a soundfile player first.")
        loadPlayerEditor('player')
    if os.path.isfile(soundfile):
        app = slashifyText(getVar("soundfilePlayer"))
        soundfile = slashifyText(soundfile)
        if getVar("systemPlatform")  == 'darwin':
            cmd = 'open -a %s %s' % (app ,soundfile)
            Popen(cmd, shell=True)
        elif getVar("systemPlatform")  == 'win32':
            cmd = 'start /NORMAL %s "%s"' % (app, soundfile)
            try:
                Popen(cmd, shell=True)
            except OSError, OSError2:
                print 'Unable to open desired software:\t' + app
        else:
            cmd = '%s %s' % (app, soundfile)
            try:
                Popen(cmd, shell=True)
            except OSError, OSError2:
                print 'Unable to open desired software:\t' + app

def editSoundfile(soundfile):
    if getVar("soundfileEditor") == '':
        showErrorDialog("Preferences not set", "Choose a soundfile editor first.")
        loadPlayerEditor('editor')
    if os.path.isfile(soundfile):
        app = slashifyText(getVar("soundfileEditor"))
        soundfile = slashifyText(soundfile)
        if getVar("systemPlatform")  == 'darwin':
            cmd = 'open -a %s %s' % (app ,soundfile)
            Popen(cmd, shell=True)
        elif getVar("systemPlatform")  == 'win32':
            cmd = 'start /NORMAL %s "%s"' % (app, soundfile)
            try:
                Popen(cmd, shell=True)
            except OSError, OSError2:
                print 'Unable to open desired software:\t' + app
        else:
            cmd = '%s %s' % (app, soundfile)
            try:
                Popen(cmd, shell=True)
            except OSError, OSError2:
                print 'Unable to open desired software:\t' + app

###### Preset functions ######
def deletePreset(preset):
    del vars.CeciliaVar['presets'][preset]

def loadPresetFromDict(preset):
    currentModule = getVar("currentModule")
    setVar("currentModule", None)
    if getVar("presets").has_key(preset) or preset == "init":
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
                else:
                    if ok:
                        setVar("userInputs", copy.deepcopy(presetData[data]))
                        updateInputsFromDict()
                    else:
                        pass
            elif data == 'userSliders':
                slidersDict = presetData[data]
                for slider in getVar("userSliders"):
                    if slider.getName() in slidersDict:
                        slider.setState(slidersDict[slider.getName()])
                del slidersDict
            elif data == 'plugins':
                pluginsDict = copy.deepcopy(presetData[data])
                getControlPanel().setPlugins(pluginsDict)
                del pluginsDict
            elif data == 'userTogglePopups':
                togDict = presetData[data]
                for widget in getVar("userTogglePopups"):
                    if widget.getName() in togDict:
                        widget.setValue(togDict[widget.getName()], True)
                del togDict
            else:
                continue
        if presetData.has_key('userGraph'):
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
            if plugin == None:
                widgetDict[i] = ['None', [0,0,0,0],[[0,0,None],[0,0,None],[0,0,None]]]
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
            if line.slider == None:
                graphDict[line.getName()] = line.getLineState()
            else:
                outvalue = line.slider.getValue()
                if line.slider.widget_type in ["slider", "plugin_knob"]:
                    graphDict[line.getName()] = line.getLineState()
                elif line.slider.widget_type == "range":
                    ends = ['min', 'max']
                    for i in range(len(outvalue)):
                        if line.getLabel().endswith(ends[i]):
                            graphDict[line.getName()+ends[i]] = line.getLineState()
                            break
                elif line.slider.widget_type == "splitter":
                    for i in range(len(outvalue)):
                        if line.getLabel().endswith("%d" % i):
                            graphDict[line.getName()+"_%d" % i] = line.getLineState()
                            break
        presetDict['userGraph'] = copy.deepcopy(graphDict)
        del graphDict

    if presetName == "init":
        setVar("initPreset", presetDict)
    else:
        getVar("presets")[presetName] = presetDict
        setVar("isModified", True)

def completeUserInputsDict():
    for i in getVar("userInputs"):
        if getVar("userInputs")[i]['type'] == 'csampler':
            cfilein = getControlPanel().getCfileinFromName(i)
            getVar("userInputs")[i]['off'+cfilein.getName()] = cfilein.getOffset()
            getVar("userInputs")[i]['loopMode'] = cfilein.getSamplerInfo()['loopMode']
            getVar("userInputs")[i]['startFromLoop'] = cfilein.getSamplerInfo()['startFromLoop']
            getVar("userInputs")[i]['loopX'] = cfilein.getSamplerInfo()['loopX']
            getVar("userInputs")[i]['loopIn'] = cfilein.getSamplerInfo()['loopIn']
            getVar("userInputs")[i]['loopOut'] = cfilein.getSamplerInfo()['loopOut']
            getVar("userInputs")[i]['gain'] = cfilein.getSamplerInfo()['gain']
            getVar("userInputs")[i]['transp'] = cfilein.getSamplerInfo()['transp']
        elif getVar("userInputs")[i]['type'] == 'cfilein':
            cfilein = getControlPanel().getCfileinFromName(i)
            getVar("userInputs")[i]['off'+cfilein.getName()] = cfilein.getOffset()
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
                elif k == ('off'+input):
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
        if dlg.ShowModal()==wx.ID_OK:
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
                                    defaultDir=defaultPath, wildcard=wildcard, style=wx.OPEN)
        if openDialog.ShowModal() == wx.ID_OK:
            cecFilePath = openDialog.GetPath()
            setVar("openFilePath", (os.path.split(cecFilePath)[0]))
        else:
            cecFilePath = None
        openDialog.Destroy()

        if cecFilePath == None:
            return

    else:
        cecFilePath = openfile

    if getVar("audioServer").isAudioServerRunning():
        stopCeciliaSound()

    snds = []
    if getVar("rememberedSound") and getVar("interfaceWidgets") and getVar("userInputs"):
        names = [d['name'] for d in getVar("interfaceWidgets")]
        keys = getVar("userInputs").keys()
        sortlist = zip([names.index(k) for k in keys], keys)
        sortlist.sort()
        index, keys = zip(*sortlist)
        for key in keys:
            if getVar("userInputs")[key]['path'] != '':
                snds.append(getVar("userInputs")[key]['path'])

    if not closeCeciliaFile(parent):
        return

    getVar("mainFrame").Hide()

    setVar("builtinModule", builtin)
    setVar("currentCeciliaFile", cecFilePath)
    parent.newRecent(cecFilePath)
    after = wx.CallLater(200, setVar("isModified", False))

    moduleInfo = ''

    setVar("isModified", False)

    getVar("audioServer").openCecFile(cecFilePath)

    if getVar("interface"):
        for i, cfilein in enumerate(getControlPanel().getCfileinList()):
            if i >= len(snds):
                break
            cfilein.onLoadFile(snds[i])

    savePresetToDict("init")

    if getVar("presets").has_key("last save"):
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
    setVar("moduleDescription", '')
    for widget in interfaceWidgets:
        if widget['type'] == 'cmodule':
            setVar("moduleDescription", widget['label'])
            break
    return interfaceWidgets

def updateNchnlsDevices():
    try:
        getVar("interface").updateNchnls()
    except:
        pass

###### Interpolation functions ######
def interpolate(lines, size, listlen):
   scale = size / lines[-1][0]
   templist = []
   for i in range(listlen-1):
       t = lines[i+1][0] - lines[i][0]
       num = int(round(t * scale))
       if num == 0:
           pass
       else:
           step = (lines[i+1][1] - lines[i][1]) / num
           for j in range(num):
               templist.append(lines[i][1] + (step*j))
   return templist               

def interpolateCurved(lines, size, listlen):
    lines = removeDuplicates(lines)
    scale = size / float(len(lines))
    depth = int(round(scale))
    off = int(1. / (scale - depth))
    templist = []
    for i in range(len(lines)-1):
        num = depth
        if (i%off) == 0: num = depth + 1
        step = (lines[i+1][1] - lines[i][1]) / num
        for j in range(num):
            templist.append(lines[i][1] + (step*j))
    return templist

def interpolateLog(lines, size, listlen, yrange):
    scale = size / lines[-1][0]
    templist = []
    for i in range(listlen-1):
        t = lines[i+1][0] - lines[i][0]
        num = int(round(t * scale))
        if num == 0:
            pass
        else:
            step = (lines[i+1][1] - lines[i][1]) / num
            for j in range(num):
                templist.append(lines[i][1] + (step*j))
    list = []
    if yrange[0] == 0: yoffrange = .00001
    else: yoffrange = yrange[0] 
    totalRange = yrange[1] - yoffrange
    currentTotalRange = math.log10(yrange[1]/yrange[0])
    currentMin = math.log10(yrange[0])
    for p in templist:
        if p == 0: p = .00001
        ratio = (p - yoffrange) / totalRange
        list.append(math.pow(10, ratio * currentTotalRange + currentMin))
    return list

###### Utility functions #######
def removeExtraSpace(text):
    li = text.split(' ')
    text = ''
    for ele in li:
        if ele != '':
            text += ele + ' '
    return text

def removeDuplicates(seq): 
   result = []
   for item in seq:
       if item not in result:
           result.append(item)
   return result

def convertWindowsPath(path):
    if getVar("systemPlatform")  == 'win32':
        return os.path.normpath(path)
    else:
        return path

def slashifyText(text):
    charsToSlashify = [' ', '(', ')']
    newText = ''
    for i in range(len(text)):
        char = text[i]
        if char in charsToSlashify:
            char = '\\' + char
        newText += char
    return newText

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
                if name[-4] == '_' and type(eval(name[-3:])) == IntType:
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
        return autoRename(newPath, index+1, True)
    else:
        newPath = path
    return newPath

def shortenName(name,maxChar):
    name = ensureNFD(name)
    if len(name)>maxChar:
        shortenChar = '...'
        addSpace = 0
        charSpace = (maxChar-len(shortenChar)) / 2
        if (maxChar-5) % 2 != 0:
            addSpace = 1
        name = name[:charSpace+addSpace] + shortenChar + name[len(name)-charSpace:]
    return name

def ensureNFD(unistr):
    if getVar("systemPlatform") in ['linux2', 'win32']:
        encodings = [DEFAULT_ENCODING, ENCODING,
                     'cp1252', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    else:
        encodings = [DEFAULT_ENCODING, ENCODING,
                     'macroman', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    decstr = unistr
    if type(decstr) != UnicodeType:
        for encoding in encodings:
            try:
                decstr = decstr.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
            except:
                decstr = "UnableToDecodeString"
                print "Unicode encoding not in a recognized format..."
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
