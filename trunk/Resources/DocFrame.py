#!/usr/bin/env python
# encoding: utf-8
import os, keyword
import wx
import wx.stc  as  stc
from wx.lib.embeddedimage import PyEmbeddedImage
import CeciliaLib
from constants import *
from pyo import class_args
from API_interface import *

# ***************** Catalog starts here *******************

catalog = {}

#----------------------------------------------------------------------
next_24_png = PyEmbeddedImage(
    "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"
    "QmCC")
catalog['next_24.png'] = next_24_png

#----------------------------------------------------------------------
previous_24_png = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAA"
    "F2+SX8VGAAAHWklEQVR42mJkaGRABf8ZGJgZmRn+/v/LzMrC6irPr+AmzS1jKsAhIA2UEvr/"
    "/9+7d//ePXty9vGZxy8e7f63/d9Oho8MfxhwAIAAYsSwAKiUlY3Vz1barsxczNJagFWY4d/f"
    "fwx///1j+PfvL8M/oAv+MwIdwcnA8PbPW4Yzd0+eOL7+aPe/Pf/WYbMAIIBQLfjLwCbLJ9cb"
    "pRGbI8kuzfDm61uGL7++MPz59wfstX///wN9BrQICEGAg4WTQYhPkOEN+0uGdRtWzX6+6FkR"
    "w3uGL8gWAAQQM4Mj3OXs2uK689N1spOZf7MxPPv8nOHnn59gw4BuBhv8hxHIYwT5AOgjoPj3"
    "/z8Y3n1/z8D9h4fBxMTM+LXcC623p95uZ/jF8BNmAUAAMTM4gF3OICMgOzEDaPjnr18Z3v94"
    "DzYWZAzMxb/+/2H4+PkTw7fv3xj+s/xnYGRhBFvyn+k/w+c/QF/+/MdgoGWocZfttvTX01+2"
    "gLUDAUAAMTPYMzCwsbB5p+tmTWD+w8bwHuii/0BX/v0HMhxoBNC13//+Yvjx6TtDoI4Pg42i"
    "BcPdF/cYPjICQ4IF6DYmoPXM/xm+/f/GwPiHmUHNSE3/8t0L9/49/HcRZAFAADEz2DGw2srZ"
    "LzIRspAGBQsoOP6AXf4HHBzf//1g+P7hC0OGbQqDr4kng4qEEgPTf2aGw0+PM7DysjH8Y2IA"
    "WvAPlPQYPv/9yiDGJcHwV/KX2tNdT1YAjfkOEEBMzGzMLhbi1qavv70FRiI4UMCuhxn+7cNX"
    "hiy7NAZHHTt4xD3/+pLhB8svhk//vjC8+/Oe4f2fjwwfgPgHMOgff3rGoKGlq8VsyuwPUgsQ"
    "QCwyfLJuQmzCDM++PYdHJjhYoIZn26IavujsCobSI1UMX3h+MzB9ZgKnLhZmFqCvmBgYGYHp"
    "F5jSDJj0GIT0RVxeH325ECCAWBR4FU3//PkDToqQiAVF6G9gsHxjyAa5XBth+JZrOxjKtlQx"
    "/OdgYhD5yc/AzMQMNvTT/88MTLzMDExA9i9gfL35/IaBT4tf9zXLSxGAAGIRYBeQAmcikPGM"
    "4IzM8P7NO4Ysm1QUw0HAGhjB10rOMLAwsYAcygByMEjDuqubGWrONDMw8jMxsP9lA/qImYGV"
    "k1eMgYlBACCAgGngvxAozBkZmcBBdOz+cYYfv34xuOk7Y+RKQU4BBiFuIQY+Tj4Gfi4+MM0H"
    "pOONoxlUeBQYOFhZGXg4OBk42NgZmNmY+BgYGbgAAgiY0BjeMTMz83//851h/93DDPff32J4"
    "yPSAYfe1/QyuWo4oFrz79h4cJMxA+P8/JKEDA4nhMNBR35i/Mghy8zP8/fuXgZ+Th+Hjh++f"
    "gQr+AAQQyyeGj8+//f6muP36bobnnx8zMHBxMHxm+sIQviKGYVX0UgYXdQe4Bdtu7mJo2NvC"
    "wCvEw8DFzsXABgwqVmBw/GD6ycAnzs3AxMQEzP2/gb7jZXj549FroAVfAAKImVGJ0eAr62/z"
    "yw/PAwsXDmBJBwxYThaGHxxfGbZc3cFgKm7CoCgsD7ZAT1KHgZWJjeHYm+MMHOJsDBz8bAzs"
    "AqwMvAIgC4FBwwIJf3F+MYYL288f/nzi81KAAGL+BIQC+iJR7z5+BebKPxAL2IDJj5OV4Qfr"
    "d4Zt13YzmIkZMygIywFLUwYGM1kjhp/f/jDc+nqdQVhAkIGXg5uBB2g4JzDc2VhYgcHDBy51"
    "j8w8Muv/0/+HAQKI6d/Zf7s/vn99Tl5MFlIoMYEDFphEgPYAg+Ej92eG+G3pDPtuHQEGASSo"
    "ZHnlGNiZ2cARysfJxSAADBJBbl4Gfm5uoG/lGK6dv3rn75m/u0BqAQKImeE3w9/PDJ9eK9kp"
    "h3/5DCwGgWUKAwcwTbMwAdM5Ezisf3P8Zjhy7wgwCXIxPP/4imHDwzUMzEIMDAJAQ0E+4OXi"
    "AqpjZxDnEWd4/fUdw5radd3AsmgbyMUAAQRyK8O/x/9ufBP/JKuuq2309guwemL+xcDICoxA"
    "YEZiBeZSbmAQMHD/Yzj1+iTDqffHGf4L/mUQ5OUHi/NxcAF9wc0gzSsOLGFZGCa1T9vycdXH"
    "DlB2ApkNEEBgC0Dp7cftH/v+qv/SUlfX0vj6C1jA/fsGzFBAC4DhCrKEg5WdgYeXm4GbDxjm"
    "QEM5WdnAYpzsbAyyfNIMzMAInjBx2sFbHXfKgObdgWRBBgaAAGKGp8EfDL++XPy87Rv/J0lV"
    "IzUDHlZ+hu/ACgdYOjEwMzOBLWFlZmVgA9FAl4IiVIiTn0GGX5rhyceXDF3NEzbfbL9dBgzy"
    "yxAnQwBAADFiq0eZHZnj5ANUisQUpfX/A+PhL7CsYmFhZuBi4wBnIgFuPgZhYBD9/v2T4cKZ"
    "CzcOzTyy8P/R/0uBWp8iGw4CAAHEiKs1wMDGIMhszuwjpCvsJqgjos/NxSPGwsbMx/qf+fP3"
    "799ev7706vqzM8+O/Dvxbzc0SH5hMwYggHBbgAxYGYAxyMAPZHGB6yNgDgWG3Bsg/wshrQAB"
    "BgD9qrwV+ofghAAAAABJRU5ErkJggg==")
