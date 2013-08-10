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

import sys, os
from constants import *

CeciliaVar = dict()

CeciliaVar['DEBUG'] = 0

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
CeciliaVar['grapherLinePath'] = os.path.expanduser('~')

# Boolean that says if file was modified since last save
CeciliaVar['isModified'] = False

# Audio / Midi
CeciliaVar['availableAudioOutputs'] = []
CeciliaVar['availableAudioOutputIndexes'] = []
CeciliaVar['availableAudioInputs'] = []
CeciliaVar['availableAudioInputIndexes'] = []
CeciliaVar['availableMidiOutputs'] = []
CeciliaVar['availableMidiOutputIndexes'] = []
CeciliaVar['availableMidiInputs'] = []
CeciliaVar['availableMidiInputIndexes'] = []

# Preferences variables
CeciliaVar['soundfilePlayer'] = ''
CeciliaVar['soundfileEditor'] = ''
CeciliaVar['textEditor'] = ''
CeciliaVar['prefferedPath'] = ''
CeciliaVar['rememberedSound'] = True

# Visual variables
CeciliaVar['useTooltips'] = 1
CeciliaVar['graphTexture'] = 1
CeciliaVar['moduleDescription'] = ''

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
CeciliaVar['initPreset'] = None
CeciliaVar['presetPanel'] = None

# Performance variables
CeciliaVar['toDac'] = True
CeciliaVar['outputFile'] = ''
CeciliaVar['totalTime'] = 30.0
CeciliaVar['defaultTotalTime'] = 30.0
CeciliaVar['startOffset'] = 0.0
CeciliaVar['globalFade'] = 0.005
CeciliaVar['audioServer'] = None
CeciliaVar['automaticMidiBinding'] = 0
#CeciliaVar['InputLive'] = True

# Server Flags
CeciliaVar['sr'] = 44100
CeciliaVar['nchnls'] = 2
CeciliaVar['defaultNchnls'] = 2
CeciliaVar['sampSize'] = 0
CeciliaVar['audioFileType'] = 'aif' # aif, wav, 
CeciliaVar['samplePrecision'] = '32 bit' # '32 bit', '64 bit'
CeciliaVar['bufferSize'] = '512'
CeciliaVar['audioHostAPI'] = 'portaudio'
CeciliaVar['audioOutput'] = 0
CeciliaVar['audioInput'] = 0
CeciliaVar['enableAudioInput'] = 0
CeciliaVar['useMidi'] = 0
CeciliaVar['midiPort'] = 'portmidi'
CeciliaVar['midiDeviceIn'] = 0
CeciliaVar['jack'] = {'client':'pyo'}

CeciliaVar['lastAudioFiles'] = ""

def readCeciliaPrefsFromFile():
    if os.path.isfile(PREFERENCES_FILE):
        try:
            file = open(PREFERENCES_FILE, 'rt')
        except IOError:
            print('Unable to open the preferences file.\n')
            return
        
        print('Loading Cecilia Preferences...')
        
        #### Some special cases ####
        convertToInt = ['sr', 'defaultNchnls', 'audioOutput', 'audioInput', 'sampSize', 'automaticMidiBinding',
                        'midiDeviceIn', 'useTooltips', 'enableAudioInput', 'graphTexture']  
        convertToFloat = ['defaultTotalTime', 'globalFade', 'DEBUG']                      
        convertToTuple = ['interfaceSize', 'interfacePosition']
        jackPrefs = ['client']
        
        # Go thru the text file to assign values to the variables
        for i, line in enumerate(file.readlines()):
            if i == 0:
                if not line.startswith("version"):
                    print('preferences file from an older version not used. New preferences will be created.\n')
                    return
                else:
                    if line.strip(' \n').split('=')[1] != APP_VERSION:
                        print('preferences file from an older version not used. New preferences will be created.\n')
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
                    if pref[0] == 'audioHostAPI' and pref[1] not in AUDIO_DRIVERS:
                        CeciliaVar[pref[0]] = 'portaudio'
                    else:
                        CeciliaVar[pref[0]] = pref[1]
        file.close()
        CeciliaVar["nchnls"] = CeciliaVar["defaultNchnls"]
        
    else:
        print('Preferences file not found.\n')

def writeCeciliaPrefsToFile():
    # Variables that need to be saved
    varsToSave = ['interfaceSize', 'interfacePosition', 'useTooltips', 'enableAudioInput', 'textEditor',
                  'sr', 'defaultNchnls', 'sampSize', 'audioHostAPI', 'audioFileType', 'audioOutput',
                  'audioInput', 'midiPort', 'midiDeviceIn', 'samplePrecision', 'client', 'graphTexture', 
                  'globalFade', 'bufferSize', 'soundfilePlayer', 'soundfileEditor', 'prefferedPath', 'DEBUG',
                  'openFilePath', 'saveFilePath', 'saveAudioFilePath', 'openAudioFilePath', 'grapherLinePath',
                  'defaultTotalTime', 'lastAudioFiles', 'automaticMidiBinding']
    
    print('Writing Cecilia preferences...')
    
    #Open preferences file for writing
    try:
        file = open(PREFERENCES_FILE,'wt')
    except IOError:
        print('Unable to open the preferences file.\n')
        return
    
    # Write variables
    file.write("version=%s\n" % APP_VERSION)
    for key in CeciliaVar:
        if key in varsToSave:
            line = '%s=%s\n' % (key, CeciliaVar[key])
            file.write(line)
        elif key=='jack':
            line = '%s=%s\n' % ('client', CeciliaVar[key]['client'])
            file.write(line)
    
    file.close()

readCeciliaPrefsFromFile()
    
