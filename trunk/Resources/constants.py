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

import os, sys
from images import *

reload(sys)
sys.setdefaultencoding("utf-8")

APP_NAME = 'Cecilia5'
APP_VERSION = '5.0.6 beta'
APP_COPYRIGHT = 'iACT,  2012'
FILE_EXTENSION = "c5"
PRESETS_DELIMITER = "####################################\n" \
                    "##### Cecilia reserved section #####\n" \
                    "#### Presets saved from the app ####\n" \
                    "####################################\n"

DEFAULT_ENCODING = sys.getdefaultencoding()
ENCODING = sys.getfilesystemencoding()

if '/%s.app' % APP_NAME in os.getcwd():
    RESOURCES_PATH = os.getcwd()
else:
    RESOURCES_PATH = os.path.join(os.getcwd(), 'Resources')

if not os.path.isdir(RESOURCES_PATH) and sys.platform == "win32":
    RESOURCES_PATH = os.path.join(os.getenv("ProgramFiles"), "Cecilia5", "Resources")

TMP_PATH = os.path.join(os.path.expanduser('~'), '.cecilia5')
PREFERENCES_FILE = os.path.join(TMP_PATH, 'ceciliaPrefs.txt')
MODULES_PATH = os.path.join(RESOURCES_PATH, 'modules')
# Folder to save automations
AUTOMATION_SAVE_PATH = os.path.join(TMP_PATH, 'automation_save')

