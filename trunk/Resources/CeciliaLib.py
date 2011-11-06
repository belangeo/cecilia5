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

import os, sys, wx, re, time, math, copy, codecs, ast
from types import UnicodeType, ListType, TupleType, IntType
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
def startCeciliaSound():
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
        getVar("audioServer").loadModule()
    getVar("grapher").toolbar.convertSlider.Hide()
    getVar("audioServer").start()

def stopCeciliaSound():
    getVar("audioServer").stop()
    if getVar("currentModule") != None:
        getVar("audioServer").checkForAutomation()
        getVar("currentModule").checkForAutomation()
        getVar("grapher").checkForAutomation()
    time.sleep(.25)
    getControlPanel().transportButtons.setPlay(False)
    getControlPanel().transportButtons.setRecord(False)
    wx.CallAfter(getControlPanel().vuMeter.reset)

def audioServerIsRunning(state):
    if state == 1:
        if getVar("interface"):
            getControlPanel().transportButtons.setPlay(True)

def queryAudioMidiDrivers():
    inputs, selectedInput, outputs, selectedOutput, midiInputs, selectedMidiInput = getVar("audioServer").getAvailableAudioMidiDrivers()

    setVar("availableAudioOutputs",  outputs)
    if getVar("audioOutput") != '':
        if getVar("audioOutput") < len(outputs):
            setVar("audioOutput", getVar("audioOutput"))
        else:    
            setVar("audioOutput", outputs.index(selectedOutput))
    else:
        setVar("audioOutput", outputs.index(selectedOutput))

    setVar("availableAudioInputs", inputs)
    if getVar("audioInput") != '':
        if getVar("audioInput") < len(inputs):
            setVar("audioInput", getVar("audioInput"))
        else:    
            setVar("audioInput", inputs.index(selectedInput))
    else:    
        setVar("audioInput", inputs.index(selectedInput))

    if midiInputs == []:
        setVar("useMidi", 0)
    else:
        setVar("useMidi", 1)    
    setVar("availableMidiInputs", midiInputs)
    if getVar("midiDeviceIn") != '':
        if getVar("midiDeviceIn") <= len(midiInputs):
            setVar("midiDeviceIn", getVar("midiDeviceIn"))
        else:
            setVar("midiDeviceIn", midiInputs.index(selectedMidiInput))
    else:            
        setVar("midiDeviceIn", midiInputs.index(selectedMidiInput))

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
        filePath = openDialog.GetPath()
        setVar("openAudioFilePath", os.path.split(filePath)[0])
    else:
        filePath = None
    openDialog.Destroy()
    return filePath

def saveFileDialog(parent, wildcard, type='Save'):
    if type == 'Save audio':
        defaultPath = getVar("saveAudioFilePath", unicode=True)
    else:
        defaultPath = getVar("saveFilePath", unicode=True)
    
    defaultFile = os.path.split(getVar("currentCeciliaFile", unicode=True))[1].split(".")[0]
    ext = "." + getVar("audioFileType")
    saveAsDialog = wx.FileDialog(parent, message="%s file as ..." % type,
                                 defaultDir=defaultPath, defaultFile=defaultFile+ext,
                                 wildcard=wildcard, style=wx.SAVE | wx.FD_OVERWRITE_PROMPT)
    if saveAsDialog.ShowModal() == wx.ID_OK:
        filePath = saveAsDialog.GetPath()
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
    dlg = wx.FileDialog(self, message="Choose a soundfile %s..." % app_type,
                             defaultDir=os.path.expanduser('~'),
                             wildcard=wildcard,
                             style=wx.OPEN)

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
        CeciliaLib.showErrorDialog("Preferences not set", "Choose a soundfile editor first.")
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
    if getVar("presets").has_key(preset) or preset == "init":
        if preset == "init":
            presetData = getVar("initPreset")
        else:
            presetData = getVar("presets")[preset]
        for data in presetData.keys():
            if data == 'nchnls':
                setVar("nchnls", presetData[data])
                updateNchnlsDevices()
            elif data == 'duration':
                setVar("totalTime", presetData[data])
                getControlPanel().updateDurationSlider()
            elif data == 'userInputs':
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
        getVar("presetPanel").setLabel(preset)
        getVar("grapher").getPlotter().draw()
                