catalog['previous_24.png'] = previous_24_png

#----------------------------------------------------------------------
up_24_png = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwY"
    "AAAABGdBTUEAALGOfPtRkwAAACBjSFJNAAB6JQAAgIMAAPn/AACA6QAAdTAAAOpgAAA6mAAA"
    "F2+SX8VGAAAEpElEQVR42mJkmMZAGPxnYGBmZo61kLZsPb3uVMuv+b9mMRAJAAKImcGbgIp/"
    "DAyMTIzREQoxc825bIW41Li97v25/fLf1X9nibEAIIDwWwA0nI2FLTpKMXaeKKM027WPNxlE"
    "OcSZJEwkPe//JM4SgADCbQHQcHYW9uhY5cR5PP9F2O59fcDAwMrI8PnPZwYhFlEmSWMpzwe/"
    "7hC0BCCAsFsANTxaOWEex18+tnvfgIazMDD8BUr8+/+P4fOvL0BLRJikjKWBltzFawlAAGFa"
    "gGQ4+z9etvvfHjIwMjMy/P33l+Ev0PD/DCDMwPAVaIkgqzCTtAnQkp+4LQEIIFQLgIZzsHBE"
    "x6skz2P9x8N2/+tDBgYmoOH//4DcDnQ92A8M/xlBGGjJb6BPWEWYZIxlPR98A1pyHdMSgABC"
    "WAAzXDVlHutfbmCwAA1nZgC7GhQsYMgISlIQ5YxAmglo+be/3xlE2MWY5ICW3P8MtOQGqiUA"
    "AQSxAGp4AtBwtr884GBhZmYCBwUoSP4AffD732+GH/9+MPz4+4Ph57+fYPwLiP8BY+bjz48M"
    "ghzCTLKGMp4PP95/+e8WwhKAAGJkmMrAwMXMFR0HDBb2v8Aw//6Q4Q/jX4Yvf76CNX76/Ynh"
    "259vYEsYmICeYmJiYGZkBjuABchmZGQC5RNgSDIyiPOIMTD/+fv3xIwj2b+2/ZoJsgAggJhZ"
    "wlmy47QT58jzKjO/ZHjN8J/zH8OHXx8Y7r17wHD30wOGr0DDQcHDBDaQmYGFmYWBlQWIgTQT"
    "MzODGKcIgxSfBIMQLz8DKxsLg5SQNJOQvpDPww/3v/2//f8EQACx/F3zV3wl6/J5f/79+Q90"
    "xf8///7+4Nfms9KwNDV69ugFAwcrG9BgFiTDmeFsoOMZhHkEGE5vOHLp681vx4DhyfL/Pzie"
    "mP9//68A9LEoQACx/N/8v+4Tw0eUmOdgZK9ncmA0AgcHEyg4mME0yHCQy1mYITQ4aNiAme/y"
    "l6PfD3zLwpJK2QACiAVDSBvoAE+gxh+MDCygsAZawgJ0KiszzOUQw0EYFA9gmoWJFUc++wUQ"
    "QCzohjOkM4ByLSPjPya4y0E0C9jlLHDDWVlYgTQTAxszKzgV4gIAAYSwQAuIUyBFM8MPBnCq"
    "YIIFERPEJ6xQ17NBI5mVFcIH68EBAAKICUxqAnESwnBg0gaHLyRJQpIjzCJYBIMsYQP7ggWv"
    "DwACiAVseBwkszH8gor+BSV5UNpmgvuCBZRMwRjoaiakoALy8fkAIIBYGKKgLv+JqL0Y/oCK"
    "AkYwZoYFFSjCGaG+YEbkBxZG/D4ACCAWkGtBBiJXjxA+KIgghkPiAxpkUAy2hAmSZBnxWAAQ"
    "QCwMvzHrX3AcoKuE+giEmaAYZhk+ABCAjjpIAgCCYSgahrTF9P5ntTDK1sgNsni/PPcOxJVy"
    "tw6fjsEWISQkRCsJo1zdWgWmAjfHDdJnWwCxMHzG9MGXn1++P7h66xv7X2ABzfid4SfjT2Co"
    "MTN8B5rzCSlVgeLhFssthh8/fvxigHgaI7oBAoiRgR1rM4UXGHTyQBY72E//8YYC0DagM/8y"
    "3Aey0QOcASDAAN0xfmdOgZiqAAAAAElFTkSuQmCC")