# Meter icons
ICON_VUMETER = catalog['vu-metre2.png']
ICON_VUMETER_DARK = catalog['vu-metre-dark2.png']
# Plugin icons
ICON_PLUGINS_KNOB = catalog['knob-trans-sm.png']
ICON_PLUGINS_KNOB_DISABLE = catalog['knob-disab-sm.png']
# Toolbox icons
ICON_TB_LOAD = catalog['load-normal-trans.png']
ICON_TB_LOAD_OVER = catalog['load-hover-trans.png']
ICON_TB_SAVE = catalog['save-normal-trans.png']
ICON_TB_SAVE_OVER = catalog['save-hover-trans.png']
ICON_TB_RESET = catalog['reset-normal-trans.png']
ICON_TB_RESET_OVER = catalog['reset-hover-trans.png']
ICON_TB_SHOW = catalog['show-normal-trans.png']
ICON_TB_SHOW_OVER = catalog['show-hover-trans.png']
ICON_TB_HIDE = catalog['hide-normal-trans.png']
ICON_TB_HIDE_OVER = catalog['hide-hover-trans.png']
ICON_TB_RECYCLE = catalog['recycle-normal-trans.png']
ICON_TB_RECYCLE_OVER = catalog['recycle-hover-trans.png']
ICON_TB_PLAY = catalog['play-normal-trans.png']
ICON_TB_PLAY_OVER = catalog['play-hover-trans.png']
ICON_TB_EDIT = catalog['edit-normal-trans.png']
ICON_TB_EDIT_OVER = catalog['edit-hover-trans.png']
ICON_TB_OPEN = catalog['open-normal-trans.png']
ICON_TB_OPEN_OVER = catalog['open-hover-trans.png']
ICON_TB_CLOSE = catalog['close-normal-trans.png']
ICON_TB_CLOSE_OVER = catalog['close-hover-trans.png']
ICON_TB_TIME = catalog['time-normal-trans.png']
ICON_TB_TIME_OVER = catalog['time-hover-trans.png']
ICON_TB_DELETE = catalog['delete-normal-trans.png']
ICON_TB_DELETE_OVER = catalog['delete-hover-trans.png']
# RadioToolbox icons
ICON_RTB_POINTER = catalog['pointer-normal-trans.png']
ICON_RTB_POINTER_OVER = catalog['pointer-hover-trans.png']
ICON_RTB_POINTER_CLICK = catalog['pointer-click-trans.png']
ICON_RTB_PENCIL = catalog['pencil-normal-trans.png']
ICON_RTB_PENCIL_OVER = catalog['pencil-hover-trans.png']
ICON_RTB_PENCIL_CLICK = catalog['pencil-click-trans.png']
ICON_RTB_ZOOM = catalog['zoom-normal-trans.png']
ICON_RTB_ZOOM_OVER = catalog['zoom-hover-trans.png']
ICON_RTB_ZOOM_CLICK = catalog['zoom-click-trans.png']
ICON_RTB_HAND = catalog['hand-normal-trans.png']
ICON_RTB_HAND_OVER = catalog['hand-hover-trans.png']
ICON_RTB_HAND_CLICK = catalog['hand-click-trans.png']
# PrefRadioToolbox icons
ICON_PREF_AUDIO = catalog['audio-normal-trans.png']
ICON_PREF_AUDIO_OVER = catalog['audio-hover-trans.png']
ICON_PREF_AUDIO_CLICK = catalog['audio-click-trans.png']
ICON_PREF_CECILIA = catalog['cecilia-normal-trans.png']
ICON_PREF_CECILIA_OVER = catalog['cecilia-hover-trans.png']
ICON_PREF_CECILIA_CLICK = catalog['cecilia-click-trans.png']
ICON_PREF_CSOUND = catalog['csound-normal-trans.png']
ICON_PREF_CSOUND_OVER = catalog['csound-hover-trans.png']
ICON_PREF_CSOUND_CLICK = catalog['csound-click-trans.png']
ICON_PREF_FILER = catalog['filer-normal-trans.png']
ICON_PREF_FILER_OVER = catalog['filer-hover-trans.png']
ICON_PREF_FILER_CLICK = catalog['filer-click-trans.png']
ICON_PREF_PATH = catalog['path-normal-trans.png']
ICON_PREF_PATH_OVER = catalog['path-hover-trans.png']
ICON_PREF_PATH_CLICK = catalog['path-click-trans.png']
ICON_PREF_MIDI = catalog['midi-normal-trans.png']
ICON_PREF_MIDI_OVER = catalog['midi-hover-trans.png']
ICON_PREF_MIDI_CLICK = catalog['midi-click-trans.png']
# PaletteToolBox icons
ICON_PTB_PROCESS = catalog['process-normal-trans.png']
ICON_PTB_PROCESS_OVER = catalog['process-hover-trans.png']
ICON_PTB_RANDOM = catalog['random-normal-trans.png']
ICON_PTB_RANDOM_OVER = catalog['random-hover-trans.png']
ICON_PTB_WAVES = catalog['waves-normal-trans.png']
ICON_PTB_WAVES_OVER = catalog['waves-hover-trans.png']
# Crossfade icons
ICON_XFADE_LINEAR = catalog['xfade-linear.png']
ICON_XFADE_POWER = catalog['xfade-power.png']
ICON_XFADE_SIGMOID = catalog['xfade-sigmoid.png']
# Mario bros
ICON_MARIO1 = catalog['Mario1.png']
ICON_MARIO2 = catalog['Mario2.png']
ICON_MARIO3 = catalog['Mario3.png']
ICON_MARIO4 = catalog['Mario4.png']
ICON_MARIO5 = catalog['Mario5.png']
ICON_MARIO6 = catalog['Mario6.png']
# Grapher background
ICON_GRAPHER_BACKGROUND = catalog['Grapher_background.png']
# About icon
ICON_CECILIA_ABOUT_SMALL = catalog['Cecilia_about_small.png']

# Audio drivers
if sys.platform == 'darwin' and '/%s.app' % APP_NAME in os.getcwd():
    AUDIO_DRIVERS = ['portaudio']
elif sys.platform == 'darwin':
    AUDIO_DRIVERS = ['coreaudio', 'portaudio', 'jack']
elif sys.platform == 'win32':
    AUDIO_DRIVERS = ['portaudio']
else:
    AUDIO_DRIVERS = ['portaudio', 'jack']

# MIDI drivers
MIDI_DRIVERS = ['portmidi']

