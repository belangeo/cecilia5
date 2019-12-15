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

import sys, os, wx
import unicodedata
from .constants import *
from pyo import pa_get_default_devices_from_host

if sys.version_info[0] < 3:
    unicode_t = unicode
else:
    unicode_t = str

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
CeciliaVar['lastCeciliaFile'] = ''
CeciliaVar['builtinModule'] = False
CeciliaVar['currentModuleRef'] = None
CeciliaVar['currentModule'] = None
CeciliaVar['currentModuleName'] = None

# Save path for the various dialogs that pops
CeciliaVar['openFilePath'] = os.path.expanduser('~')
CeciliaVar['saveFilePath'] = os.path.expanduser('~')
CeciliaVar['openAudioFilePath'] = os.path.expanduser('~')
CeciliaVar['saveAudioFilePath'] = os.path.expanduser('~')
CeciliaVar['grapherLinePath'] = os.path.expanduser('~')

# Boolean that says if file was modified since last save
CeciliaVar['presetToLoad'] = None

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
CeciliaVar['interfacePosition'] = (0, 25)
CeciliaVar['grapher'] = None
CeciliaVar['gainSlider'] = None
CeciliaVar['plugins'] = [None] * NUM_OF_PLUGINS
CeciliaVar['userSliders'] = []
CeciliaVar['userTogglePopups'] = []
CeciliaVar['userSamplers'] = []
CeciliaVar['userInputs'] = dict()
CeciliaVar['samplerSliders'] = []
CeciliaVar['samplerTogglePopup'] = []
CeciliaVar['initPreset'] = None
CeciliaVar['presetPanel'] = None

CeciliaVar['tooltips'] = []

# Performance variables
CeciliaVar['toDac'] = True
CeciliaVar['outputFile'] = ''
CeciliaVar['totalTime'] = 30.0
CeciliaVar['defaultTotalTime'] = 30.0
CeciliaVar['startOffset'] = 0.0
CeciliaVar['globalFade'] = 0.005
CeciliaVar['audioServer'] = None
CeciliaVar['automaticMidiBinding'] = 0
CeciliaVar['showSpectrum'] = 0
CeciliaVar['spectrumFrame'] = None

if sys.platform.startswith("win"):
    def_in, def_out = pa_get_default_devices_from_host("directsound")
elif sys.platform.startswith("darwin"):
    def_in, def_out = pa_get_default_devices_from_host("core")
else:
    def_in, def_out = pa_get_default_devices_from_host("alsa")
if def_in < 0:
    def_in = 0
if def_out < 0:
    def_out = 0

# Server Flags
CeciliaVar['sr'] = 44100
CeciliaVar['nchnls'] = 2
CeciliaVar['defaultNchnls'] = 2
CeciliaVar['sampSize'] = 0
CeciliaVar['audioFileType'] = 'aif' # aif, wav, flac, ogg, sd2, au, caf
CeciliaVar['samplePrecision'] = '32 bit' # '32 bit', '64 bit'
CeciliaVar['bufferSize'] = '512'
CeciliaVar['audioHostAPI'] = 'portaudio'
CeciliaVar['audioOutput'] = def_out
CeciliaVar['audioInput'] = def_in
CeciliaVar['enableAudioInput'] = 0
CeciliaVar['useMidi'] = 0
CeciliaVar['useSoundDur'] = 0
CeciliaVar['midiPort'] = 'portmidi'
CeciliaVar['midiDeviceIn'] = 0
CeciliaVar['defaultFirstInput'] = 0
CeciliaVar['defaultFirstOutput'] = 0
CeciliaVar['jack'] = {'client': 'cecilia5'}

CeciliaVar['lastAudioFiles'] = ""

