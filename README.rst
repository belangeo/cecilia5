=======================================
Cecilia5 - the audio processing toolbox
=======================================

.. image:: doc-en/source/images/Cecilia_splash.png
     :align: center

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

Official web site
-----------------

To download the latest version of Cecilia5 binary app, go to 
`the official web site! <http://ajaxsoundstudio.com/software/cecilia/>`_

User documentation
------------------

To consult the user online documentation, go to 
`ajaxsoundstudio.com <http://ajaxsoundstudio.com/cecilia5doc/index.html>`_.

Requirements
------------

**If, for whatever reason, you can't use the binary app, here is what you need to install for running Cecilia5 from sources:**

* `Python 3.6 <https://www.python.org/downloads/release/python-368/>`_ or 
  `Python 3.7 <https://www.python.org/downloads/release/python-379/>`_ (preferred) or
  `Python 3.8 <https://www.python.org/downloads/release/python-385/>`_.
The programming language used to code the application.

* `WxPython 4.1.0 (Phoenix) <https://wxpython.org/pages/downloads/>`_
The toolkit used to create the graphical interface. (install with `pip install wxPython`)

* `pyo 1.0.3 <http://ajaxsoundstudio.com/software/pyo/>`_
The audio engine which gives his power to Cecilia. (install with `pip install pyo`)

* `numpy <https://pypi.python.org/pypi/numpy>`_
Array processing module for numbers. Used to accelerate the grapher display.
Install the last stable version.

Screenshot
----------

.. image:: doc-en/source/images/snapshot.png
     :width: 100%

