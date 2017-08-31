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

To download the latest version of Cecilia5, go to 
`the official web site! <http://ajaxsoundstudio.com/software/cecilia/>`_

User documentation
------------------

To consult the user online documentation, go to 
`ajaxsoundstudio.com <http://ajaxsoundstudio.com/cecilia5doc/index.html>`_.

Requirements
------------

**Minimum versions (for running Cecilia5 from sources):**

* `Python 3.5 <https://www.python.org/downloads/release/python-353/>`_
  `Python 3.6 <https://www.python.org/downloads/release/python-362/>`_ is prefered.
The programming language used to code the application.

* `WxPython 3.0.3 (Phoenix) <https://github.com/wxWidgets/Phoenix>`_
The toolkit used to create the graphical interface. Use the most recent
`snapshot-build <https://wxpython.org/Phoenix/snapshot-builds/>`_.

* `pyo <http://ajaxsoundstudio.com/software/pyo/>`_
The audio engine which gives his power to Cecilia. It should be
compiled from the latest `sources <https://github.com/belangeo/pyo>`_.

* `numpy <https://pypi.python.org/pypi/numpy>`_
Array processing module for numbers. Used to accelerate the grapher display.
Install the last stable version.

Screenshot
----------

.. image:: doc-en/source/images/snapshot.png
     :width: 100%