def loadBitmaps():
    CeciliaVar['ICON_VUMETER'] = ICON_VUMETER.GetBitmap()
    CeciliaVar['ICON_VUMETER_DARK'] = ICON_VUMETER_DARK.GetBitmap()
    CeciliaVar['ICON_PLUGINS_KNOB'] = ICON_PLUGINS_KNOB.GetBitmap()
    CeciliaVar['ICON_PLUGINS_KNOB_DISABLE'] = ICON_PLUGINS_KNOB_DISABLE.GetBitmap()
    CeciliaVar['ICON_PLUGINS_ARROW_UP'] = ICON_PLUGINS_ARROW_UP.GetBitmap()
    CeciliaVar['ICON_PLUGINS_ARROW_UP_HOVER'] = ICON_PLUGINS_ARROW_UP_HOVER.GetBitmap()
    CeciliaVar['ICON_PLUGINS_ARROW_DOWN'] = ICON_PLUGINS_ARROW_DOWN.GetBitmap()
    CeciliaVar['ICON_PLUGINS_ARROW_DOWN_HOVER'] = ICON_PLUGINS_ARROW_DOWN_HOVER.GetBitmap()
    CeciliaVar['ICON_TB_LOAD'] = ICON_TB_LOAD.GetBitmap()
    CeciliaVar['ICON_TB_LOAD_OVER'] = ICON_TB_LOAD_OVER.GetBitmap()
    CeciliaVar['ICON_TB_SAVE'] = ICON_TB_SAVE.GetBitmap()
    CeciliaVar['ICON_TB_SAVE_OVER'] = ICON_TB_SAVE_OVER.GetBitmap()
    CeciliaVar['ICON_TB_RESET'] = ICON_TB_RESET.GetBitmap()
    CeciliaVar['ICON_TB_RESET_OVER'] = ICON_TB_RESET_OVER.GetBitmap()
    CeciliaVar['ICON_TB_SHOW'] = ICON_TB_SHOW.GetBitmap()
    CeciliaVar['ICON_TB_SHOW_OVER'] = ICON_TB_SHOW_OVER.GetBitmap()
    CeciliaVar['ICON_TB_HIDE'] = ICON_TB_HIDE.GetBitmap()
    CeciliaVar['ICON_TB_HIDE_OVER'] = ICON_TB_HIDE_OVER.GetBitmap()
    CeciliaVar['ICON_TB_RECYCLE'] = ICON_TB_RECYCLE.GetBitmap()
    CeciliaVar['ICON_TB_RECYCLE_OVER'] = ICON_TB_RECYCLE_OVER.GetBitmap()
    CeciliaVar['ICON_TB_PLAY'] = ICON_TB_PLAY.GetBitmap()
    CeciliaVar['ICON_TB_PLAY_OVER'] = ICON_TB_PLAY_OVER.GetBitmap()
    CeciliaVar['ICON_TB_EDIT'] = ICON_TB_EDIT.GetBitmap()
    CeciliaVar['ICON_TB_EDIT_OVER'] = ICON_TB_EDIT_OVER.GetBitmap()
    CeciliaVar['ICON_TB_OPEN'] = ICON_TB_OPEN.GetBitmap()
    CeciliaVar['ICON_TB_OPEN_OVER'] = ICON_TB_OPEN_OVER.GetBitmap()
    CeciliaVar['ICON_TB_CLOSE'] = ICON_TB_CLOSE.GetBitmap()
    CeciliaVar['ICON_TB_CLOSE_OVER'] = ICON_TB_CLOSE_OVER.GetBitmap()
    CeciliaVar['ICON_TB_TIME'] = ICON_TB_TIME.GetBitmap()
    CeciliaVar['ICON_TB_TIME_OVER'] = ICON_TB_TIME_OVER.GetBitmap()
    CeciliaVar['ICON_TB_DELETE'] = ICON_TB_DELETE.GetBitmap()
    CeciliaVar['ICON_TB_DELETE_OVER'] = ICON_TB_DELETE_OVER.GetBitmap()
    CeciliaVar['ICON_RTB_POINTER'] = ICON_RTB_POINTER.GetBitmap()
    CeciliaVar['ICON_RTB_POINTER_OVER'] = ICON_RTB_POINTER_OVER.GetBitmap()
    CeciliaVar['ICON_RTB_POINTER_CLICK'] = ICON_RTB_POINTER_CLICK.GetBitmap()
    CeciliaVar['ICON_RTB_PENCIL'] = ICON_RTB_PENCIL.GetBitmap()
    CeciliaVar['ICON_RTB_PENCIL_OVER'] = ICON_RTB_PENCIL_OVER.GetBitmap()
    CeciliaVar['ICON_RTB_PENCIL_CLICK'] = ICON_RTB_PENCIL_CLICK.GetBitmap()
    CeciliaVar['ICON_RTB_ZOOM'] = ICON_RTB_ZOOM.GetBitmap()
    CeciliaVar['ICON_RTB_ZOOM_OVER'] = ICON_RTB_ZOOM_OVER.GetBitmap()
    CeciliaVar['ICON_RTB_ZOOM_CLICK'] = ICON_RTB_ZOOM_CLICK.GetBitmap()
    CeciliaVar['ICON_RTB_HAND'] = ICON_RTB_HAND.GetBitmap()
    CeciliaVar['ICON_RTB_HAND_OVER'] = ICON_RTB_HAND_OVER.GetBitmap()
    CeciliaVar['ICON_RTB_HAND_CLICK'] = ICON_RTB_HAND_CLICK.GetBitmap()
    CeciliaVar['ICON_PREF_AUDIO'] = ICON_PREF_AUDIO.GetBitmap()
    CeciliaVar['ICON_PREF_AUDIO_OVER'] = ICON_PREF_AUDIO_OVER.GetBitmap()
    CeciliaVar['ICON_PREF_AUDIO_CLICK'] = ICON_PREF_AUDIO_CLICK.GetBitmap()
    CeciliaVar['ICON_PREF_CECILIA'] = ICON_PREF_CECILIA.GetBitmap()
    CeciliaVar['ICON_PREF_CECILIA_OVER'] = ICON_PREF_CECILIA_OVER.GetBitmap()
    CeciliaVar['ICON_PREF_CECILIA_CLICK'] = ICON_PREF_CECILIA_CLICK.GetBitmap()
    CeciliaVar['ICON_PREF_FILER'] = ICON_PREF_FILER.GetBitmap()
    CeciliaVar['ICON_PREF_FILER_OVER'] = ICON_PREF_FILER_OVER.GetBitmap()
    CeciliaVar['ICON_PREF_FILER_CLICK'] = ICON_PREF_FILER_CLICK.GetBitmap()
    CeciliaVar['ICON_PREF_PATH'] = ICON_PREF_PATH.GetBitmap()
    CeciliaVar['ICON_PREF_PATH_OVER'] = ICON_PREF_PATH_OVER.GetBitmap()
    CeciliaVar['ICON_PREF_PATH_CLICK'] = ICON_PREF_PATH_CLICK.GetBitmap()
    CeciliaVar['ICON_PREF_MIDI'] = ICON_PREF_MIDI.GetBitmap()
    CeciliaVar['ICON_PREF_MIDI_OVER'] = ICON_PREF_MIDI_OVER.GetBitmap()
    CeciliaVar['ICON_PREF_MIDI_CLICK'] = ICON_PREF_MIDI_CLICK.GetBitmap()
    CeciliaVar['ICON_PTB_PROCESS'] = ICON_PTB_PROCESS.GetBitmap()
    CeciliaVar['ICON_PTB_PROCESS_OVER'] = ICON_PTB_PROCESS_OVER.GetBitmap()
    CeciliaVar['ICON_PTB_RANDOM'] = ICON_PTB_RANDOM.GetBitmap()
    CeciliaVar['ICON_PTB_RANDOM_OVER'] = ICON_PTB_RANDOM_OVER.GetBitmap()
    CeciliaVar['ICON_PTB_WAVES'] = ICON_PTB_WAVES.GetBitmap()
    CeciliaVar['ICON_PTB_WAVES_OVER'] = ICON_PTB_WAVES_OVER.GetBitmap()
    CeciliaVar['ICON_INPUT_1_FILE'] = ICON_INPUT_1_FILE.GetBitmap()
    CeciliaVar['ICON_INPUT_2_LIVE'] = ICON_INPUT_2_LIVE.GetBitmap()
    CeciliaVar['ICON_INPUT_3_MIC'] = ICON_INPUT_3_MIC.GetBitmap()
    CeciliaVar['ICON_INPUT_4_MIC_RECIRC'] = ICON_INPUT_4_MIC_RECIRC.GetBitmap()
    CeciliaVar['ICON_XFADE_LINEAR'] = ICON_XFADE_LINEAR.GetBitmap()
    CeciliaVar['ICON_XFADE_POWER'] = ICON_XFADE_POWER.GetBitmap()
    CeciliaVar['ICON_XFADE_SIGMOID'] = ICON_XFADE_SIGMOID.GetBitmap()
    CeciliaVar['ICON_MARIO1'] = ICON_MARIO1.GetBitmap()
    CeciliaVar['ICON_MARIO2'] = ICON_MARIO2.GetBitmap()
    CeciliaVar['ICON_MARIO3'] = ICON_MARIO3.GetBitmap()
    CeciliaVar['ICON_MARIO4'] = ICON_MARIO4.GetBitmap()
    CeciliaVar['ICON_MARIO5'] = ICON_MARIO5.GetBitmap()
    CeciliaVar['ICON_MARIO6'] = ICON_MARIO6.GetBitmap()
    CeciliaVar['ICON_GRAPHER_BACKGROUND'] = ICON_GRAPHER_BACKGROUND.GetBitmap()
    CeciliaVar['ICON_CECILIA_ABOUT_SMALL'] = ICON_CECILIA_ABOUT_SMALL.GetBitmap()
    CeciliaVar['ICON_DOC_PREVIOUS'] = ICON_DOC_PREVIOUS.GetBitmap()
    CeciliaVar['ICON_DOC_NEXT'] = ICON_DOC_NEXT.GetBitmap()
    CeciliaVar['ICON_DOC_UP'] = ICON_DOC_UP.GetBitmap()