catalog['up_24.png'] = up_24_png

_INTRO_TEXT =   """
"Cecilia5 API documentation"

# What is a Cecilia module

A Cecilia module is a python file (with the extension 'C5', associated to 
the application) containing a class named `Module`, within which the audio 
processing chain is developed, and a list called `Interface`, telling the 
software what are the graphical controls necessary for the proper operation 
of the module. the file can then be loaded by the application to apply the 
process on different audio signals, whether coming from sound files or from
the microphone input. Processes used to manipulate the audio signal must be 
written with the Python's dedicated signal processing module 'pyo'.

# API Documentation Structure

This API is divided into two parts: firstly, there is the description of the 
parent class, named `BaseModule`, from which every module must inherit. This 
class implements a lot of features that ease the creation of a dsp chain.
Then, the various available GUI elements (widgets) are presented.

"""

_EXAMPLE_1 = '''
                            ### EXAMPLE 1 ###
# This example shows how to use the sampler to loop any soundfile from the disk.
# A state-variable filter is then applied on the looped sound. 

class Module(BaseModule):
    """
    "State Variable Filter"
    
    Description

    This module implements lowpass, bandpass and highpass filters in parallel
    and allow the user to interpolate on an axis lp -> bp -> hp.
    
    Sliders
    
        # Cutoff/Center Freq : 
                Cutoff frequency for lp and hp (center freq for bp)
        # Filter Q : 
                Q factor (inverse of bandwidth) of the filter
        # Type (lp->bp->hp) : 
                Interpolating factor between filters
        # Dry / Wet : 
                Mix between the original and the filtered signals

    Graph Only
    
        # Overall Amplitude : 
                The amplitude curve applied on the total duration of the performance
    
    Popups & Toggles
    
        # Polyphony Voices : 
                Number of voices played simultaneously (polyphony), 
                only available at initialization time
        # Polyphony Chords : 
                Pitch interval between voices (chords), 
                only available at initialization time

    """
    def __init__(self):
        BaseModule.__init__(self)
        self.snd = self.addSampler("snd")
        self.dsp = SVF(self.snd, self.freq, self.q, self.type)
        self.out = Interp(self.snd, self.dsp, self.drywet, mul=self.env)

Interface = [
    csampler(name="snd"),
    cgraph(name="env", label="Overall Amplitude", func=[(0,1),(1,1)], col="blue1"),
    cslider(name="freq", label="Cutoff/Center Freq", min=20, max=20000, init=1000, 
            rel="log", unit="Hz", col="green1"),
    cslider(name="q", label="Filter Q", min=0.5, max=25, init=1, rel="log", 
            unit="x", col="green2"),
    cslider(name="type", label="Type (lp->bp->hp)", min=0, max=1, init=0.5, 
            rel="lin", unit="x", col="green3"),
    cslider(name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", 
            unit="x", col="blue1"),
    cpoly()
]

'''

_EXAMPLE_2 = '''
                            ### EXAMPLE 2 ###
# This example shows how to load a sound in a table (RAM) in order to apply
# non-streaming effects. Here a frequency self-modulated reader is used to
# create new harmonics, in a way similar to waveshaping distortion.

class Module(BaseModule):
    """
    "Self-modulated frequency sound looper"
    
    Description
    
    This module loads a sound in a table and apply a frequency self-modulated
    playback of the content. A Frequency self-modulation occurs when the
    output sound of the playback is used to modulate the reading pointer speed.
    That produces new harmonics in a way similar to waveshaping distortion. 
    
    Sliders
    
        # Transposition : 
                Transposition, in cents, of the input sound
        # Feedback : 
                Amount of self-modulation in sound playback
        # Filter Frequency : 
                Frequency, in Hertz, of the filter
        # Filter Q : 
                Q of the filter (inverse of the bandwidth)
    
    Graph Only
    
        # Overall Amplitude : 
                The amplitude curve applied on the total duration of the performance

    Popups & Toggles
    
        # Filter Type : 
                Type of the filter
        # Polyphony Voices : 
                Number of voices played simultaneously (polyphony), 
                only available at initialization time
        # Polyphony Chords : 
                Pitch interval between voices (chords), 
                only available at initialization time

    """
    def __init__(self):
        BaseModule.__init__(self)
        self.snd = self.addFilein("snd")
        self.trfactor = CentsToTranspo(self.transpo, mul=self.polyphony_spread)
        self.freq = Sig(self.trfactor, mul=self.snd.getRate())
        self.dsp = OscLoop(self.snd, self.freq, self.feed*0.0002, 
                           mul=self.polyphony_scaling * 0.5)
        self.mix = self.dsp.mix(self.nchnls)
        self.out = Biquad(self.mix, freq=self.filt_f, q=self.filt_q, 
                          type=self.filt_t_index, mul=self.env)

    def filt_t(self, index, value):
        self.out.type = index

Interface = [
    cfilein(name="snd"),
    cgraph(name="env", label="Overall Amplitude", func=[(0,1),(1,1)], col="blue1"),
    cslider(name="transpo", label="Transposition", min=-4800, max=4800, init=0, 
            unit="cnts", col="red1"),
    cslider(name="feed", label="Feedback", min=0, max=1, init=0.25, unit="x", 
            col="purple1"),
    cslider(name="filt_f", label="Filter Frequency", min=20, max=18000, 
            init=10000, rel="log", unit="Hz", col="green1"),
    cslider(name="filt_q", label="Filter Q", min=0.5, max=25, init=1, 
            rel="log", unit="x", col="green2"),
    cpopup(name="filt_t", label="Filter Type", init="Lowpass", 
           value=["Lowpass", "Highpass", "Bandpass", "Bandreject"], col="green1"),
    cpoly()
]

'''

