# Cecilia5 #

![Cecilia logo](http://github.com/belangeo/cecilia5/tree/master/doc-en/source/images/Cecilia5_96.png)

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
[the official web site!](http://ajaxsoundstudio.com/software/cecilia/)

# Requirements #

**Minimum versions (for running Cecilia5 from sources):**

* [Python 3.5](https://www.python.org/downloads/release/python-353/)

    - The programming language used to code the application.

* [WxPython 3.0.3 (Phoenix)](https://github.com/wxWidgets/Phoenix)

    - The toolkit used to create the graphical interface. Use the
    most recent [snapshot-build](https://wxpython.org/Phoenix/snapshot-builds/).

* [pyo](http://ajaxsoundstudio.com/software/pyo/)

    - The audio engine which gives his power to Cecilia. It should be 
    compiled from the latest [sources](https://github.com/belangeo/pyo).

* [numpy](https://pypi.python.org/pypi/numpy)

    - Array processing module for numbers. Used to accelerate the grapher display.
    Install the last stable version.