# plugin types
PLUGINS_CHOICE = ['None', 'Reverb', 'Filter', 'Chorus', 'Para EQ', '3 Bands EQ', 'Compress', 'Gate', 
                  'Disto', 'AmpMod', 'Phaser', 'Delay', 'Flange', 'Harmonizer', 'Resonators', 'DeadReson']

# Audio settings
AUDIO_FILE_FORMATS = ['aiff', 'wav']
SAMPLE_RATES = ['22050','44100','48000', '88200', '96000']
BIT_DEPTHS= {'16 bits int': 0, '24 bits int': 1, '32 bits int': 2, '32 bits float': 3}
BUFFER_SIZES = ['64','128','256','512','1024','2048','4096','8192','16384']

# Menu Ids
ID_OPEN = 1002
ID_SAVE = 1004
ID_SAVEAS = 1005
ID_UNDO = 1013
ID_REDO = 1014
ID_COPY = 1016
ID_PASTE = 1017
ID_REMEMBER = 1019
ID_PLAY_STOP = 1034
ID_USE_MIDI = 2052
ID_OPEN_RECENT = 4000
ID_OPEN_BUILTIN = 4100
ID_UPDATE_INTERFACE = 5000
ID_MODULE_INFO = 5100

# Fonts
FONT_FACE = 'Trebuchet MS'
if sys.platform in ['linux2', 'win32']:
    CONTROLSLIDER_FONT = 7
    LABEL_FONT = 7
    MENU_FONT = 8
    CLOCKER_FONT = 10
    ENTRYUNIT_FONT = 7
    GRAPHER_AXIS_FONT = 8
    GRAPHER_LEGEND_FONT = 8
    TEXT_LABELFORWIDGET_FONT = 7
    SECTION_TITLE_FONT = 10
    TEXT_CHANNELNUM_FONT = 7
    SPLITTER_FONT = 7
    LIST_ENTRY_FONT = 9
else:
    CONTROLSLIDER_FONT = 10
    LABEL_FONT = 10
    MENU_FONT = 11
    CLOCKER_FONT = 14
    ENTRYUNIT_FONT = 10
    GRAPHER_AXIS_FONT = 10
    GRAPHER_LEGEND_FONT = 10
    TEXT_LABELFORWIDGET_FONT = 10
    SECTION_TITLE_FONT = 14
    TEXT_CHANNELNUM_FONT = 9
    SPLITTER_FONT = 9
    LIST_ENTRY_FONT = 12