_COLOUR_TEXT = """
Colours

Five colours, with four shades each, are available to build the interface.
The colour should be given, as a string, to the `col` argument of a widget
function.
    
            red1    blue1    green1    purple1    orange1 
            red2    blue2    green2    purple2    orange2 
            red3    blue3    green3    purple3    orange3 
            red4    blue4    green4    purple4    orange4

"""

_MODULES_TEXT =   """
"Documentation of builtin modules" 

The builtin modules are classified into different categories:

"""

_CATEGORY_OVERVIEW = {  'Dynamics': """
"Modules related to waveshaping and amplitude manipulations"

""", 
                        'Filters': """
"Filtering and subtractive synthesis modules"

""", 
                        'Multiband': """
"Various processing applied independently to four spectral regions" 

""", 
                        'Pitch': """
"Modules related to playback speed and pitch manipulations"

""", 
                        'Resonators&Verbs': """
"Artificial spaces generation modules"

""", 
                        'Spectral': """
"Spectral streaming processing modules"

""", 
                        'Synthesis': """
"Additive synthesis and particle generators"

""", 
                        'Time': """ 
"Granulation based time-stretching and delay related modules"

"""}

_MODULE_CATEGORIES = ['Dynamics', 'Filters', 'Multiband', 'Pitch', 'Resonators&Verbs', 'Spectral', 'Synthesis', 'Time']
_DOC_KEYWORDS = ['Attributes', 'Examples', 'Parameters', 'Methods', 'Notes', 'Methods details', 'Public', "BaseModule_API", "Interface_API", 
                 'Notes', 'Overview', 'Initline', 'Description', 'Sliders', 'Graph Only', 'Popups & Toggles', 'Template', 'Colours']
_KEYWORDS_LIST = ["cfilein", "csampler", "cpoly", "cgraph", "cslider", "crange", "csplitter",
                    "ctoggle", "cpopup", "cbutton", "cgen"]
_KEYWORDS_TREE = {"BaseModule_API": [], "Interface_API": ["cfilein", "csampler", "cpoly", "cgraph", "cslider", "crange", "csplitter",
                    "ctoggle", "cpopup", "cbutton", "cgen"]}
_NUM_PAGES = len(_KEYWORDS_LIST)

DOC_STYLES = {'Default': {'default': '#000000', 'comment': '#003333', 'commentblock': '#000000', 'selback': '#CCCCCC',
                    'number': '#000000', 'string': '#000000', 'triple': '#000000', 'keyword': '#00007F', 'keyword2': '#003333',
                    'class': '#0000FF', 'function': '#007F7F', 'identifier': '#000000', 'caret': '#00007E',
                    'background': '#EEEEEE', 'linenumber': '#000000', 'marginback': '#B0B0B0', 'markerfg': '#CCCCCC',
                      'markerbg': '#000000', 'bracelight': '#AABBDD', 'bracebad': '#DD0000', 'lineedge': '#CCCCCC'}}
if wx.Platform == '__WXMSW__':
  DOC_FACES = {'face': 'Verdana', 'size' : 8, 'size2': 7}
elif wx.Platform == '__WXMAC__':
  DOC_FACES = {'face': 'Monaco', 'size' : 12, 'size2': 9}
else:
  DOC_FACES = {'face': 'Monospace', 'size' : 8, 'size2': 7}
DOC_FACES['size3'] = DOC_FACES['size2'] + 4
DOC_FACES['size4'] = DOC_FACES['size2'] + 3
for key, value in DOC_STYLES['Default'].items():
  DOC_FACES[key] = value

DOC_STYLES_P = {'Default': {'default': '#000000', 'comment': '#007F7F', 'commentblock': '#7F7F7F', 'selback': '#CCCCCC',
                    'number': '#005000', 'string': '#7F007F', 'triple': '#7F0000', 'keyword': '#00007F', 'keyword2': '#007F9F',
                    'class': '#0000FF', 'function': '#007F7F', 'identifier': '#000000', 'caret': '#00007E',
                    'background': '#EEEEEE', 'linenumber': '#000000', 'marginback': '#B0B0B0', 'markerfg': '#CCCCCC',
                      'markerbg': '#000000', 'bracelight': '#AABBDD', 'bracebad': '#DD0000', 'lineedge': '#CCCCCC'}}

if wx.Platform == '__WXMSW__':
  DOC_FACES_P = {'face': 'Verdana', 'size' : 8, 'size2': 7}
elif wx.Platform == '__WXMAC__':
  DOC_FACES_P = {'face': 'Monaco', 'size' : 12, 'size2': 9}
else:
  DOC_FACES_P = {'face': 'Monospace', 'size' : 8, 'size2': 7}
