#!/usr/bin/env python
# encoding: utf-8
def cfilein(name="filein", label="Audio", help="text for tooltip"):
    """
    Parameters:

        name : str
            A string passed to the parameter `name` of a method BaseModule.addFilein.
            This method returns a SndTable object containing Cecilia's number of channels
            filled with the selected sound from the interface.
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
    BaseModule.addSampler(name, user_pitch, user_amp)

    Parameters:

        name : str
            A string passed to the parameter `name` of a method BaseModule.addSampler.
            This method returns a Mix object containing Cecilia's number of channels
            audio streams from a Looper object controlled with the sampler frame in 
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
            Help string shown in the sampler popup's tooltip.

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
            Help string shown in the sampler popup's tooltip.

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
    dic = {"type": "cbutton"}
    dic["name"] = name
    dic["label"] = label
    dic["col"] = col
    dic["help"] = help
    return dic

def cgen(name="gen", label="Wave shape", init=[1,0,.3,0,.2,0,.143,0,.111], rate="k", col="red", help="text for tooltip"):                                
    dic = {"type": "cgen"}
    dic["name"] = name
    dic["label"] = label
    dic["init"] = init
    dic["rate"] = rate
    dic["col"] = col
    dic["help"] = help
    return dic

# default interface
DEFAULT_INTERFACE = [csampler(name="snd")]
