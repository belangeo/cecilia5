#!/usr/bin/env python
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

def cfilein(name="filein", label="Audio", help="text for tooltip"):
    """
    Description:
    
    This interactive menu allows the user to import a soundfile into the processing
    module. When a file is chosen using this widget, Cecilia will scan the whole 
    folder and create a dropdown menu with all the soundfiles within this folder to 
    give a quick access to them.

    Many cfileins can be defined in an interface. They will appear under the input 
    label in the left side panel of the main window in the order defined. 

    In the processing class, you use the BaseModule's method `addFilein` to retrieve 
    the SndTable filled with the selected sound.
    
        BaseModule.addFilein(name)
    
    For a cfilein created with name="mysound", the table should be retrieve with a 
    call like this one:
    
        self.table = self.addFilein("mysound")

    Parameters:

        name : str
            A string passed to the parameter `name` of a method BaseModule.addFilein.
            This method returns a SndTable object containing Cecilia's number of 
            channels filled with the selected sound from the interface.
        label : str
            Label shown in the interface.
        help : str
            Help string shown in the filein popup's tooltip.

    """
    dic = {"type": "cfilein"}
    dic["name"] = name
    dic["label"] = label
    dic["help"] = help
    return dic

def csampler(name="sampler", label="Audio", help="text for tooltip"):
    """
    Description:
    
    This menu allows the user to choose a soundfile for processing in the module. Many 
    csamplers can be defined in an interface. They will appear under the input label 
    in the left side panel of the main window in the order they have been defined. When 
    you choose a sound using this interface, Cecilia will scan the whole folder for 
    soundfiles. A submenu containing all soundfiles present in the folder will allow a 
    quick access to them. Looping, pitch and amplitude parameters of the loaded soundfile 
    can be controlled by a csampler window which opens when toggling the small drop down 
    triangle just besides the name of the sound.
    
    A sampler returns an audio variable containing Cecilia's number of output channels 
    aregardless of the number of channels in the soundfile. A distribution algorithm is 
    used to assign X number of channels to Y number of outputs.
    
    In the processing class, you use the BaseModule's method `addSampler` to retrieve 
    the audio variable containing all channels of the looped sound.

        BaseModule.addSampler(name, user_pitch, user_amp)

    For a csampler created with name="mysound", the audio variable should be retrieve 
    with a call like this one:
    
        self.snd = self.addSampler("mysound")
  
    Audio LFOs on pitch and amplitude of the looped sound can be passed directly to the
    addSampler method:
    
        self.pitlf = Sine(freq=.1, mul=.25, add=1)
        self.amplf = Sine(freq=.15, mul=.5, add=.5)
        self.snd = self.addSampler("mysound", self.pitlf, self.amplf)
            
    Parameters:

        name : str
            A string passed to the parameter `name` of a method BaseModule.addSampler.
            This method returns a Mix object containing Cecilia's number of channels
            audio streams from a Looper object controlled with the sampler window of 
            the interface.
        label : str
            Label shown in the interface.
        help : str
            Help string shown in the sampler popup's tooltip.

    """
    dic = {"type": "csampler"}
    dic["name"] = name
    dic["label"] = label
    dic["help"] = help
    return dic