DOC_FACES_P['size3'] = DOC_FACES_P['size2'] + 4
for key, value in DOC_STYLES_P['Default'].items():
  DOC_FACES_P[key] = value


def _ed_set_style(editor, searchKey=None):
    editor.SetLexer(stc.STC_LEX_PYTHON)
    editor.SetKeyWords(0, " ".join(_KEYWORDS_LIST))
    if searchKey == None:
        editor.SetKeyWords(1, " ".join(_DOC_KEYWORDS))
    else:
        editor.SetKeyWords(1, " ".join(_DOC_KEYWORDS) + " " + searchKey)

    editor.SetMargins(5,5)
    editor.SetSTCCursor(2)
    editor.SetIndent(4)
    editor.SetTabIndents(True)
    editor.SetTabWidth(4)
    editor.SetUseTabs(False)

    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,  "fore:%(default)s,face:%(face)s,size:%(size)d,back:%(background)s" % DOC_FACES)
    editor.StyleClearAll()
    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "fore:%(default)s,face:%(face)s,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "fore:%(linenumber)s,back:%(marginback)s,face:%(face)s,size:%(size2)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "fore:%(default)s,face:%(face)s" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_DEFAULT, "fore:%(default)s,face:%(face)s,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:%(comment)s,face:%(face)s,bold,italic,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_NUMBER, "fore:%(number)s,face:%(face)s,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_STRING, "fore:%(string)s,face:%(face)s,bold,size:%(size4)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_CHARACTER, "fore:%(string)s,face:%(face)s,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_WORD, "fore:%(keyword)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_WORD2, "fore:%(keyword2)s,face:%(face)s,bold,size:%(size3)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_TRIPLE, "fore:%(triple)s,face:%(face)s,bold,size:%(size4)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:%(triple)s,face:%(face)s,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:%(class)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_DEFNAME, "fore:%(function)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d,face:%(face)s" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:%(identifier)s,face:%(face)s,size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:%(commentblock)s,face:%(face)s,italic,size:%(size)d" % DOC_FACES)

def _ed_set_style_p(editor, searchKey=None):
    editor.SetLexer(stc.STC_LEX_PYTHON)
    editor.SetKeyWords(0, " ".join(keyword.kwlist) + " None True False ")

    editor.SetMargins(5,5)
    editor.SetSTCCursor(2)
    editor.SetIndent(4)
    editor.SetTabIndents(True)
    editor.SetTabWidth(4)
    editor.SetUseTabs(False)

    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,  "fore:%(default)s,face:%(face)s,size:%(size)d,back:%(background)s" % DOC_FACES_P)
    editor.StyleClearAll()
    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "fore:%(default)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "fore:%(linenumber)s,back:%(marginback)s,face:%(face)s,size:%(size2)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "fore:%(default)s,face:%(face)s" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_DEFAULT, "fore:%(default)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:%(comment)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_NUMBER, "fore:%(number)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_STRING, "fore:%(string)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_CHARACTER, "fore:%(string)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_WORD, "fore:%(keyword)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_WORD2, "fore:%(keyword2)s,face:%(face)s,bold,size:%(size3)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_TRIPLE, "fore:%(triple)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:%(triple)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:%(class)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_DEFNAME, "fore:%(function)s,face:%(face)s,bold,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d,face:%(face)s" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:%(identifier)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:%(commentblock)s,face:%(face)s,size:%(size)d" % DOC_FACES_P)

def complete_words_from_str(text, keyword):
    words = [keyword]
    keyword = keyword.lower()
    text_ori = text
    text = text.replace("`", " ").replace("'", " ").replace(".", " ").replace(",", " ").replace('"', " ").replace("=", " ").replace("\n", " ").lower()
    found = text.find(keyword)
    while found > -1:
        start = text.rfind(" ", 0, found)
        end = text.find(" ", found)
        words.append(text_ori[start:end])
        found = text.find(keyword, found+1)
    words = " ".join(words)
    return words

class ManualPanel(wx.Treebook):
    def __init__(self, parent):
        wx.Treebook.__init__(self, parent, -1, size=(600,480), style=wx.BK_DEFAULT | wx.SUNKEN_BORDER)
        self.parent = parent
        self.searchKey = None
        if not os.path.isdir(DOC_PATH):
            os.mkdir(DOC_PATH)
        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED, self.OnPageChanged)

    def cleanup(self):
        self.searchKey = None
        self.DeleteAllPages()
        self.reset_history()

    def reset_history(self):
        self.fromToolbar = False
        self.oldPage = ""
        self.sequence = []
        self.seq_index = 0

    def AdjustSize(self):
        self.GetTreeCtrl().InvalidateBestSize()
        self.SendSizeEvent()

    def copy(self):
        self.GetPage(self.GetSelection()).win.Copy()

    def collapseAll(self):
        count = self.GetPageCount()
        for i in range(count):
            if self.IsNodeExpanded(i):
                self.CollapseNode(i)

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        if new != old:
            text = self.GetPageText(new)
            self.getPage(text)
        event.Skip()

    def history_check(self):
        back = True
        forward = True
        if self.seq_index <= 0:
            back = False
        if self.seq_index == (len(self.sequence) - 1):
            forward = False
        self.parent.history_check(back, forward)

    def history_back(self):
        self.seq_index -= 1
        if self.seq_index < 0:
            self.seq_index = 0
        self.fromToolbar = True
        self.SetSelection(self.sequence[self.seq_index])
        self.history_check()

    def history_forward(self):
        seq_len = len(self.sequence)
        self.seq_index += 1
        if self.seq_index == seq_len:
            self.seq_index = seq_len - 1
        self.fromToolbar = True
        self.SetSelection(self.sequence[self.seq_index])
        self.history_check()

    def setStyle(self):
        tree = self.GetTreeCtrl()
        tree.SetBackgroundColour(DOC_STYLES['Default']['background'])
        root = tree.GetRootItem()
        tree.SetItemTextColour(root, DOC_STYLES['Default']['identifier'])
        (child, cookie) = tree.GetFirstChild(root)
        while child.IsOk():
            tree.SetItemTextColour(child, DOC_STYLES['Default']['identifier'])
            if tree.ItemHasChildren(child):
                (child2, cookie2) = tree.GetFirstChild(child)
                while child2.IsOk():
                    tree.SetItemTextColour(child2, DOC_STYLES['Default']['identifier'])
                    (child2, cookie2) = tree.GetNextChild(child, cookie2)
            (child, cookie) = tree.GetNextChild(root, cookie)
        
