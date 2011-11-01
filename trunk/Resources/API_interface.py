#!/usr/bin/env python
# encoding: utf-8
def cfilein(name="filein", label="Audio", help="text for tooltip"):
    """
    Doc...
    """
    dic = {"type": "cfilein"}
    dic["name"] = name
    dic["label"] = label
    dic["help"] = help
    return dic

def csampler(name="sampler", label="Audio", help="text for tooltip"):
    dic = {"type": "csampler"}
    dic["name"] = name
    dic["label"] = label
    dic["help"] = help
    return dic

def cpoly(name="poly", label="Polyphony", min=1, max=10, init=1, col="red", 
          help="text for tooltip"):
    dic = {"type": "cpoly"}
    dic["name"] = name
    dic["label"] = label
    dic["min"] = min
    dic["max"] = max
    dic["init"] = init
    dic["col"] = col
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

def ctoggle(name="toggle", label="Start/Stop", init=True, col="red", help="text for tooltip"):                                
    dic = {"type": "ctoggle"}
    dic["name"] = name
    dic["label"] = label
    dic["init"] = init
    dic["col"] = col
    dic["help"] = help
    return dic

def cpopup(name="popup", label="Chooser", value=["1", "2", "3", "4"], 
           init="1", col="red", help="text for tooltip"):                                
    dic = {"type": "cpopup"}
    dic["name"] = name
    dic["label"] = label
    dic["value"] = value
    dic["init"] = init
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

def cgen(name="gen", label="Wave shape", init=[1,0,.3,0,.2,0,.143,0,.111], col="red", help="text for tooltip"):                                
    dic = {"type": "cgen"}
    dic["name"] = name
    dic["label"] = label
    dic["init"] = init
    dic["col"] = col
    dic["help"] = help
    return dic

# default interface
DEFAULT_INTERFACE = [csampler(name="snd")]