# Colours
BACKGROUND_COLOUR = "#666666"
GRAPHER_BACK_COLOUR = "#D1D1D1"
TITLE_BACK_COLOUR = "#333333"
SECTION_TITLE_COLOUR = "#CCCCCC"
WHITE_COLOUR = "#FFFFFF"
GREY_COLOUR = "#666666"
BLACK_COLOUR = "#000000"
BORDER_COLOUR = "#444444"
CLOSEBOX_INSIDE_COLOUR = "#8896BB"
TEXT_LABELFORWIDGET_COLOUR = "#FFFFFF"
GRADIENT_DARK_COLOUR = "#313740"
WIDGET_BORDER_COLOUR = "#BBBBBB"
KNOB_BORDER_COLOUR = "#929292"
POPUP_BACK_COLOUR = "#80A0B0"
POPUP_BORDER_COLOUR = "#222222"
POPUP_LABEL_COLOUR = "#FFFFFF"
POPUP_HIGHLIGHT_COLOR = "#DDDDDD"
POPUP_TEXT_COLOUR = "#806666"
POPUP_PAGETEXT_COLOR = "#FFFFFF"
POPUP_PAGEARROW_COLOR = "#FFFFFF"
POPUP_PAGEARROW_COLOR_OVER = "#0088CC"
POPUP_DISABLE_LABEL_COLOUR = "#333333"
LABEL_LABEL_COLOUR = "#FFFFFF"
LABEL_BACK_COLOUR = "#666666"
CPOLY_COLOUR = "#555555"
TOGGLE_BACK_COLOUR = "#414753"
TOGGLE_LABEL_COLOUR = "#FFFFFF"
TOOL_BACK_COLOUR = '#D0D56D'
TOOL_BORDER_COLOUR = "#797979"
ENTRYUNIT_HIGHLIGHT_COLOUR = "#222222"
ENTRYUNIT_BACK_COLOUR = "#666666"
SLIDER_BACK_COLOUR = "#666666"
SLIDER_KNOB_COLOUR = "#444444"
SLIDER_PLAY_COLOUR_HOT = "#004400"
SLIDER_PLAY_COLOUR_PRESSED = "#00FF00"
SLIDER_PLAY_COLOUR_OVER = "#FFFFFF"
SLIDER_PLAY_COLOUR_NO_BIND = "#FFFF00"
SLIDER_REC_COLOUR_HOT = "#440000"
SLIDER_REC_COLOUR_PRESSED = "#FF0000"
SLIDER_REC_COLOUR_OVER = "#FFFFFF"
CONTROLSLIDER_DISABLE_COLOUR = '#DDDDDD'
CONTROLSLIDER_BACK_COLOUR = '#99A7CC'
CONTROLSLIDER_KNOB_COLOUR = '#ABABAB'
CONTROLSLIDER_SELECTED_COLOUR = '#333333'
CONTROLSLIDER_TEXT_COLOUR = '#FFFFFF'
CONTROLLABEL_BACK_COLOUR = "#6F7F97"
TR_BACK_COLOUR = "#6F7F97"
TR_BORDER_COLOUR = '#BBBBBB'
TR_PLAY_NORMAL_COLOUR = '#009911'
TR_PLAY_CLICK_COLOUR = '#007A29'
TR_RECORD_OFF_COLOUR = '#6E3131'
TR_RECORD_ON_COLOUR = '#FF0000'

COLOUR_CLASSES = {'green': [100., 0.30, .75], 
        'forestgreen': [83., 0.35, .62], 
        'olivegreen': [75., 0.48, .5],
        'lightgreen': [90., 0.59, .33],
        'red': [0., .4, .5],        
        'orange': [20., 0.5, .46], 
        'khaki': [40., 0.55, .4], 
        'tan': [50., 0.65, .35], 
        'blue': [230., 0.55, .5], 
        'marineblue': [225., 0.45, .45], 
        'royalblue': [203., 0.5, .33], 
        'lightblue': [196., 0.65, .25],
        'brightred': [0., 0.55, .9], 
        'brightblue': [200., 0.55, .9], 
        'brightgreen': [90., 0.55, .9], 
        'chorusyellow': [42., 0.4, .65], 
        'filterred': [342., 0.44, .47], 
        'compblue': [240., 0.44, .22], 
        'grey': [0., 0.34, 0.]
}

# ToolTips
TT_PLAY = "Triangle: Launch playback. Click again to stop."
TT_RECORD = "Circle: Record Output to a file. No sound is heard."
TT_CLOCK = "Current time of playback."

TT_SEL_SOUND = "Select source sound. If none, open standard dialog. Source folder is read."

TT_PLAY_SOUND = "Speaker: Play sound in Player app."
TT_EDIT_SOUND = "Scissors: Edit sound in Editor app."
TT_LOAD_SOUND = "Folder: Change folder for input sound. Source folder is read."
TT_OPEN_SAMPLER = "Triangle: Toggle for source sound controls."
TT_SET_OUTPUT = "Folder: Change destination and name for output sound."
TT_USE_OUTPUT = "Arrows: Use output sound as source sound."
TT_SAVE_GRAPH = "Floppy: Save graph to the disk."
TT_LOAD_GRAPH = "Folder: Load graph from disk."
TT_REINIT_GRAPH = "Arrow: Reinitialize graph."
TT_SHOW_GRAPH = "Eye: Show/Hide graph."
TT_PRESET_SAVE = "Floppy: Save a preset."
TT_PRESET_DELETE =  "X: Delete a preset."
TT_SET_DUR = "Clock: Set duration of output to source sound duration."