class ManualPanel_modules(ManualPanel):
    def __init__(self, parent):
        ManualPanel.__init__(self, parent)
        self.root, self.directories, self.files = CeciliaLib.buildFileTree()
        self.parse()

    def parse(self):
        self.cleanup()
        self.needToParse = True
        count = 1
        win = self.makePanel("Modules")
        self.AddPage(win, "Modules")
        for key in self.directories:
            count += 1
            win = self.makePanel(key)
            self.AddPage(win, key)
            for key2 in self.files[key]:
                count += 1
                win = self.makePanel(os.path.join(self.root, key, key2))
                self.AddSubPage(win, key2)
        self.setStyle()
        self.getPage("Modules")
        wx.FutureCall(100, self.AdjustSize)

    def parseOnSearchName(self, keyword):
        self.cleanup()
        keyword = keyword.lower()
        for key in self.directories:
            for key2 in self.files[key]:
                if keyword in key2.lower():
                    win = self.makePanel(os.path.join(self.root, key, key2))
                    self.AddPage(win, key2)
        self.setStyle()
        wx.CallAfter(self.AdjustSize)

    def parseOnSearchPage(self, keyword):
        self.cleanup()
        keyword = keyword.lower()
        for key in self.directories:
            for key2 in self.files[key]:
                with open(os.path.join(self.root, key, key2), "r") as f:
                    text = f.read().lower()
                    first = text.find('"""')
                    if first != -1:
                        newline = text.find("\n", first)
                        second = text.find('"""', newline)
                        text = text[newline+1:second]
                    else:
                        text = "module not documented..."
                    if keyword in text:
                        win = self.makePanel(os.path.join(self.root, key, key2))
                        self.AddPage(win, key2)
        self.setStyle()
        wx.CallAfter(self.AdjustSize)

    def makePanel(self, obj=None):
        panel = wx.Panel(self, -1)
        panel.isLoad = False
        if self.needToParse:
            if obj == "Modules":
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                panel.win.SetUseHorizontalScrollBar(False)
                text = "" 
                for cat in _MODULE_CATEGORIES:
                    l = _CATEGORY_OVERVIEW[cat].splitlines()[1].replace('"', '').strip()
                    text += "# %s\n    %s\n" % (cat, l)
                panel.win.SetText(_MODULES_TEXT + text)
            elif obj in _MODULE_CATEGORIES:
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                panel.win.SetUseHorizontalScrollBar(False)
                text = _CATEGORY_OVERVIEW[obj]
                for file in self.files[obj]:
                    text += "# %s\n" % file
                    with open(os.path.join(self.root, obj, file), "r") as f:
                        t = f.read()
                        first = t.find('"""')
                        if first != -1:
                            newline = t.find("\n", first)
                            second = t.find('\n', newline+2)
                            text += t[newline+1:second].replace('"', '')
                            text += "\n"
                panel.win.SetText(text)
            elif os.path.isfile(obj):
                with open(obj, "r") as f:
                    text = f.read()
                    first = text.find('"""')
                    if first != -1:
                        newline = text.find("\n", first)
                        second = text.find('"""', newline)
                        text = text[newline+1:second]
                    else:
                        text = "Module not documented..."
                obj = os.path.split(obj)[1]
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                panel.win.SetUseHorizontalScrollBar(False) 
                panel.win.SetText(text)
            else:
                print "WATH'S THIS", obj
                var = eval(obj)
                if type(var) == type(""):
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                    panel.win.SetUseHorizontalScrollBar(False) 
                    panel.win.SetText(var)
                else:
                    text = var.__doc__
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                    panel.win.SetUseHorizontalScrollBar(False) 
                    panel.win.SetText(text)
                    
            panel.win.SaveFile(CeciliaLib.ensureNFD(os.path.join(DOC_PATH, obj)))
        return panel

    def getPage(self, word):
        if word == self.oldPage:
            self.fromToolbar = False
            return
        page_count = self.GetPageCount()
        for i in range(page_count):
            text = self.GetPageText(i)
            if text == word:
                self.oldPage = word
                if not self.fromToolbar:
                    self.sequence = self.sequence[0:self.seq_index+1]
                    self.sequence.append(i)
                    self.seq_index = len(self.sequence) - 1
                    self.history_check()
                self.parent.setTitle(text)
                self.SetSelection(i)
                panel = self.GetPage(self.GetSelection())
                if not panel.isLoad:
                    panel.isLoad = True
                    panel.win = stc.StyledTextCtrl(panel, -1, size=panel.GetSize(), style=wx.SUNKEN_BORDER)
                    panel.win.SetUseHorizontalScrollBar(False) 
                    panel.win.LoadFile(os.path.join(CeciliaLib.ensureNFD(DOC_PATH), word))
                    panel.win.SetMarginWidth(1, 0)
                    if self.searchKey != None:
                        words = complete_words_from_str(panel.win.GetText(), self.searchKey)
                        _ed_set_style(panel.win, words)
                    else:
                        _ed_set_style(panel.win)
                    panel.win.SetSelectionEnd(0)

                    def OnPanelSize(evt, win=panel.win):
                        win.SetPosition((0,0))
                        win.SetSize(evt.GetSize())

                    panel.Bind(wx.EVT_SIZE, OnPanelSize)
                self.fromToolbar = False
                return
        try:
            win = self.makePanel(CeciliaLib.getVar("currentCeciliaFile"))
            self.AddPage(win, word)
            self.getPage(word)
        except:
            pass

