#!/usr/bin/env python
# encoding: utf-8
"""
Copyright 2011 iACT, Universite de Montreal,
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

BaseModule_API = """
BaseModule_API

Here are the explanations about the processing class under every cecilia5 module.

# Declaration of the module's class

Every module must contain a class named 'Module', where the audio processing
will be developed. In order to work properly inside the environment, this
class must inherit from the `BaseModule` class, defined inside the Cecilia
source code. The BaseModule's internals create all links between the interface
and the module's processing. A Cecilia module must be declared like this:

###########################################################################
class Module(BaseModule):
    '''
    Module's documentation
    '''
    def __init__(self):
        BaseModule.__init__(self)
        ### Here comes the processing chain...
###########################################################################

The module file will be executed in an environment where both `BaseModule` and
`pyo` are already available. No need to import anything specific to define the
audio process of the module.

# Module's output

The last object of the processing chain (ie the one producing the output sound)
must be called 'self.out'. The audio server gets the sound from this variable
and sends it to the Post-Processing plugins and from there, to the soundcard.

Here is an example of a typical output variable, where 'self.snd' is the dry
sound and 'self.dsp' is the processed sound. 'self.drywet' is a mixing slider
and 'self.env' is the overall gain from a grapher's line:

###########################################################################
self.out = Interp(self.snd, self.dsp, self.drywet, mul=self.env)
###########################################################################

# Module's documentation

The class should provide a __doc__ string giving relevant information about
the processing implemented by the module. The user can show the documentation
by selecting 'Help Menu' ---> 'Show Module Info'. Here is an example:

###########################################################################
    '''
    "Convolution brickwall lowpass/highpass/bandpass/bandstop filter"

    Description

    Convolution filter with a user-defined length sinc kernel. This
    kind of filters are very CPU expensive but can give quite good
    stopband attenuation.

    Sliders

        # Cutoff Frequency :
            Cutoff frequency, in Hz, of the filter.
        # Bandwidth :
            Bandwith, in Hz, of the filter.
            Used only by bandpass and pnadstop filters.
        # Filter Order :
            Number of points of the filter kernel. A longer kernel means
            a sharper attenuation (and a higher CPU cost). This value is
            only available at initialization time.

    Graph Only

        # Overall Amplitude :
            The amplitude curve applied on the total duration of the performance

    Popups & Toggles

        # Filter Type :
            Type of the filter (lowpass, highpass, bandpass, bandstop)
        # Balance :
            Compression mode. Off, balanced with a fixed signal
            or balanced with the input source.
        # Polyphony Voices :
            Number of voices played simultaneously (polyphony),
            only available at initialization time
        # Polyphony Spread :
            Pitch variation between voices (chorus),
            only available at initialization time

    '''
###########################################################################

Public Attributes

These are the attributes, defined in the BaseModule class, available to the
user to help in the design of his custom modules.

# self.sr :
    Cecilia's current sampling rate.
# self.nchnls :
    Cecilia's current number of channels.
# self.totalTime :
    Cecilia's current duration.
# self.filepath :
    Path to the directory where is saved the current cecilia file.
# self.number_of_voices :
    Number of voices from the cpoly widget.
# self.polyphony_spread :
    List of transposition factors from the cpoly widget.
# self.polyphony_scaling :
    Amplitude value according to polyphony number of voices.

Public Methods

These are the methods, defined in the BaseModule class, available to the
user to help in the design of his custom modules.

# self.addFilein(name) :
    Creates a SndTable object from the name of a cfilein widget.
# self.addSampler(name, pitch, amp) :
    Creates a sampler/looper from the name of a csampler widget.
# self.getSamplerDur(name) :
    Returns the duration of the sound used by the sampler `name`.
# self.duplicate(seq, num) :
    Duplicates elements in a sequence according to the `num` parameter.
# self.setGlobalSeed(x) :
    Sets the Server's global seed used by objects from the random family.

Template

This template, saved in a file with the extension '.c5', created a basic
module where a sound can be load in a sampler for reading, with optional
polyphonic playback. A graph envelope modulates the amplitude of the sound
over the performance duration.

###########################################################################
class Module(BaseModule):
    '''
    Module's documentation
    '''
    def __init__(self):
        BaseModule.__init__(self)
        ### get the sound from a sampler/looper
        self.snd = self.addSampler('snd')
        ### mix the channels and apply the envelope from the graph
        self.out = Mix(self.snd, voices=self.nchnls, mul=self.env)

