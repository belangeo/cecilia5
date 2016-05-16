# Cecilia5 #

Cecilia is an audio signal processing environment. Cecilia lets you create 
your own GUI (grapher, sliders, toggles, popup menus) using a simple syntax. 
Cecilia comes with many original builtin modules for sound effects and synthesis.

Previously written in tcl/tk, Cecilia (version 4, named Cecilia4) was entirely 
rewritten in Python/wxPython and uses the Csound API for communicating between 
the interface and the audio engine. At this time, version 4.2 is the last 
release of this branch.

Cecilia5 now uses the pyo audio engine created for the Python programming 
language. pyo allows a much more powerfull integration of the audio engine to 
the graphical interface. Since it's a standard python module, there is no need 
to use an API to communicate with the interface.

# Official web site #

To download the latest version of Cecilia5, go to 
[the official web site](http://ajaxsoundstudio.com/software/cecilia/)

# Requirements #

**Minimum versions (for running Cecilia5 from sources):**

Python: 2.6 or 2.7

wxPython: 3.0.0.0

pyo: 0.7.5

numpy: 1.6 to 1.8 (not 1.9)
