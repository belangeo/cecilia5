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

import sys, os
from constants import *

CeciliaVar = dict()

CeciliaVar['DEBUG'] = True

# System variables
CeciliaVar['systemPlatform'] = sys.platform
CeciliaVar['numDisplays'] = 1
CeciliaVar['displaySize'] = []
CeciliaVar['displayOffset'] = []
CeciliaVar['mainFrame'] = None

# Path of the currently opened file
CeciliaVar['currentCeciliaFile'] = ''
CeciliaVar['builtinModule'] = False
CeciliaVar['currentModuleRef'] = None
CeciliaVar['currentModule'] = None

# Save path for the various dialogs that pops
CeciliaVar['openFilePath'] = os.path.expanduser('~')
CeciliaVar['saveFilePath'] = os.path.expanduser('~')
CeciliaVar['openAudioFilePath'] = os.path.expanduser('~')
CeciliaVar['saveAudioFilePath'] = os.path.expanduser('~')

# Boolean that says if file was modified since last save
CeciliaVar['isModified'] = False

# Audio / Midi
CeciliaVar['availableAudioOutputs'] = []
CeciliaVar['availableAudioInputs'] = []
CeciliaVar['availableMidiOutputs'] = []
CeciliaVar['availableMidiInputs'] = []

# Preferences variables
CeciliaVar['soundfilePlayer'] = ''
CeciliaVar['soundfileEditor'] = ''
CeciliaVar['prefferedPath'] = ''
CeciliaVar['rememberedSound'] = True

# Visual variables
CeciliaVar['useTooltips'] = 1
CeciliaVar['graphTexture'] = 1
CeciliaVar['moduleDescription'] = ''

# interface is a list of dictionaries.
# each entry is a dictionary defining a widget.
# the key is the name of the widget
# It is a list. not a dictionary.
# this way, we keep the user entries in order.
CeciliaVar['interfaceWidgets'] = []
CeciliaVar['interface'] = None
CeciliaVar['interfaceSize'] = (1000, 600)
CeciliaVar['interfacePosition'] = None
CeciliaVar['grapher'] = None
CeciliaVar['gainSlider'] = None
CeciliaVar['plugins'] = [None, None, None]
CeciliaVar['userSliders'] = []
CeciliaVar['userTogglePopups'] = []
CeciliaVar['userSamplers'] = []
CeciliaVar['userInputs'] = dict()
CeciliaVar['samplerSliders'] = []
CeciliaVar['samplerTogglePopup'] = []
CeciliaVar['presets'] = dict()
CeciliaVar['presetPanel'] = None

# Performance variables
CeciliaVar['outputFile'] = 'dac'
CeciliaVar['totalTime'] = 30.0
CeciliaVar['defaultTotalTime'] = 30.0
CeciliaVar['audioServer'] = None

# Csound Flags
CeciliaVar['sr'] = 44100
CeciliaVar['nchnls'] = 2
CeciliaVar['defaultNchnls'] = 2
CeciliaVar['sampSize'] = 0
CeciliaVar['audioFileType'] = 'aiff' # aiff, wav, 
CeciliaVar['bufferSize'] = 512
CeciliaVar['audioHostAPI'] = 'portaudio'
CeciliaVar['audioOutput'] = 0
CeciliaVar['audioInput'] = ''
CeciliaVar['enableAudioInput'] = 0
CeciliaVar['useMidi'] = 0
CeciliaVar['midiPort'] = 'portmidi'
CeciliaVar['midiDeviceIn'] = 0
CeciliaVar['jack'] = {'client':'pyo', 'inPortName':'system:capture_', 'outPortName':'system:playback_'}

def readCeciliaPrefsFromFile():
    if os.path.isfile(PREFERENCES_FILE):
        try:
            file = open(PREFERENCES_FILE, 'rt')
        except IOError:
            print('Unable to open the preferences file.')
            return
        
        print('Loading Cecilia Preferences...')
        
        #### Some special cases ####
        convertToInt = ['sr', 'kr', 'ksmps', 'defaultNchnls', 'audioOutput', 'audioInput', 'sampSize',
                        'midiDeviceIn', 'useTooltips', 'enableAudioInput', 'graphTexture']  
        convertToFloat = ['defaultTotalTime']                      
        convertToTuple = ['interfaceSize', 'interfacePosition']
        jackPrefs = ['client', 'inPortName', 'outPortName']
        
        # Go thru the text file to assign values to the variables
        for i, line in enumerate(file.readlines()):
            if i == 0:
                if not line.startswith("version"):
                    print('preferences file from an older version not used. New preferences will be created.')
                    return
                else:
                    if line.strip(' \n').split('=')[1] != APP_VERSION:
                        print('preferences file from an older version not used. New preferences will be created.')
                        return
                    else:
                        continue

            pref = line.strip(' \n').split('=')
            
            if pref[1]!='':
                if pref[0] in convertToInt:
                    CeciliaVar[pref[0]] = int(pref[1])
                elif pref[0] in convertToFloat:
                    CeciliaVar[pref[0]] = float(pref[1])
                elif pref[0] in convertToTuple:
                    CeciliaVar[pref[0]] = eval(pref[1])        
                elif pref[0] in jackPrefs:
                    CeciliaVar['jack'][pref[0]] = pref[1]
                else:
                    CeciliaVar[pref[0]] = pref[1]  
        file.close()
        CeciliaVar["nchnls"] = CeciliaVar["defaultNchnls"]
        
    else:
        print('Preferences file not found')

def writeCeciliaPrefsToFile():
    # Variables that need to be saved
    varsToSave = ['interfaceSize', 'interfacePosition', 'useTooltips', 'enableAudioInput',
                  'sr', 'kr', 'ksmps', 'defaultNchnls', 'sampSize', 'audioHostAPI',
                  'audioFileType', 'hardBuff', 'softBuff', 'audioOutput',
                  'audioInput', 'midiPort', 'midiDeviceIn',
                  'client', 'inPortName', 'graphTexture',
                  'outPortName', 'soundfilePlayer', 'soundfileEditor', 'prefferedPath',
                  'openFilePath', 'saveFilePath', 'saveAudioFilePath', 
                  'openAudioFilePath', 'defaultTotalTime']
    
    print('Writing Cecilia preferences...')
    
    #Open preferences file for writing
    try:
        file = open(PREFERENCES_FILE,'wt')
    except IOError:
        print('Unable to open the preferences file.')
        return
    
    # Write variables
    file.write("version=%s\n" % APP_VERSION)
    for key in CeciliaVar:
        if key in varsToSave:
            line = '%s=%s\n' % (key, CeciliaVar[key])
            file.write(line)
        elif key=='jack':
            line = '%s=%s\n' % ('client', CeciliaVar[key]['client'])
            line += '%s=%s\n' % ('inPortName', CeciliaVar[key]['inPortName'])
            line += '%s=%s\n' % ('outPortName', CeciliaVar[key]['outPortName'])
            file.write(line)
    
    file.close()

readCeciliaPrefsFromFile()
    