def ensureNFD(unistr):
    if sys.platform.startswith('linux') or sys.platform == 'win32':
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

# Reading and writing of preferences should be moved to CeciliaLib.
def readCeciliaPrefsFromFile():
    if os.path.isfile(PREFERENCES_FILE):
        try:
            file = open(PREFERENCES_FILE, 'rt', encoding=FILE_ENCODING)
        except:
            print('Unable to open the preferences file.\n')
            print('Cecilia will use the default preferences.\n')
            return

        print('Loading Cecilia Preferences...')

        #### Some special cases ####
        convertToInt = ['sr', 'defaultNchnls', 'audioOutput', 'audioInput', 'sampSize', 'automaticMidiBinding',
                        'midiDeviceIn', 'useTooltips', 'enableAudioInput', 'graphTexture', 'showSpectrum', 'useSoundDur',
                        'defaultFirstInput', 'defaultFirstOutput']
        convertToFloat = ['defaultTotalTime', 'globalFade', 'DEBUG']
        convertToTuple = ['interfaceSize', 'interfacePosition']
        jackPrefs = ['client']

        text = ensureNFD(file.read())

        # Go through the text file to assign values to the variables
        try:
            for i, line in enumerate(text.splitlines()):
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

                if pref[1] != '':
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
        except:
            print("something wrong happened when reading preferences "
                   "(probably character encoding/decoding problem), "
                   "some preferences may be lost.")

        file.close()
        CeciliaVar["nchnls"] = CeciliaVar["defaultNchnls"]

    else:
        print('Preferences file not found. Using defaults...\n')