TT_OUTPUT = "Name of output file."
TT_DUR_SLIDER = "Set duration of output. Shift click in slider knob to set value from keyboard."
TT_GAIN_SLIDER = "Adjust gain of output. Shift click in slider knob to set value from keyboard."
TT_CHANNELS = "Select # of channels for output."
TT_PEAK = "Displays peak amplitude of output. Double-click to reset."
TT_GRAPH_POPUP = "Select graph for editing."
TT_RES_SLIDER = "Adjust resolution of recorded graph."
TT_POINTER = "Arrow: Use pointer tool - v."
TT_ZOOM = "Magnifying glass: Use zoom - z."
TT_HAND = "Hand: Use hand tool - h."
TT_PENCIL = "Pencil: Use pencil tool - p."
TT_STOCHASTIC = "Rand line: Use stochastic function generator."
TT_WAVEFORM = "Sine wave: Use waveform function generator."
TT_PROCESSOR = "Gears: Use function processor."

TT_PRESET = "Choose a preset for this module."

TT_SLIDER_LABEL = "Parameter name for slider. Click to select in grapher. Shift-click to solo in grapher. Right-click starts midi learn. Shift-Right-click removed midi binding."
TT_SLIDER_PLAY = "Triangle: Playback controls.\nDark green = Off\nLight green = play with visual update\nYellow = play without visual update."
TT_SLIDER_RECORD = "Circle: Record movements of this slider."
TT_SLIDER_DISPLAY = "Slider display. Click in to enter value from keyboard. Click and scroll on value increment/decrement."

TT_SAMPLER_OFFSET = "Offset time into source sound."
TT_SAMPLER_LOOP = "Direction of loop."
TT_SAMPLER_START = "Start from loop point."
TT_SAMPLER_LOOP_IN = "Set loop in point."
TT_SAMPLER_LOOP_DUR = "Set loop duration."
TT_SAMPLER_CROSSFADE = "Set duration of loop crossfade."
TT_SAMPLER_GAIN = "Set input gain of source sound."
TT_SAMPLER_TRANSPO = "Set transposition of source sound."

TT_STOCH_TYPE = "Type of random distribution."
TT_STOCH_INTERP = "Interpolation method between points."
TT_STOCH_POINTS = "Number of points over which to draw the function."
TT_STOCH_MIN = "Minimum value (mapped over range of parameter)."
TT_STOCH_MAX = "Maximum value (mapped over range of parameter)."
TT_STOCH_X1 = "Distribution specific parameter."
TT_STOCH_X2 = "Distribution specific parameter."

TT_WAVE_SHAPE = "Waveshape."
TT_WAVE_POINTS = "Number of points over which to draw the function."
TT_WAVE_AMP = "Amplitude waveform."
TT_WAVE_FREQ = "Frequency of waveform."
TT_WAVE_PHASE = "Phase of waveform."
TT_WAVE_WIDTH = "Pulse width (square waveform only)."

TT_GRAPHER = """
Pointer tool: Click on graph line to select. Click and drag line to move it horizontally. Double-click to toggle between curved and straight line.
Click on point or drag to select points. Double-click anywhere to add point. Delete key to delete selected points.

Pencil tool: Click anywhere to add point. Click and drag to add multiple points.

Zoom tool: Click and drag to zoom a region. Escape key to reset zoom level.

Hand tool: Click and drag to move view of the grapher.              
"""

TT_RANGE_LABEL = "Parameter name for slider. Click on the left side of label to select minimum value in grapher. Click on the right side of label to select maximum value in grapher. Shift-click to solo in grapher. Right-click starts midi learn. Shit-Right-click removed midi binding."

TT_POLY_LABEL = "Number of independent notes generated."
TT_POLY_SPREAD = "Pitch spread between individual notes."

TT_POST_ITEMS = "Choose a post-processing module. Parameters appear on the left buttons. Signal routing is from top to bottom. Computation must be restarted for the post-processing to take effects."
