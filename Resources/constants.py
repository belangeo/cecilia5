"""
Copyright 2009 iACT, Universite de Montreal, Jean Piche, Olivier Belanger, Dominic Thibault

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

import os, sys

APP_NAME = 'Cecilia'
APP_VERSION = '5.0.0 beta'

ENCODING = sys.getfilesystemencoding()

if '/Cecilia.app' in os.getcwd():
    RESOURCES_PATH = os.getcwd()
else:
    RESOURCES_PATH = os.path.join(os.getcwd(), 'Resources')

if not os.path.isdir(RESOURCES_PATH) and sys.platform == "win32":
    RESOURCES_PATH = os.path.join(os.getenv("ProgramFiles"), "Cecilia", "Resources")

TMP_PATH = os.path.join(os.path.expanduser('~'), '.cecilia5')
PREFERENCES_FILE = os.path.join(TMP_PATH, 'ceciliaPrefs.txt')
MODULES_PATH = os.path.join(RESOURCES_PATH, 'modules')
HTML_PATH = os.path.join(RESOURCES_PATH, 'html')
# Folder to save automations
AUTOMATION_SAVE_PATH = os.path.join(TMP_PATH, 'automation_save')
# Icons path
ICON_PATH = os.path.join(RESOURCES_PATH, 'icons')
# Cecilia manual path
CEC_MAN_PATH = os.path.join(RESOURCES_PATH, 'help')

# Meter icons
ICON_VUMETER = os.path.join(ICON_PATH, 'vu-metre2.png')
ICON_VUMETER_DARK = os.path.join(ICON_PATH, 'vu-metre-dark2.png')

# Plugin icons
ICON_PLUGINS_KNOB = os.path.join(ICON_PATH, 'knob-trans-sm.png')
ICON_PLUGINS_KNOB_DISABLE = os.path.join(ICON_PATH, 'knob-disab-sm.png')

# Toolbox icons
ICON_TB_LOAD = os.path.join(ICON_PATH, 'load-normal-trans.png')
ICON_TB_LOAD_OVER = os.path.join(ICON_PATH, 'load-hover-trans.png')
ICON_TB_SAVE = os.path.join(ICON_PATH, 'save-normal-trans.png')
ICON_TB_SAVE_OVER = os.path.join(ICON_PATH, 'save-hover-trans.png')
ICON_TB_RESET = os.path.join(ICON_PATH, 'reset-normal-trans.png')
ICON_TB_RESET_OVER = os.path.join(ICON_PATH, 'reset-hover-trans.png')
ICON_TB_SHOW = os.path.join(ICON_PATH, 'show-normal-trans.png')
ICON_TB_SHOW_OVER = os.path.join(ICON_PATH, 'show-hover-trans.png')
ICON_TB_HIDE = os.path.join(ICON_PATH, 'hide-normal-trans.png')
ICON_TB_HIDE_OVER = os.path.join(ICON_PATH, 'hide-hover-trans.png')
ICON_TB_RECYCLE = os.path.join(ICON_PATH, 'recycle-normal-trans.png')
ICON_TB_RECYCLE_OVER = os.path.join(ICON_PATH, 'recycle-hover-trans.png')
ICON_TB_PLAY = os.path.join(ICON_PATH, 'play-normal-trans.png')
ICON_TB_PLAY_OVER = os.path.join(ICON_PATH, 'play-hover-trans.png')
ICON_TB_EDIT = os.path.join(ICON_PATH, 'edit-normal-trans.png')
ICON_TB_EDIT_OVER = os.path.join(ICON_PATH, 'edit-hover-trans.png')
ICON_TB_OPEN = os.path.join(ICON_PATH, 'open-normal-trans.png')
ICON_TB_OPEN_OVER = os.path.join(ICON_PATH, 'open-hover-trans.png')
ICON_TB_CLOSE = os.path.join(ICON_PATH, 'close-normal-trans.png')
ICON_TB_CLOSE_OVER = os.path.join(ICON_PATH, 'close-hover-trans.png')
ICON_TB_TIME = os.path.join(ICON_PATH, 'time-normal-trans.png')
ICON_TB_TIME_OVER = os.path.join(ICON_PATH, 'time-hover-trans.png')
ICON_TB_DELETE = os.path.join(ICON_PATH, 'delete-normal-trans.png')
ICON_TB_DELETE_OVER = os.path.join(ICON_PATH, 'delete-hover-trans.png')

# RadioToolbox icons
ICON_RTB_POINTER = os.path.join(ICON_PATH, 'pointer-normal-trans.png')
ICON_RTB_POINTER_OVER = os.path.join(ICON_PATH, 'pointer-hover-trans.png')
ICON_RTB_POINTER_CLICK = os.path.join(ICON_PATH, 'pointer-click-trans.png')
ICON_RTB_PENCIL = os.path.join(ICON_PATH, 'pencil-normal-trans.png')
ICON_RTB_PENCIL_OVER = os.path.join(ICON_PATH, 'pencil-hover-trans.png')
ICON_RTB_PENCIL_CLICK = os.path.join(ICON_PATH, 'pencil-click-trans.png')
ICON_RTB_ZOOM = os.path.join(ICON_PATH, 'zoom-normal-trans.png')
ICON_RTB_ZOOM_OVER = os.path.join(ICON_PATH, 'zoom-hover-trans.png')
ICON_RTB_ZOOM_CLICK = os.path.join(ICON_PATH, 'zoom-click-trans.png')
ICON_RTB_HAND = os.path.join(ICON_PATH, 'hand-normal-trans.png')
ICON_RTB_HAND_OVER = os.path.join(ICON_PATH, 'hand-hover-trans.png')
ICON_RTB_HAND_CLICK = os.path.join(ICON_PATH, 'hand-click-trans.png')

# PrefRadioToolbox icons
ICON_PREF_AUDIO = os.path.join(ICON_PATH, 'audio-normal-trans.png')
ICON_PREF_AUDIO_OVER = os.path.join(ICON_PATH, 'audio-hover-trans.png')
ICON_PREF_AUDIO_CLICK = os.path.join(ICON_PATH, 'audio-click-trans.png')
ICON_PREF_CECILIA = os.path.join(ICON_PATH, 'cecilia-normal-trans.png')
ICON_PREF_CECILIA_OVER = os.path.join(ICON_PATH, 'cecilia-hover-trans.png')
ICON_PREF_CECILIA_CLICK = os.path.join(ICON_PATH, 'cecilia-click-trans.png')
ICON_PREF_CSOUND = os.path.join(ICON_PATH, 'csound-normal-trans.png')
ICON_PREF_CSOUND_OVER = os.path.join(ICON_PATH, 'csound-hover-trans.png')
ICON_PREF_CSOUND_CLICK = os.path.join(ICON_PATH, 'csound-click-trans.png')
ICON_PREF_PATH = os.path.join(ICON_PATH, 'path-normal-trans.png')
ICON_PREF_PATH_OVER = os.path.join(ICON_PATH, 'path-hover-trans.png')
ICON_PREF_PATH_CLICK = os.path.join(ICON_PATH, 'path-click-trans.png')
ICON_PREF_MIDI = os.path.join(ICON_PATH, 'midi-normal-trans.png')
ICON_PREF_MIDI_OVER = os.path.join(ICON_PATH, 'midi-hover-trans.png')
ICON_PREF_MIDI_CLICK = os.path.join(ICON_PATH, 'midi-click-trans.png')

# PaletteToolBox icons
ICON_PTB_PROCESS = os.path.join(ICON_PATH, 'process-normal-trans.png')
ICON_PTB_PROCESS_OVER = os.path.join(ICON_PATH, 'process-hover-trans.png')
ICON_PTB_RANDOM = os.path.join(ICON_PATH, 'random-normal-trans.png')
ICON_PTB_RANDOM_OVER = os.path.join(ICON_PATH, 'random-hover-trans.png')
ICON_PTB_WAVES = os.path.join(ICON_PATH, 'waves-normal-trans.png')
ICON_PTB_WAVES_OVER = os.path.join(ICON_PATH, 'waves-hover-trans.png')

# Crossfade icons
ICON_XFADE_LINEAR = os.path.join(ICON_PATH, 'xfade-linear.png')
ICON_XFADE_POWER = os.path.join(ICON_PATH, 'xfade-power.png')
ICON_XFADE_SIGMOID = os.path.join(ICON_PATH, 'xfade-sigmoid.png')

# Audio drivers
if sys.platform=='darwin':
    AUDIO_DRIVERS = ['coreaudio', 'portaudio', 'jack']
    ENDOFLINE_CHAR = '\r'
elif sys.platform=='win32':
    AUDIO_DRIVERS = ['portaudio']
    ENDOFLINE_CHAR = '\r\n'
else:
    AUDIO_DRIVERS = ['portaudio', 'jack']
    ENDOFLINE_CHAR = '\n'

# MIDI drivers
MIDI_DRIVERS = ['portmidi']

# plugin types
PLUGINS_CHOICE = ['None', 'Reverb', 'Filter', 'Chorus', 'Para EQ', '3 Bands EQ', 'Compress', 'Gate', 
                    'Disto', 'AmpMod', 'Phaser', 'Delay', 'Flange', 'Harmonizer', 'Resonators', 'DeadReson']

# File Formats Availables
AUDIO_FILE_FORMATS = ['aiff', 'wav']

# Sample rates availables
SAMPLE_RATES = ['22050','44100','48000', '88200', '96000']
BIT_DEPTHS= {'16 bits int': 0, '24 bits int': 1, '32 bits int': 2, '32 bits float': 3}

BUFFER_SIZES = ['64','128','256','512','1024','2048','4096','8192','16384']

# Sizes for each panel of the preference panel
PREFERENCE_PANEL_SIZES = {  -1:(332,370), # Appearance
                            0:(332,370), # Audio
                            1:(360,375), # Csound
                            2:(380,365), # Dependencies
                            3:(332,460), # Info
                            4:(332,310), # Midi
                            }

# Menu Ids
ID_NEW = 1001
ID_OPEN = 1002
ID_SAVE = 1004
ID_SAVEAS = 1005
ID_PREF = 1011
ID_QUIT = 1012
ID_UNDO = 1013
ID_REDO = 1014
ID_CUT = 1015
ID_COPY = 1016
ID_PASTE = 1017
ID_SELECTALL = 1018
ID_REMEMBER = 1019
ID_FIND_REPLACE = 1020
ID_FONT = 1021
ID_COMMENT = 1022
ID_INDENT = 1023
ID_UPPER_POWER2 = 1024
ID_LOWER_POWER2 = 1025
ID_INDENT_ORC = 1029
ID_TAB_SCORE = 1030
ID_INSERT_PATH = 1031
ID_AUTOCOMP_OPCODE = 1032
ID_OPEN_CSD = 1033
ID_OPEN_LOG = 1037
ID_PLAY_STOP = 1034
ID_2205 = 1997
ID_4410 = 1998
ID_8820 = 1999
ID_44100 = 2001
ID_48000 = 2002
ID_88200 = 2003
ID_96000 = 2004
ID_192000 = 2005
ID_CUSTOM_SR = 2006
ID_16BIT = 2007
ID_24BIT = 2008
ID_32BIT = 2009
ID_CUSTOM_SAMPSIZE = 2010
ID_SHOW_PREVIEW = 2050
ID_SHOW_TABLE = 2051
ID_USE_MIDI = 2052
ID_OPEN_RECENT = 4000
ID_OPEN_BUILTIN = 4100
ID_UPDATE_INTERFACE = 5000

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
    TEXT_LABELFORWIDGET_FONT = 8
    SECTION_TITLE_FONT = 10
    TEXT_CHANNELNUM_FONT = 7
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

# Colours
BACKGROUND_COLOUR = "#666666"
GRAPHER_BACK_COLOUR = "#C1C1C1"
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
        'grey': [0., 0.4, 0.]
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

TT_POLY_LABEL = "Number of independent notes generated. See the Filters/Phaser module for an application example."
TT_POLY_SPREAD = "Pitch spread between individual notes. See the Filters/Phaser module for an application example."

TT_POST_ITEMS = "Choose a post-processing module. Parameters appear on the left buttons. Signal routing is from top to bottom. Computation must be restarted for the post-processing to take effects."