def writeCeciliaPrefsToFile():
    varsToSave = ['interfaceSize', 'interfacePosition', 'useTooltips', 'enableAudioInput', 'textEditor',
                  'sr', 'defaultNchnls', 'sampSize', 'audioHostAPI', 'audioFileType', 'audioOutput',
                  'audioInput', 'midiPort', 'midiDeviceIn', 'samplePrecision', 'client', 'graphTexture',
                  'globalFade', 'bufferSize', 'soundfilePlayer', 'soundfileEditor', 'prefferedPath', 'DEBUG',
                  'openFilePath', 'saveFilePath', 'saveAudioFilePath', 'openAudioFilePath', 'grapherLinePath',
                  'defaultTotalTime', 'lastAudioFiles', 'automaticMidiBinding', 'showSpectrum', 'useSoundDur',
                  'defaultFirstInput', 'defaultFirstOutput', 'lastCeciliaFile']

    print('Writing Cecilia preferences...')

    try:
        file = open(PREFERENCES_FILE, 'wt')
    except IOError:
        print('Unable to open the preferences file.\n')
        return

    file.write("version=%s\n" % APP_VERSION)
    for key in CeciliaVar:
        if key in varsToSave:
            line = '%s=%s\n' % (key, CeciliaVar[key])
            file.write(line)
        elif key == 'jack':
            line = '%s=%s\n' % ('client', CeciliaVar[key]['client'])
            file.write(line)

    file.close()

readCeciliaPrefsFromFile()