Interface = [
    csampler(name='snd'),
    cgraph(name='env', label='Amplitude', func=[(0,1),(1,1)], col='blue1'),
    cpoly()
]
###########################################################################

"""

Interface_API = """
Interface_API

The next functions describe every available widgets for building a Cecilia5 interface.

"""

def cfilein(name="filein", label="Audio", help=""):
    """
    "Creates a popup menu to load a soundfile in a table"

    Initline

    cfilein(name='filein', label='Audio', help='')

    Description

    This interactive menu allows the user to import a soundfile into the
    processing module. When the user chooses a sound using the interface,
    Cecilia will scan the whole folder for soundfiles. A submenu containing
    all soundfiles present in the folder will allow a quicker access to them
    later on.

    More than one cfilein can be defined in a module. They will appear under
    the input label in the left side panel of the main window, in the order
    defined.

    In the processing class, use the BaseModule's method `addFilein` to
    retrieve the SndTable filled with the selected sound.

        >>> BaseModule.addFilein(name)

    For a cfilein created with name='mysound', the table is retrieved
    using a call like this one:

        >>> self.table = self.addFilein('mysound')

    Parameters

        # name : str
            A string passed to the parameter `name` of the BaseModule.addFilein
            method. This method returns a SndTable object containing Cecilia's
            number of channels filled with the selected sound in the interface.
        # label : str
            Label shown in the interface.
        # help : str
            Help string shown in the widget's popup tooltip.

    """
    dic = {"type": "cfilein"}
    dic["name"] = name
    dic["label"] = label
    dic["help"] = help
    return dic

def csampler(name="sampler", label="Audio", help=""):
    """
    "Creates a popup menu to load a soundfile in a sampler"

    Initline

    csampler(name='sampler', label='Audio', help='')

    Description

    This menu allows the user to choose a soundfile for processing in the
    module. More than one csampler can be defined in a module. They will
    appear under the input label in the left side panel of the main window,
    in the order they have been defined. When the user chooses a sound using
    the interface, Cecilia will scan the whole folder for soundfiles. A
    submenu containing all soundfiles present in the folder will allow a
    quicker access to them later on. Loop points, pitch and amplitude
    parameters of the loaded soundfile can be controlled by the csampler
    window that drops when clicking the triangle just besides the name of
    the sound.

    A sampler returns an audio variable containing Cecilia's number of
    output channels regardless of the number of channels in the soundfile.
    A distribution algorithm is used to assign X number of channels to Y
    number of outputs.

    In the processing class, use the BaseModule's method `addSampler` to
    retrieve the audio variable containing all channels of the looped sound.

        >>> BaseModule.addSampler(name, pitch, amp)

    For a csampler created with name='mysound', the audio variable is
    retrieved using a call like this one:

        >>> self.snd = self.addSampler('mysound')

    Audio LFOs on pitch and amplitude of the looped sound can be passed
    directly to the addSampler method:

        >>> self.pitlf = Sine(freq=.1, mul=.25, add=1)
        >>> self.amplf = Sine(freq=.15, mul=.5, add=.5)
        >>> self.snd = self.addSampler('mysound', self.pitlf, self.amplf)

    Parameters

        # name : str
            A string passed to the parameter `name` of the BaseModule.addSampler
            method. This method returns a Mix object containing Cecilia's
            number of channels as audio streams from a Looper object
            controlled with the sampler window of the interface.
        # label : str
            Label shown in the interface.
        # help : str
            Help string shown in the sampler popup's tooltip.

    """
    dic = {"type": "csampler"}
    dic["name"] = name
    dic["label"] = label
    dic["help"] = help
    return dic

def cpoly(name="poly", label="Polyphony", min=1, max=10, init=1, help=""):
    """
    "Creates two popup menus used as polyphony manager"

    Initline

    cpoly(name='poly', label='Polyphony', min=1, max=10, init=1, help='')

    Description

    cpoly is a widget conceived to help manage the voice polyphony of a
    module. cpoly comes with a popup menu that allows the user to choose how
    many instances (voices) of a process will be simultaneously playing. It
    also provides another popup to choose the type of polyphony (phasing,
    chorus, out-of-tune or one of the provided chords).

    cpoly has two values that are passed to the processing module: the number
    of voices and the voice spread. The number of voices can be collected
    using `self.number_of_voices`. `self.polyphony_spread` gives access to
    the transposition factors defined by the type of polyphony.

    If a csampler is used, you don't need to take care of polyphony, it's
    automatically handled inside the csampler. Without a csampler, user can
    retrieve polyphony popups values with these builtin reserved
    variables :

        # self.number_of_voices : int
            Number of layers of polyphony
        # self.polyphony_spread : list of floats
            Transposition factors as a list of floats
        # self.polyphony_scaling : float
            An amplitude factor based on the number of voices

    Notes

    The cpoly interface object and its associated variables can be used in
    the dsp module any way one sees fit.

    No more than one `cpoly` can be declared in a module.

    Parameters

        # name : str
            Name of the widget.
        # label : str
            Label shown in the interface.
        # min : int
            Minimum value for the number of layers slider.
        # max : int
            Maximum value for the number of layers slider.
        # init : int
            Initial value for the number of layers slider.
        # help : str
            Help string shown in the cpoly tooltip.

    """
    dic = {"type": "cpoly"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["init"] = init
    dic["help"] = help
    return dic

def cgraph(name="graph", label="Envelope", min=0.0, max=1.0, rel="lin", table=False, size=8192,
            unit="x", curved=False, func=[(0, 0.), (.01, 1), (.99, 1), (1, 0.)], col="red"):
    """
    "Creates a graph only automated parameter or a shapeable envelope"

    Initline

    cgraph(name='graph', label='Envelope', min=0.0, max=1.0, rel='lin',
           table=False, size=8192, unit='x', curved=False,
           func=[(0, 0.), (.01, 1), (.99, 1), (1, 0.)], col='red')

    Description

    A graph line represents the evolution of a variable during a Cecilia
    performance. The value of the graph is passed to the module with a
    variable named `self.name`. The 'func' argument defines an initial
    break-point line shaped with time/value pairs (floats) as a list. Time
    values must be defined from 0 to 1 and are multiplied by the total_time
    of the process. When True, the 'table' argument writes the graph line in
    a PyoTableObject named with the variable `self.name`. The graph can then
    be used for any purpose in the module by recalling its variable. The
    `col` argument defines the color of the graph line using a color value.

    Parameters

        # name : str
            Name of the grapher line.
        # label : str
            Label shown in the grapher popup.
        # min : float
            Minimum value for the Y axis.
        # max : float
            Maximum value for the Y axis.
        # rel : str {'lin', 'log'}
            Y axis scaling.
        # table : boolean
            If True, a PyoTableObject will be created instead of a
            control variable.
        # size : int
            Size, in samples, of the PyoTableObject.
        # unit : str
            Unit symbol shown in the interface.
        # curved : boolean
            If True, a cosinus segments will be drawn between points.
            The curved mode can be switched by double-click on the curve
            in the grapher. Defaults to Flase
        # func : list of tuples
            Initial graph line in break-points (serie of time/value points).
            Times must be in increasing order between 0 and 1.
        # col : str
            Color of the widget.

    """
    dic = {"type": "cgraph"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["rel"] = rel
    dic["table"] = table
    dic["unit"] = unit
    dic["curved"] = curved
    dic["size"] = size
    dic["func"] = func
    dic["col"] = col
    return dic

def cslider(name="slider", label="Pitch", min=20.0, max=20000.0, init=1000.0, rel="lin", res="float",
            gliss=0.025, unit="x", up=False, func=None, midictl=None, half=False, col="red", help=""):
    """
    "Creates a slider, and its own graph line, for time-varying controls"

    Initline

    cslider(name='slider', label='Pitch', min=20.0, max=20000.0, init=1000.0,
            rel='lin', res='float', gliss=0.025, unit='x', up=False,
            func=None, midictl=None, half=False, col='red', help='')

    Description

    When created, the slider is stacked in the slider pane of the main Cecilia
    window in the order it is defined. The value of the slider is passed to
    the module with a variable named `self.name`. The `up` argument passes
    the value of the slider on mouse up if set to True or continuously if set
    to False. The `gliss` argument determines the duration of the portamento
    (in seconds) applied between values. The portamento is automatically set
    to 0 if `up` is True. The resolution of the slider can be set to int or
    float using the `res` argument. Slider color can be set using the `col`
    argument and a color value. However, sliders with `up` set to True are
    greyed out and the `col` argument is ignored.

    If `up` is set to True, the cslider will not create an audio rate signal,
    but will call a method named `widget_name` + '_up'. This method must be
    defined in the class `Module`. For a cslider with the name 'grains', the
    method should be declared like this:

    >>> def grains_up(self, value):

    Every time a slider is defined with `up` set to False, a corresponding
    graph line is automatically defined for the grapher in the Cecilia
    interface. The recording and playback of an automated slider is linked
    to its graph line.

    Parameters

        # name : str
            Name of the slider.
        # label : str
            Label shown in the slider label and the grapher popup.
        # min : float
            Minimum value of the slider.
        # max : float
            Maximum value of the slider.
        # init : float
            Slider's initial value.
        # rel : str {'lin', 'log'}
            Slider scaling. Defaults to 'lin'.
        # res : str {'int', 'float'}
            Slider resolution. Defaults to 'float'
        # gliss : float
            Portamento between values in seconds. Defaults to 0.025.
        # unit : str
            Unit symbol shown in the interface.
        # up : boolean
            Value passed on mouse up if True. Defaults to False.
        # func : list of tuples
            Initial automation in break-points format (serie of time/value
            points). Times must be in increasing order between 0 and 1.
        # midictl : int
            Automatically map a midi controller to this slider.
            Defaults to None.
        # half : boolean
            Determines if the slider is full-width or half-width. Set to True
            to get half-width slider. Defaults to False.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the cslider tooltip.

    """
    dic = {"type": "cslider"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["init"] = init
    dic["rel"] = rel
    dic["res"] = res
    dic["func"] = func
    dic["gliss"] = gliss
    dic["unit"] = unit
    dic["up"] = up
    dic["midictl"] = midictl
    dic["half"] = half
    dic["col"] = col
    dic["help"] = help
    return dic

def crange(name="range", label="Pitch", min=20.0, max=20000.0, init=[500.0, 2000.0], rel="log",
           res="float", gliss=0.025, unit="x", up=False, func=None, midictl=None, col="red", help=""):
    """
    "Two-sided slider, with its own graph lines, for time-varying controls"

    Initline

    crange(name='range', label='Pitch', min=20.0, max=20000.0,
           init=[500.0, 2000.0], rel='log', res='float', gliss=0.025,
           unit='x', up=False, func=None, midictl=None, col='red', help='')

    Description

    This function creates a two-sided slider used to control a minimum and
    a maximum range at the sime time. When created, the range slider is
    stacked in the slider pane of the main Cecilia window in the order it
    is defined. The values of the range slider are passed to the module
    with a variable named `self.name`. The range minimum is collected using
    `self.name[0]` and the range maximum is collected using `self.name[1]`.
    The `up` argument passes the values of the range on mouse up if set to
    True or continuously if set to False. The `gliss` argument determines
    the duration of the portamento (in sec) applied on a new value. The
    resolution of the range slider can be set to 'int' or 'float' using the
    `res` argument. Slider color can be set using the `col` argument and a
    color value. However, sliders with `up` set to True are greyed out and
    the `col` argument is ignored.

    Every time a range slider is defined, two graph lines are automatically
    defined for the grapher in the Cecilia interface. One is linked to the
    minimum value of the range, the other one to the maximum value of the
    range. The recording and playback of an automated slider is linked to its
    graph line.

    Notes

    In order to quickly select the minimum value (and graph line), the user
    can click on the left side of the crange label, and on the right side of
    the label to select the maximum value (and graph line).

    Parameters

        # name : str
            Name of the range slider.
        # label : str
            Label shown in the crange label and the grapher popup.
        # min : float
            Minimum value of the range slider.
        # max : float
            Maximum value of the range slider.
        # init : list of float
            Range slider minimum and maximum initial values.
        # rel : str {'lin', 'log'}
            Range slider scaling. Defaults to 'lin'.
        # res : str {'int', 'float'}
            Range slider resolution. Defaults to 'float'
        # gliss : float
            Portamento between values in seconds. Defaults to 0.025.
        # unit : str
            Unit symbol shown in the interface.
        # up : boolean
            Value passed on mouse up if True. Defaults to False.
        # func : list of list of tuples
            Initial automation in break-points format (serie of time/value
            points). Times must be in increasing order between 0 and 1.
            The list must contain two lists of points, one for the minimum
            value and one for the maximum value.
        # midictl : list of int
            Automatically map two midi controllers to this range slider.
            Defaults to None.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the crange tooltip.

    """
    dic = {"type": "crange"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["init"] = init
    dic["rel"] = rel
    dic["res"] = res
    if func is None:
        dic["func"] = [None, None]
    else:
        dic["func"] = func
    dic["gliss"] = gliss
    dic["unit"] = unit
    dic["up"] = up
    dic["midictl"] = midictl
    dic["half"] = False
    dic["col"] = col
    dic["help"] = help
    return dic

def csplitter(name="splitter", label="Pitch", min=20.0, max=20000.0, init=[500.0, 2000.0, 5000.0],
              rel="log", res="float", gliss=0.025, unit="x", up=False, num_knobs=3, col="red", help=""):
    """
    "Creates a multi-knobs slider used to split the spectrum in sub-regions"

    Initline

    csplitter(name='splitter', label='Pitch', min=20.0, max=20000.0,
              init=[500.0, 2000.0, 5000.0], rel='log', res='float',
              gliss=0.025, unit='x', up=False, num_knobs=3, col='red', help='')

    Description

    When created, the splitter is stacked in the slider pane of the main
    Cecilia window in the order it is defined. The values of the splitter
    slider are passed to the module with a variable named `self.name`. The
    knob values are collected using `self.name[0]` to `self.name[num-knobs-1]`.
    The `up` argument passes the values of the splitter on mouse up if set to
    True or continuously if set to False. The `gliss` argument determines the
    duration of the portamento (in seconds) applied between values. The
    resolution of the splitter slider can be set to int or float using the
    `res` argument. The slider color can be set using the `col` argument and
    a color value. However, sliders with `up` set to True are greyed out and
    the `col` argument is ignored.

    The csplitter is designed to be used with the FourBand() object in
    order to allow multi-band processing. Although the FourBand() parameters
    can be changed at audio rate, it is not recommended. This filter is CPU
    intensive and can have erratic behavior when boundaries are changed too
    quickly.

    Parameters

        # name : str
            Name of the splitter slider.
        # label : str
            Label shown in the csplitter label.
        # min : float
            Minimum value of the splitter slider.
        # max : float
            Maximum value of the splitter slider.
        # init : list of float
            Splitter knobs initial values. List must be of length `num_knobs`.
            Defaults to [500.0, 2000.0, 5000.0].
        # rel : str {'lin', 'log'}
            Splitter slider scaling. Defaults to 'lin'.
        # res : str {'int', 'float'}
            Splitter slider resolution. Defaults to 'float'
        # gliss : float
            Portamento between values in seconds. Defaults to 0.025.
        # unit : str
            Unit symbol shown in the interface.
        # up : boolean
            Value passed on mouse up if True. Defaults to False.
        # num_knobs : int
            Number of junction knobs. Defaults to 3.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the csplitter tooltip.

    """
    dic = {"type": "csplitter"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["init"] = init
    dic["rel"] = rel
    dic["res"] = res
    dic["gliss"] = gliss
    dic["unit"] = unit
    dic["up"] = up
    dic["num_knobs"] = num_knobs
    dic["midictl"] = None
    dic["half"] = False
    dic["col"] = col
    dic["help"] = help
    return dic

def ctoggle(name="toggle", label="Start/Stop", init=True, rate="k", stack=False, col="red", help=""):
    """
    "Creates a two-states button"

    Initline

    ctoggle(name='toggle', label='Start/Stop', init=True, rate='k',
            stack=False, col='red', help='')

    Description

    A toggle button is a two-states switch that can be used to start and stop
    processes.

    If `rate` argument is set to 'i', a built-in reserved variable is created
    at initialization time. The variable's name is constructed like this :

        >>> self.widget_name + '_value'

    If `name` is set to 'foo', the variable's name will be:

        >>> self.foo_value

    If `rate` argument is set to 'k', a module method using one argument
    must be defined with the name `name`. If `name` is set to 'foo', the
    function should be defined like this :

        >>> def foo(self, value):

    value is an integer (0 or 1).

    Parameters

        # name : str
            Name of the widget used to defined the function or the
            reserved variable.
        # label : str
            Label shown in the interface.
        # init : int
            Initial state of the toggle.
        # rate : str {'k', 'i'}
            Indicates if the toggle is handled at initialization time only
            ('i') with a reserved variable or with a function ('k') that can
            be called at any time during playback.
        # stack : boolean
            If True, the toggle will be added on the same row as the last
            toogle with stack=True and a label not empty. Defaults to False.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the toggle tooltip.

    """
    dic = {"type": "ctoggle"}
    dic["name"] = name
    dic["label"] = label
    dic["init"] = init
    dic["rate"] = rate
    dic['stack'] = stack
    dic["col"] = col
    dic["help"] = help
    return dic

def cpopup(name="popup", label="Chooser", value=["1", "2", "3", "4"],
           init="1", rate="k", col="red", help=""):
    """
    "Creates a popup menu offering a limited set of choices"

    Initline

    cpopup(name='popup', label='Chooser', value=['1', '2', '3', '4'],
               init='1', rate='k', col='red', help='')

    Description

    A popup menu offers a limited set choices that are available to modify
    the state of the current module.

    If `rate` argument is set to 'i', two built-in reserved variables are
    created at initialization time. The variables' names are constructed
    like this :

        >>> self.widget_name + '_index' for the selected position in the popup.
        >>> self.widget_name + '_value' for the selected string in the popup.

    If `name` is set to 'foo', the variables names will be:

        >>> self.foo_index (this variable is an integer)
        >>> self.foo_value (this variable is a string)

    If `rate` argument is set to 'k', a module method using two arguments
    must be defined with the name `name`. If `name` is set to 'foo', the
    function should be defined like this :

        >>> def foo(self, index, value):
        >>>     index -> int
        >>>     value -> str

    Parameters

        # name : str
            Name of the widget.
            Used to defined the function or the reserved variables.
        # label : str
            Label shown in the interface.
        # value : list of strings
            An array of strings with which to initialize the popup.
        # init : int
            Initial state of the popup.
        # rate : str {'k', 'i'}
            Indicates if the popup is handled at initialization time only
            ('i') with reserved variables or with a function ('k') that can
            be called at any time during playback.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the popup tooltip.

    """
    dic = {"type": "cpopup"}
    dic["name"] = name
    dic["label"] = label
    dic["value"] = value
    dic["init"] = init
    dic["rate"] = rate
    dic["col"] = col
    dic["help"] = help
    return dic

def cbutton(name="button", label="Trigger", col="red", help=""):
    """
    "Creates a button that can be used as an event trigger"

    Initline

    cbutton(name='button', label='Trigger', col='red', help='')

    Description

    A button has no state, it only sends a trigger when it is clicked.

    When the button is clicked, a function is called with the current
    state of the mouse (down or up) as argument.

    If `name` is set to 'foo', the function should be defined like this :

        >>> def foo(self, value):

    value is True on mouse pressed and False on mouse released.

    Parameters

        # name : str
            Name of the widget. Used to defined the function.
        # label : str
            Label shown in the interface.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the button tooltip.

    """
    dic = {"type": "cbutton"}
    dic["name"] = name
    dic["label"] = label
    dic["col"] = col
    dic["help"] = help
    return dic

def cgen(name="gen", label="Wave shape", init=[1,0,.3,0,.2,0,.143,0,.111],
         rate="k", popup=None, col="red", help=""):
    """
    "Creates a list entry useful to generate list of arbitrary values"

    Initline

    cgen(name='gen', label='Wave shape', init=[1,0,.3,0,.2,0,.143,0,.111],
             rate='k', popup=None, col='red', help='')

    Description

    Widget that can be used to create a list of floating-point values. A
    left click on the widget will open a floating window to enter the desired
    values. Values can be separated by commas or by spaces.

    If `rate` argument is set to 'i', a built-in reserved variable is created
    at initialization time. The variable name is constructed like this :

        >>> self.widget_name + '_value' for retrieving a list of floats.

    If `name` is set to 'foo', the variable name will be:

        >>> self.foo_value (this variable is a list of floats)

    If `rate` argument is set to 'k', a module method using one argument
    must be defined with the name `name`. If `name` is set to 'foo', the
    function should be defined like this :

        >>> def foo(self, value):
        >>>     value -> list of strings

    Parameters

        # name : str
            Name of the widget.
            Used to defined the function or the reserved variable.
        # label : str
            Label shown in the interface.
        # init : int
            An array of number, separated with commas, with which to
            initialize the widget.
        # rate : str {'k', 'i'}
            Indicates if the widget is handled at initialization time only
            ('i') with a reserved variable or with a function ('k') that can
            be called at any time during playback.
        # popup : tuple (str, int) -> (popup's name, index)
            If a tuple is specified, and cgen is modified, the popup will
            be automatically set to the given index.
        # col : str
            Color of the widget.
        # help : str
            Help string shown in the widget's tooltip.

    """
    dic = {"type": "cgen"}
    dic["name"] = name
    dic["label"] = label
    dic["init"] = init
    dic["rate"] = rate
    dic["popup"] = popup
    dic["col"] = col
    dic["help"] = help
    return dic