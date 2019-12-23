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
import os, keyword, shutil
import wx
import wx.stc as stc
from .constants import *
from .API_interface import *
import Resources.CeciliaLib as CeciliaLib

_INTRO_TEXT = """
"Cecilia5 API Documentation"

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
    cgraph(name="env", label="Overall Amplitude", func=[(0, 1), (1, 1)], col="blue1"),
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
    cgraph(name="env", label="Overall Amplitude", func=[(0, 1), (1, 1)], col="blue1"),
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
"""

_COLOURS = """
            red1    blue1    green1    purple1    orange1
            red2    blue2    green2    purple2    orange2
            red3    blue3    green3    purple3    orange3
            red4    blue4    green4    purple4    orange4
"""

_MODULES_TEXT = """
"Documentation of Built-In Modules"

The built-in modules are classified into different categories:

"""

_CATEGORY_OVERVIEW = {'Dynamics': """
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
                 'Notes', 'Overview', 'Initline', 'Description', 'Sliders', 'Graph Only', 'Popups & Toggles', 'Template', 'Colours',
                 'Public Attributes', 'Public Methods']
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
  DOC_FACES = {'face': 'Verdana', 'size': 8, 'size2': 7}
elif wx.Platform == '__WXMAC__':
  DOC_FACES = {'face': 'Monaco', 'size': 12, 'size2': 9}
else:
  DOC_FACES = {'face': 'Monospace', 'size': 8, 'size2': 7}
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
  DOC_FACES_P = {'face': 'Verdana', 'size': 8, 'size2': 7}
elif wx.Platform == '__WXMAC__':
  DOC_FACES_P = {'face': 'Monaco', 'size': 12, 'size2': 9}
else:
  DOC_FACES_P = {'face': 'Monospace', 'size': 8, 'size2': 7}
DOC_FACES_P['size3'] = DOC_FACES_P['size2'] + 4
for key, value in DOC_STYLES_P['Default'].items():
  DOC_FACES_P[key] = value


def _ed_set_style(editor, searchKey=None):
    editor.SetLexer(stc.STC_LEX_PYTHON)
    editor.SetKeyWords(0, " ".join(_KEYWORDS_LIST))
    if searchKey is None:
        editor.SetKeyWords(1, " ".join(_DOC_KEYWORDS))
    else:
        editor.SetKeyWords(1, " ".join(_DOC_KEYWORDS) + " " + searchKey)

    editor.SetMargins(5, 5)
    editor.SetSTCCursor(2)
    editor.SetIndent(4)
    editor.SetTabIndents(True)
    editor.SetTabWidth(4)
    editor.SetUseTabs(False)

    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:%(default)s, face:%(face)s, size:%(size)d, back:%(background)s" % DOC_FACES)
    editor.StyleClearAll()
    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:%(default)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "fore:%(linenumber)s, back:%(marginback)s, face:%(face)s, size:%(size2)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "fore:%(default)s, face:%(face)s" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_DEFAULT, "fore:%(default)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:%(comment)s, face:%(face)s, bold, italic, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_NUMBER, "fore:%(number)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_STRING, "fore:%(string)s, face:%(face)s, bold, size:%(size4)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_CHARACTER, "fore:%(string)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_WORD, "fore:%(keyword)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_WORD2, "fore:%(keyword2)s, face:%(face)s, bold, size:%(size3)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_TRIPLE, "fore:%(triple)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:%(triple)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:%(class)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_DEFNAME, "fore:%(function)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_OPERATOR, "bold, size:%(size)d, face:%(face)s" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:%(identifier)s, face:%(face)s, size:%(size)d" % DOC_FACES)
    editor.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:%(commentblock)s, face:%(face)s, italic, size:%(size)d" % DOC_FACES)

def _ed_set_style_p(editor, searchKey=None):
    editor.SetLexer(stc.STC_LEX_PYTHON)
    editor.SetKeyWords(0, " ".join(keyword.kwlist) + " None True False ")

    editor.SetMargins(5, 5)
    editor.SetSTCCursor(2)
    editor.SetIndent(4)
    editor.SetTabIndents(True)
    editor.SetTabWidth(4)
    editor.SetUseTabs(False)

    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:%(default)s, face:%(face)s, size:%(size)d, back:%(background)s" % DOC_FACES_P)
    editor.StyleClearAll()
    editor.StyleSetSpec(stc.STC_STYLE_DEFAULT, "fore:%(default)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "fore:%(linenumber)s, back:%(marginback)s, face:%(face)s, size:%(size2)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "fore:%(default)s, face:%(face)s" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_DEFAULT, "fore:%(default)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:%(comment)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_NUMBER, "fore:%(number)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_STRING, "fore:%(string)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_CHARACTER, "fore:%(string)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_WORD, "fore:%(keyword)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_WORD2, "fore:%(keyword2)s, face:%(face)s, bold, size:%(size3)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_TRIPLE, "fore:%(triple)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:%(triple)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:%(class)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_DEFNAME, "fore:%(function)s, face:%(face)s, bold, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_OPERATOR, "bold, size:%(size)d, face:%(face)s" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:%(identifier)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)
    editor.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:%(commentblock)s, face:%(face)s, size:%(size)d" % DOC_FACES_P)

def complete_words_from_str(text, keyword):
    words = [keyword]
    keyword = keyword.lower()
    text_ori = text
    text = text.replace("`", " ").replace("'", " ").replace(".", " ").replace(", ", " ").replace('"', " ").replace("=", " ").replace("\n", " ").lower()
    found = text.find(keyword)
    while found > -1:
        start = text.rfind(" ", 0, found)
        end = text.find(" ", found)
        words.append(text_ori[start:end])
        found = text.find(keyword, found + 1)
    words = " ".join(words)
    return words

class ManualPanel(wx.Treebook):
    def __init__(self, parent):
        wx.Treebook.__init__(self, parent, -1, size=(600, 480), style=wx.BK_DEFAULT | wx.BORDER_SUNKEN)
        self.parent = parent
        self.searchKey = None
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
        #self.GetTreeCtrl().InvalidateBestSize()
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
        return # TreeBook has no more a GetTreeCtrl method. Don't know how to retrieve it...
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


modules_path = os.path.join(os.getcwd(), "doc-en", "source", "src", "modules")
def prepare_doc_tree():
    if os.path.isdir(modules_path):
        shutil.rmtree(modules_path)
    os.mkdir(modules_path)
    for cat in _MODULE_CATEGORIES:
        os.mkdir(os.path.join(modules_path, cat))

def create_modules_index():
    lines = _MODULES_TEXT.splitlines(True)
    lines.pop(0)
    with open(os.path.join(modules_path, "index.rst"), "w") as f:
        f.write(lines[0].replace('"', ''))
        f.write("=" * len(lines[0]))
        f.write("\n")
        for i in range(1, len(lines)):
            f.write(lines[i])
        f.write("\n.. toctree::\n   :maxdepth: 2\n\n")
        for cat in _MODULE_CATEGORIES:
            f.write("   %s/index\n" % cat)

def create_category_index(category, overview, modules):
    path = os.path.join(modules_path, category)
    lines = overview.splitlines(True)
    lines.pop(0)
    with open(os.path.join(path, "index.rst"), "w") as f:
        f.write(category + " : " + lines[0].replace('"', ''))
        f.write("=" * len(category + lines[0]))
        f.write("\n")
        for i in range(1, len(lines)):
            f.write(lines[i])
        f.write("\n.. toctree::\n   :maxdepth: 1\n\n")
        for mod in modules:
            f.write("   %s\n" % mod.split(".")[0])

def create_module_doc_page(module, text):
    root, name = os.path.split(module)
    root, category = os.path.split(root)
    name = name.split(".")[0]
    pname = name + ".rst"
    path = os.path.join(modules_path, category, pname)
    lines = text.splitlines(True)
    for i, line in enumerate(lines):
        if len(line) > 4:
            lines[i] = line[4:]
    with open(path, "w") as f:
        f.write(name + " : " + lines[0].replace('"', ''))
        f.write("=" * len(name + lines[0]))
        f.write("\n")
        tosub = 0
        for i in range(1, len(lines)):
            if tosub > 0:
                f.write("-" * tosub)
                f.write("\n")
            if lines[i].strip() in _DOC_KEYWORDS:
                tosub = len(lines[i])
            else:
                tosub = 0
            if "#" in lines[i] and ":" in lines[i]:
                line = lines[i].replace("# ", "**").replace(" :", "** :")
            else:
                line = lines[i]
            f.write(line)

class ManualPanel_modules(ManualPanel):
    def __init__(self, parent):
        ManualPanel.__init__(self, parent)
        self.root, self.directories, self.files = CeciliaLib.buildFileTree()
        self.parse()

    def parse(self):
        if BUILD_RST:
            prepare_doc_tree()
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
        wx.CallLater(100, self.AdjustSize)

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
                        text = text[newline + 1:second]
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
                if BUILD_RST:
                    create_modules_index()
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                panel.win.SetUseHorizontalScrollBar(False)
                panel.win.SetUseVerticalScrollBar(False)
                text = ""
                for cat in _MODULE_CATEGORIES:
                    l = _CATEGORY_OVERVIEW[cat].splitlines()[1].replace('"', '').strip()
                    text += "# %s\n    %s\n" % (cat, l)
                panel.win.SetText(_MODULES_TEXT + text)
            elif obj in _MODULE_CATEGORIES:
                if BUILD_RST:
                    create_category_index(obj, _CATEGORY_OVERVIEW[obj], self.files[obj])
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                panel.win.SetUseHorizontalScrollBar(False)
                panel.win.SetUseVerticalScrollBar(False)
                text = _CATEGORY_OVERVIEW[obj]
                for file in self.files[obj]:
                    text += "# %s\n" % file
                    with open(os.path.join(self.root, obj, file), "r") as f:
                        t = f.read()
                        first = t.find('"""')
                        if first != -1:
                            newline = t.find("\n", first)
                            second = t.find('\n', newline + 2)
                            text += t[newline + 1:second].replace('"', '')
                            text += "\n"
                panel.win.SetText(text)
            elif os.path.isfile(obj):
                with open(obj, "r") as f:
                    text = f.read()
                    first = text.find('"""')
                    if first != -1:
                        newline = text.find("\n", first)
                        second = text.find('"""', newline)
                        text = text[newline + 1:second]
                    else:
                        text = '"Module not documented..."'
                    if BUILD_RST:
                        create_module_doc_page(obj, text)
                obj = os.path.split(obj)[1]
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                panel.win.SetUseHorizontalScrollBar(False)
                panel.win.SetUseVerticalScrollBar(False)
                panel.win.SetText(text)
            else:
                var = eval(obj)
                if isinstance(var, str):
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                    panel.win.SetUseHorizontalScrollBar(False)
                    panel.win.SetUseVerticalScrollBar(False)
                    panel.win.SetText(var)
                else:
                    text = var.__doc__
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                    panel.win.SetUseHorizontalScrollBar(False)
                    panel.win.SetUseVerticalScrollBar(False)
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
                    self.sequence = self.sequence[0:self.seq_index + 1]
                    self.sequence.append(i)
                    self.seq_index = len(self.sequence) - 1
                    self.history_check()
                self.parent.setTitle(text)
                self.SetSelection(i)
                panel = self.GetPage(self.GetSelection())
                if not panel.isLoad:
                    panel.isLoad = True
                    panel.win = stc.StyledTextCtrl(panel, -1, size=panel.GetSize(), style=wx.BORDER_SUNKEN)
                    panel.win.SetUseHorizontalScrollBar(False)
                    panel.win.LoadFile(os.path.join(CeciliaLib.ensureNFD(DOC_PATH), word))
                    panel.win.SetMarginWidth(1, 0)
                    if self.searchKey is not None:
                        words = complete_words_from_str(panel.win.GetText(), self.searchKey)
                        _ed_set_style(panel.win, words)
                    else:
                        _ed_set_style(panel.win)
                    panel.win.SetSelectionEnd(0)

                    def OnPanelSize(evt, win=panel.win):
                        win.SetPosition((0, 0))
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

api_doc_path = os.path.join(os.getcwd(), "doc-en", "source", "src", "api")
def prepare_api_doc_tree():
    if os.path.isdir(api_doc_path):
        shutil.rmtree(api_doc_path)
    os.mkdir(api_doc_path)
    for cat in ["BaseModule", "Interface"]:
        os.mkdir(os.path.join(api_doc_path, cat))

def create_api_doc_index():
    lines = _INTRO_TEXT.splitlines(True)
    lines.pop(0)
    with open(os.path.join(api_doc_path, "index.rst"), "w") as f:
        f.write(lines[0].replace('"', ''))
        f.write("=" * len(lines[0]))
        f.write("\n")
        tosub = 0
        for i in range(1, len(lines)):
            if tosub > 0:
                f.write("-" * tosub)
                f.write("\n")
            if lines[i].startswith("#"):
                lines[i] = lines[i].replace("# ", "")
                tosub = len(lines[i])
            else:
                tosub = 0
            f.write(lines[i])
        f.write("\n.. toctree::\n   :maxdepth: 2\n\n")
        for cat in ["BaseModule", "Interface"]:
            f.write("   %s/index\n" % cat)

def create_base_module_index():
    lines = BaseModule_API.splitlines(True)
    lines.pop(0)
    with open(os.path.join(api_doc_path, "BaseModule", "index.rst"), "w") as f:
        f.write(lines[0].replace("_", " "))
        f.write("=" * len(lines[0]))
        f.write("\n")
        tosub = 0
        in_code_block = False
        for i in range(1, len(lines)):
            if in_code_block:
                if lines[i].startswith("###"):
                    in_code_block = False
                    lines[i] = "\n"
                else:
                    lines[i] = "    " + lines[i]
            else:
                if lines[i].startswith("###"):
                    lines[i] = ".. code::\n\n"
                    in_code_block = True
            if tosub > 0:
                f.write("-" * tosub)
                f.write("\n")
            if lines[i].startswith("#") and ":" not in lines[i]:
                lines[i] = lines[i].replace("# ", "")
                tosub = len(lines[i])
            elif lines[i].startswith("#") and ":" in lines[i]:
                lines[i] = lines[i].replace("# ", "**").replace(" :", "**")
            elif lines[i].strip() in _DOC_KEYWORDS and not in_code_block:
                tosub = len(lines[i])
            else:
                tosub = 0
            f.write(lines[i])

def create_interface_api_index():
    lines = Interface_API.splitlines(True)
    lines.pop(0)
    with open(os.path.join(api_doc_path, "Interface", "index.rst"), "w") as f:
        f.write(lines[0].replace("_", " "))
        f.write("=" * len(lines[0]))
        f.write("\n")
        for i in range(1, len(lines)):
            f.write(lines[i])

        f.write("\n.. toctree::\n   :maxdepth: 1\n\n")
        for word in _KEYWORDS_LIST:
            f.write("   %s\n" % word)
        f.write("   colours\n")
        f.write("   example1\n")
        f.write("   example2\n")

    lines = _COLOUR_TEXT.splitlines(True)
    lines.pop(0)
    lines2 = _COLOURS.splitlines(True)
    lines2.pop(0)
    with open(os.path.join(api_doc_path, "Interface", "colours.rst"), "w") as f:
        f.write(lines[0])
        f.write("=" * len(lines[0]))
        for i in range(1, len(lines)):
            f.write(lines[i])
        f.write("\n\n.. code::\n\n")
        for i in range(len(lines2)):
            f.write(lines2[i] + "\n")
    lines = _EXAMPLE_1.splitlines(True)
    lines.pop(0)
    with open(os.path.join(api_doc_path, "Interface", "example1.rst"), "w") as f:
        f.write(lines[0].replace("###", "").strip().lower().capitalize() + "\n")
        f.write("=" * len(lines[0]))
        f.write("\n\n.. code::\n\n")
        for i in range(1, len(lines)):
            f.write("    " + lines[i])
    lines = _EXAMPLE_2.splitlines(True)
    lines.pop(0)
    with open(os.path.join(api_doc_path, "Interface", "example2.rst"), "w") as f:
        f.write(lines[0].replace("###", "").strip().lower().capitalize() + "\n")
        f.write("=" * len(lines[0]))
        f.write("\n\n.. code::\n\n")
        for i in range(1, len(lines)):
            f.write("    " + lines[i])

def create_api_doc_page(obj, text):
    path = os.path.join(api_doc_path, "Interface", "%s.rst" % obj)
    lines = text.splitlines(True)
    lines.pop(0)
    for i, line in enumerate(lines):
        if len(line) > 4:
            lines[i] = line[4:]
    with open(path, "w") as f:
        f.write(obj + " : " + lines[0].replace('"', '').lower())
        f.write("=" * len(obj + lines[0]))
        f.write("\n")
        tosub = 0
        indent = 0
        incode = False
        prompt = False
        for i in range(1, len(lines)):
            if tosub > 0:
                f.write("-" * tosub)
                f.write("\n")
            if incode:
                f.write("\n.. code::\n")
                incode = False
            if ">>> " in lines[i]:
                if not prompt:
                    prompt = True
                    f.write("\n.. code::\n\n")
            else:
                prompt = False
            if lines[i].strip() in _DOC_KEYWORDS:
                tosub = len(lines[i])
                if lines[i].strip() == "Initline":
                    indent = 4
                    incode = True
                else:
                    indent = 0
            else:
                tosub = 0
            if "#" in lines[i] and ":" in lines[i]:
                line = lines[i].replace("# ", "**").replace(" :", "** :")
            elif indent > 0 and tosub == 0 or prompt:
                line = "    " + lines[i].replace(">>> ", "")
            else:
                line = lines[i]
            f.write(line)

class ManualPanel_api(ManualPanel):
    def __init__(self, parent):
        ManualPanel.__init__(self, parent)
        self.parse()

    def parse(self):
        if BUILD_RST:
            prepare_api_doc_tree()
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
        wx.CallLater(100, self.AdjustSize)

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
                if BUILD_RST:
                    create_api_doc_index()
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                panel.win.SetUseHorizontalScrollBar(False)
                panel.win.SetUseVerticalScrollBar(False)
                panel.win.SetText(_INTRO_TEXT)
            elif "Example" in obj:
                panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                panel.win.SetUseHorizontalScrollBar(False)
                panel.win.SetUseVerticalScrollBar(False)
                if "1" in obj:
                    panel.win.SetText(_EXAMPLE_1)
                elif "2" in obj:
                    panel.win.SetText(_EXAMPLE_2)
            else:
                var = eval(obj)
                if isinstance(var, str):
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                    panel.win.SetUseHorizontalScrollBar(False)
                    panel.win.SetUseVerticalScrollBar(False)
                    if "Interface_API" in var:
                        if BUILD_RST:
                            create_interface_api_index()
                        for word in _KEYWORDS_LIST:
                            lines = eval(word).__doc__.splitlines()
                            line = "%s : %s\n" % (word, lines[1].replace('"', '').strip())
                            var += line
                        var += _COLOUR_TEXT
                        var += _COLOURS
                    else:
                        if BUILD_RST:
                            create_base_module_index()
                    panel.win.SetText(var)
                else:
                    text = var.__doc__
                    if BUILD_RST:
                        create_api_doc_page(obj, text)
                    panel.win = stc.StyledTextCtrl(panel, -1, size=(600, 480), style=wx.BORDER_SUNKEN)
                    panel.win.SetUseHorizontalScrollBar(False)
                    panel.win.SetUseVerticalScrollBar(False)
                    panel.win.SetText(text.replace(">>> ", ""))

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
                    self.sequence = self.sequence[0:self.seq_index + 1]
                    self.sequence.append(i)
                    self.seq_index = len(self.sequence) - 1
                    self.history_check()
                self.parent.setTitle(text)
                self.SetSelection(i)
                panel = self.GetPage(self.GetSelection())
                if not panel.isLoad:
                    panel.isLoad = True
                    panel.win = stc.StyledTextCtrl(panel, -1, size=panel.GetSize(), style=wx.BORDER_SUNKEN)
                    panel.win.SetUseHorizontalScrollBar(False)
                    panel.win.LoadFile(os.path.join(CeciliaLib.ensureNFD(DOC_PATH), word))
                    panel.win.SetMarginWidth(1, 0)
                    if self.searchKey is not None:
                        words = complete_words_from_str(panel.win.GetText(), self.searchKey)
                        _ed_set_style(panel.win, words)
                    else:
                        if "Example" in word:
                            _ed_set_style_p(panel.win)
                        else:
                            _ed_set_style(panel.win)
                    panel.win.SetSelectionEnd(0)

                    def OnPanelSize(evt, win=panel.win):
                        win.SetPosition((0, 0))
                        win.SetSize(evt.GetSize())

                    panel.Bind(wx.EVT_SIZE, OnPanelSize)
                self.fromToolbar = False
                return

class ManualFrame(wx.Frame):
    def __init__(self, parent=None, id=-1, size=(950, 650), kind="api"):
        if kind == "api":
            title = 'API Documentation'
        else:
            title = 'Modules Documentation'
        wx.Frame.__init__(self, parent=parent, id=id, title=title, size=size)
        self.SetMinSize((600, 480))

        self.kind = kind
        gosearchID = 1000
        aTable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, 47, gosearchID)])
        self.SetAcceleratorTable(aTable)
        self.Bind(wx.EVT_MENU, self.setSearchFocus, id=gosearchID)

        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((24, 24))

        back_ico = CeciliaLib.getVar("ICON_DOC_PREVIOUS")
        forward_ico = CeciliaLib.getVar("ICON_DOC_NEXT")
        home_ico = CeciliaLib.getVar("ICON_DOC_UP")

        backTool = self.toolbar.AddTool(wx.ID_BACKWARD, "", back_ico, "Back")
        self.toolbar.EnableTool(wx.ID_BACKWARD, False)
        self.Bind(wx.EVT_MENU, self.onBack, backTool)

        self.toolbar.AddSeparator()

        forwardTool = self.toolbar.AddTool(wx.ID_FORWARD, "", forward_ico, "Forward")
        self.toolbar.EnableTool(wx.ID_FORWARD, False)
        self.Bind(wx.EVT_MENU, self.onForward, forwardTool)

        self.toolbar.AddSeparator()

        homeTool = self.toolbar.AddTool(wx.ID_HOME, "", home_ico, "Go Home")
        self.toolbar.EnableTool(wx.ID_HOME, True)
        self.Bind(wx.EVT_MENU, self.onHome, homeTool)

        self.toolbar.AddSeparator()

        self.searchTimer = None
        self.searchScope = "Page Names"
        self.searchMenu = wx.Menu()
        item = self.searchMenu.Append(-1, "Search Scope")
        item.Enable(False)
        for i, txt in enumerate(["Page Names", "Manual Pages"]):
            id = i + 10
            self.searchMenu.Append(id, txt)
            self.Bind(wx.EVT_MENU, self.onSearchScope, id=id)

        self.search = wx.SearchCtrl(self.toolbar, 200, size=(200, -1), style=wx.WANTS_CHARS | wx.TE_PROCESS_ENTER)
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
        return # TreeBook has no more a GetTreeCtrl method. Don't know how to retrieve it...
        self.doc_panel.GetTreeCtrl().SetFocus()

    def onSearch(self, evt):
        if self.searchTimer is not None:
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