def savePresetToDict(presetName):
    presetDict = dict()
    presetDict['nchnls'] = getVar("nchnls")
    presetDict['duration'] = getVar("totalTime")
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
        ends = ['min', 'max']
        for line in getVar("grapher").getPlotter().getData():
            if line.slider == None:
                graphDict[line.getName()] = line.getLineState()
            else:        
                outvalue = line.slider.getValue()
                if type(outvalue) not in [ListType, TupleType]:
                    graphDict[line.getName()] = line.getLineState()
                else:
                    for i in range(len(outvalue)): 
                        if line.getLabel().endswith(ends[i]):
                            graphDict[line.getName()+ends[i]] = line.getLineState()
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
    if getVar("currentCeciliaFile", unicode=True) == '' or getVar("builtinModule"):
        wildcard = "Cecilia file (*.cec)|*.cec|" \
                   "All files (*.*)|*.*"
        fileToSave = saveFileDialog(parent, wildcard, 'Save')
        if not fileToSave:
            return False
        else:
            if not fileToSave.endswith('.cec'):
                fileToSave = fileToSave + '.cec'    
    else:
        fileToSave = getVar("currentCeciliaFile", unicode=True)
    
    try:
        file = open(fileToSave, 'wt')
    except IOError:
        dlg = wx.MessageDialog(parent, 'Please verify permissions and write access on the file and try again.',
                            '"%s" could not be opened for writing' % (fileToSave), 
                            wx.OK | wx.ICON_EXCLAMATION)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Destroy()
            return

    file.close()

    setVar("builtinModule", False)
    setVar("currentCeciliaFile", fileToSave)
    setVar("isModified", False)
    
    return True

def openCeciliaFile(parent, openfile=None, builtin=False):
    if not openfile:
        wildcard = "Cecilia file (*.cec)|*.cec|" \
                   "All files (*.*)|*.*"
        defaultPath = getVar("openFilePath", unicode=True)
        openDialog = wx.FileDialog(parent, message='Choose a file to %s' % type, 
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

    snds = []
    if getVar("rememberedSound"):
        for key in getVar("userInputs").keys():
            if getVar("userInputs")[key]['path'] != '':
                snds.append(getVar("userInputs")[key]['path'])

    if not closeCeciliaFile(parent):
        return

    getVar("mainFrame").Hide()

    if builtin:
        setVar("builtinModule", True)
    else:
        setVar("builtinModule", False)
    setVar("currentCeciliaFile", cecFilePath)
    parent.newRecent(cecFilePath)
    after = wx.CallLater(200, setVar("isModified", False))

    moduleInfo = ''

    setVar("isModified", False)

    # here we need to exec the file...
    getVar("audioServer").openCecFile(cecFilePath)

    print "------ 8 ------"
    if getVar("interface"):
        for i, cfilein in enumerate(getControlPanel().getCfileinList()):
            if i >= len(snds):
                break
            cfilein.onLoadFile(snds[i])
    print "------ 9 ------"
    
    if 0:
        if separatedText['Open'] != []:
            for line in separatedText['Open']:
                if 'totalTime' in line:
                    setTotalTime(float(line.strip().replace('totalTime=', '')))
                    getControlPanel().durationSlider.SetValue(float(line.strip().replace('totalTime=', '')))
                if 'masterVolume' in line:
                    getVar("gainSlider").SetValue(float(line.strip().replace('masterVolume=', '')))
                    
    savePresetToDict("init")
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
def createGrapherInst(line):
    data = line.getData()
    name = line.getName()
    log = line.getLog()
    yrange = line.getYrange()
    curved = line.getCurved()
    csoundPoints = line.getCsoundPoints()
    lines = line.getLines()
    types = line.getTypes()
    suffix = line.getSuffix()
    gen = line.getGen()
    size = line.getSize()

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
    if len(name)>maxChar:
        shortenChar = '...'
        addSpace = 0
        charSpace = (maxChar-len(shortenChar)) / 2
        if (maxChar-5) % 2 != 0:
            addSpace = 1
        name = name[:charSpace+addSpace] + shortenChar + name[len(name)-charSpace:]
    return name

def ensureNFD(unistr):
    if getVar("systemPlatform")  == 'win32':
        encodings = [ENCODING, 'cp1252', 'utf-8', 'iso-8859-1', 'utf-16']
        format = 'NFC'
    else:
        encodings = [ENCODING, 'utf-8', 'macroman', 'iso-8859-1', 'utf-16']
        format = 'NFD'
    if type(unistr) != UnicodeType:
        for encoding in encodings:
            try:
                unistr = unistr.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
            except:
                unistr = "UnableToDecodeString"
                print "Unicode encoding not in a recognized format..."
                break
    return unicodedata.normalize(format, unistr)