class ManualPanel_api(ManualPanel):
    def __init__(self, parent):
        ManualPanel.__init__(self, parent)
        self.parse()
        
    def parse(self):
        self.cleanup()
        self.needToParse = True
        count = 1
        win = self.makePanel("Intro")
        self.AddPage(win, "Intro")
        for key in _KEYWORDS_TREE.keys():
            count += 1
            win = self.makePanel(key)
            self.AddPage(win, key)
            for key2 in _KEYWORDS_TREE[key]:
                count += 1
                win = self.makePanel(key2)
                self.AddPage(win, key2)
        self.setStyle()
        win = self.makePanel("Example 1")
        self.AddPage(win, "Example 1")
        win = self.makePanel("Example 2")
        self.AddPage(win, "Example 2")
        self.getPage("Intro")
        wx.FutureCall(100, self.AdjustSize)

    def parseOnSearchName(self, keyword):
        self.cleanup()
        keyword = keyword.lower()
        for key in _KEYWORDS_LIST:
            if keyword in key.lower():
                win = self.makePanel(key)
                self.AddPage(win, key)
        self.setStyle()
        self.getPage("Intro")
        wx.CallAfter(self.AdjustSize)

    def parseOnSearchPage(self, keyword):
        self.cleanup()
        keyword = keyword.lower()
        for key in _KEYWORDS_LIST:
            with open(os.path.join(DOC_PATH, key), "r") as f:
                text = f.read().lower()
                if keyword in text:
                    win = self.makePanel(key)
                    self.AddPage(win, key)
        self.setStyle()
        self.getPage("Intro")
        wx.CallAfter(self.AdjustSize)

    def makePanel(self, obj=None):
        panel = wx.Panel(self, -1)
        panel.isLoad = False
        if self.needToParse:
            if obj == "Intro":
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                panel.win.SetUseHorizontalScrollBar(False) 
                panel.win.SetText(_INTRO_TEXT)
            elif "Example" in obj:
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                panel.win.SetUseHorizontalScrollBar(False)
                if "1" in obj:
                    panel.win.SetText(_EXAMPLE_1)                
                elif "2" in obj:
                    panel.win.SetText(_EXAMPLE_2)                
            else:
                var = eval(obj)
                if type(var) == type(""):
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                    panel.win.SetUseHorizontalScrollBar(False) 
                    if "Interface_API" in var:
                        for word in _KEYWORDS_LIST:
                            lines = eval(word).__doc__.splitlines()
                            line = "%s : %s\n" % (word, lines[1].replace('"', '').strip())
                            var += line
                        var += _COLOUR_TEXT
                    panel.win.SetText(var)
                else:
                    text = var.__doc__
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.SUNKEN_BORDER)
                    panel.win.SetUseHorizontalScrollBar(False) 
                    panel.win.SetText(text)
                    
            panel.win.SaveFile(CeciliaLib.ensureNFD(os.path.join(DOC_PATH, obj)))
        return panel

    def getPage(self, word):
        if word == self.oldPage:
            self.fromToolbar = False
            return
        page_count = self.GetPageCount()
        for i in range(page_count):
            text = self.GetPageText(i)
            if text == word:
                self.oldPage = word
                if not self.fromToolbar:
                    self.sequence = self.sequence[0:self.seq_index+1]
                    self.sequence.append(i)
                    self.seq_index = len(self.sequence) - 1
                    self.history_check()
                self.parent.setTitle(text)
                self.SetSelection(i)
                panel = self.GetPage(self.GetSelection())
                if not panel.isLoad:
                    panel.isLoad = True
                    panel.win = stc.StyledTextCtrl(panel, -1, size=panel.GetSize(), style=wx.SUNKEN_BORDER)
                    panel.win.SetUseHorizontalScrollBar(False) 
                    panel.win.LoadFile(os.path.join(CeciliaLib.ensureNFD(DOC_PATH), word))
                    panel.win.SetMarginWidth(1, 0)
                    if self.searchKey != None:
                        words = complete_words_from_str(panel.win.GetText(), self.searchKey)
                        _ed_set_style(panel.win, words)
                    else:
                        if "Example" in word:
                            _ed_set_style_p(panel.win)
                        else:
                            _ed_set_style(panel.win)
                    panel.win.SetSelectionEnd(0)

                    def OnPanelSize(evt, win=panel.win):
                        win.SetPosition((0,0))
                        win.SetSize(evt.GetSize())

                    panel.Bind(wx.EVT_SIZE, OnPanelSize)
                self.fromToolbar = False
                return

class ManualFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, size=(800, 600), kind="api"):
        if kind == "api":
            title='API Documentation'
        else:
            title='Modules Documentation'
        wx.Frame.__init__(self, parent=parent, id=id, title=title, size=size)
        self.SetMinSize((600, 480))

        self.kind = kind
        gosearchID = 1000
        aTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, 47, gosearchID)])
        self.SetAcceleratorTable(aTable)
        self.Bind(wx.EVT_MENU, self.setSearchFocus, id=gosearchID)

        tb_size = 24

        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((tb_size, tb_size))  # sets icon size

        back_ico = catalog["previous_%d.png" % tb_size]
        forward_ico = catalog["next_%d.png" % tb_size]
        home_ico = catalog["up_%d.png" % tb_size]

        backTool = self.toolbar.AddSimpleTool(wx.ID_BACKWARD, back_ico.GetBitmap(), "Back")
        self.toolbar.EnableTool(wx.ID_BACKWARD, False)
        self.Bind(wx.EVT_MENU, self.onBack, backTool)

        self.toolbar.AddSeparator()

        forwardTool = self.toolbar.AddSimpleTool(wx.ID_FORWARD, forward_ico.GetBitmap(), "Forward")
        self.toolbar.EnableTool(wx.ID_FORWARD, False)
        self.Bind(wx.EVT_MENU, self.onForward, forwardTool)

        self.toolbar.AddSeparator()

        homeTool = self.toolbar.AddSimpleTool(wx.ID_HOME, home_ico.GetBitmap(), "Go Home")
        self.toolbar.EnableTool(wx.ID_HOME, True)
        self.Bind(wx.EVT_MENU, self.onHome, homeTool)

        self.toolbar.AddSeparator()

        self.searchTimer = None
        self.searchScope = "Page Names"
        self.searchMenu = wx.Menu()
        item = self.searchMenu.Append(-1, "Search Scope")
        item.Enable(False)
        for i, txt in enumerate(["Page Names", "Manual Pages"]):
            id = i+10
            self.searchMenu.Append(id, txt)
            self.Bind(wx.EVT_MENU, self.onSearchScope, id=id)

        self.search = wx.SearchCtrl(self.toolbar, 200, size=(200,-1), style=wx.WANTS_CHARS | wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        self.search.SetMenu(self.searchMenu)
        self.toolbar.AddControl(self.search)
        self.Bind(wx.EVT_TEXT, self.onSearch, id=200)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSearchEnter, id=200)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onSearchCancel, id=200)

        self.toolbar.Realize()

        self.status = wx.StatusBar(self, -1)
        self.SetStatusBar(self.status)

        if kind == "api":
            self.doc_panel = ManualPanel_api(self)
            self.doc_panel.getPage("Intro")
        else:
            self.doc_panel = ManualPanel_modules(self)
            self.doc_panel.getPage("Modules")
            
        self.menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(99, "Close\tCtrl+W")
        self.menuBar.Append(menu1, 'File')
        menu2 = wx.Menu()
        menu2.Append(101, "Copy\tCtrl+C")
        self.menuBar.Append(menu2, 'Text')
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, self.copy, id=101)
        self.Bind(wx.EVT_MENU, self.close, id=99)
        self.Bind(wx.EVT_CLOSE, self.close)

    def openPage(self, page):
        self.doc_panel.getPage(page)
        if not self.IsShownOnScreen():
            self.Show()
        self.Raise()

    def setSearchFocus(self, evt):
        self.search.SetFocus()

    def onSearchEnter(self, evt):
        self.doc_panel.GetTreeCtrl().SetFocus()

    def onSearch(self, evt):
        if self.searchTimer != None:
            self.searchTimer.Stop()
        self.searchTimer = wx.CallLater(200, self.doSearch)

    def doSearch(self):
        keyword = self.search.GetValue()
        if keyword == "":
            self.doc_panel.parse()
        else:
            if self.searchScope == "Page Names":
                self.doc_panel.parseOnSearchName(keyword)
            else:
                self.doc_panel.parseOnSearchPage(keyword)
        self.searchTimer = None

    def onSearchCancel(self, evt):
        self.search.SetValue("")

    def onSearchScope(self, evt):
        id = evt.GetId()
        if id == 10:
            self.searchScope = "Page Names"
        else:
            self.searchScope = "Manual Pages"

    def copy(self, evt):
        self.doc_panel.copy()

    def close(self, evt):
        self.Hide()

    def setTitle(self, page):
        if self.kind == "api":
            self.SetTitle('API Documentation - %s' % page)
        else:
            self.SetTitle('Modules Documentation - %s' % page)

    def history_check(self, back, forward):
        self.toolbar.EnableTool(wx.ID_BACKWARD, back)
        self.toolbar.EnableTool(wx.ID_FORWARD, forward)

    def onBack(self, evt):
        self.doc_panel.history_back()

    def onForward(self, evt):
        self.doc_panel.history_forward()

    def onHome(self, evt):
        search = self.search.GetValue()
        if search != "":
            self.search.SetValue("")
        self.doc_panel.getPage("Intro")
        self.doc_panel.collapseAll()

if __name__ == "__main__":
    app = wx.PySimpleApp()
    doc_frame = ManualFrame()
    doc_frame.Center()
    doc_frame.Show()
    app.MainLoop()