def cpoly(name="poly", label="Polyphony", min=1, max=10, init=1, help="text for tooltip"):
    """
    Automatically handled inside the CeciliaSampler.
    
    Without a CeciliaSampler, user can retrieve polyphony popup and slider values 
    with these builtin reserved variables :
        
        self.number_of_voices : int. Number of layers of polyphony.
        self.polyphony_spread : float. Amplitude that can be used for pitch deviation.
    
    No more than one `cpoly` can be declared by module.

    Parameters:

        name : str
            Name of the widget.
        label : str
            Label shown in the interface.
        min : int
            Minimum value for the number of layers slider.
        max : int
            Maximum value for the number of layers slider.
        init : int
            Initial value for the number of layers slider.
        help : str
            Help string shown in the cpoly's tooltip.

    """
    dic = {"type": "cpoly"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["init"] = init
    dic["help"] = help
    return dic

def cgraph(name="graph", label="Envelope", min=0.0, max=1.0, rel="lin", table=False, unit="x", 
           size=8192, func=[(0, 0.), (.01, 1), (.99, 1), (1, 0.)], col="red", help="text for tooltip"):
    dic = {"type": "cgraph"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["rel"] = rel
    dic["table"] = table
    dic["unit"] = unit
    dic["size"] = size
    dic["func"] = func
    dic["col"] = col
    dic["help"] = help
    return dic
    
def cslider(name="slider", label="Pitch", min=20.0, max=20000.0, init=1000.0, rel="lin", res="float", 
            gliss=0.025, unit="x", up=False, func=None, midictl=None, col="red", help="text for tooltip"):
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
    dic["col"] = col
    dic["help"] = help
    return dic

def crange(name="range", label="Pitch", min=20.0, max=20000.0, init=[500.0, 2000.0], rel="log", 
           res="float", gliss=0.025, unit="x", up=False, func=[None, None], midictl=None, col="red", help="text for tooltip"):
    dic = {"type": "crange"}
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
    dic["col"] = col
    dic["help"] = help
    return dic

def ctoggle(name="toggle", label="Start/Stop", init=True, rate="k", col="red", help="text for tooltip"):                                
    """
    If `rate` argument is set to "i", a builtin reserved variable is created at initialization time.
    The variable's name is construct like this :
        
        self.widget_name + "_value"
        
    If `name` is set to "foo", the variable's name will be:
    
        self.foo_value

    If `rate` argument is set to "k", a module's method, taking one argument, must be defined with the
    name `name`. If `name` is set to "foo", the function should be defined like this :
    
        def foo(self, value):
            
    value is an integer taking 0 or 1.
    
    Parameters:

        name : str
            Name of the widget. Used to defined the function or the reserved variable.
        label : str
            Label shown in the interface.
        init : int
            Initial state of the toggle.
        rate : str {"k", "i"}
            Indicates if the toggle is handled at initialization time only ("i") with a reserved variable 
            or with a function ("k") that can be called at any time during the playback.
        col : str
            Colour of the widget.
        help : str
            Help string shown in the toggle's tooltip.

    """
    dic = {"type": "ctoggle"}
    dic["name"] = name
    dic["label"] = label
    dic["init"] = init
    dic["rate"] = rate
    dic["col"] = col
    dic["help"] = help
    return dic

def cpopup(name="popup", label="Chooser", value=["1", "2", "3", "4"],
           init="1", rate="k", col="red", help="text for tooltip"):                                
    """
    If `rate` argument is set to "i", two builtin reserved variables is created at initialization time.
    The variable's names are construct like this :

        self.widget_name + "_index" for the selected position in the popup.
        self.widget_name + "_value" for the selected string in the popup.

    If `name` is set to "foo", the variable's name will be:
    
        self.foo_index (this variable is an integer)
        self.foo_value (this variable is a string)

    If `rate` argument is set to "k", a module's method, taking two arguments, must be defined with the
    name `name`. If `name` is set to "foo", the function should be defined like this :
    
        def foo(self, index, value):
            index -> int
            value -> str

    Parameters:

        name : str
            Name of the widget. Used to defined the function or the reserved variables.
        label : str
            Label shown in the interface.
        value : list of strings
            An array of strings with which to initialise the popup.
        init : int
            Initial state of the popup.
        rate : str {"k", "i"}
            Indicates if the popup is handled at initialization time only ("i") with reserved variables 
            or with a function ("k") that can be called at any time during the playback.
        col : str
            Colour of the widget.
        help : str
            Help string shown in the popup's tooltip.

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

def cbutton(name="button", label="Trigger", col="red", help="text for tooltip"):                                
    """
    When the button is clicked, a function is called with the current state of the button in argument.
    
    If `name` is set to "foo", the function should be defined like this :
    
        def foo(self, value):
            
    value is True on mouse pressed and False on mouse released.
    
    Parameters:

        name : str
            Name of the widget. Used to defined the function.
        label : str
            Label shown in the interface.
        col : str
            Colour of the widget.
        help : str
            Help string shown in the button's tooltip.

    """
    dic = {"type": "cbutton"}
    dic["name"] = name
    dic["label"] = label
    dic["col"] = col
    dic["help"] = help
    return dic

def cgen(name="gen", label="Wave shape", init=[1,0,.3,0,.2,0,.143,0,.111], rate="k", popup=None, col="red", help="text for tooltip"):
    """
    Widget used to create a list of floating-point values.
    
    If `rate` argument is set to "i", a builtin reserved variable is created at initialization time.
    The variable's name are construct like this :

        self.widget_name + "_value" for retrieving a list of floats.

    If `name` is set to "foo", the variable's name will be:
    
        self.foo_value (this variable is a list of floats)

    If `rate` argument is set to "k", a module's method, taking one argument, must be defined with the
    name `name`. If `name` is set to "foo", the function should be defined like this :
    
        def foo(self, value):
            value -> list of strings

    Parameters:

        name : str
            Name of the widget. Used to defined the function or the reserved variable.
        label : str
            Label shown in the interface.
        init : int
            An array of number, separated with commas, with which to initialise the widget.
        rate : str {"k", "i"}
            Indicates if the widget is handled at initialization time only ("i") with a reserved 
            variable or with a function ("k") that can be called at any time during the playback.
        popup : tuple (str, int) -> (popup's name, index)
            If a tuple is specified, when cgen is modified, the popup will be automatically set to
            the given index.
        col : str
            Colour of the widget.
        help : str
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

# default interface
DEFAULT_INTERFACE = [csampler(name="snd")]
