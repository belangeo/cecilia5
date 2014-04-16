Installation - Requirements
============================

Cecilia5 is compatible with the following systems:

- Mac OS X (from 10.5 to 10.9) 
- Windows (XP, Vista, 7 or 8)
- Linux (at least Debian-based distros but should work with other linux flavours)
    

Installing Cecilia5 on Windows or OSX
---------------------------------------

Windows and OSX users can download self-contained binaries of the latest version of 
Cecilia5 `here <http://ajaxsoundstudio.com/software/cecilia/>`_.

Running Cecilia5 from the lastest sources
-------------------------------------------

Before running Cecilia5 from the latest sources, 
please check if all these elements are installed on your computer:

- `Python 2.6 <https://www.python.org/download/releases/2.6.6>`_ or `Python 2.7 <https://www.python.org/download/releases/2.7.6>`_. 
- `Pyo 0.6.9 <http://ajaxsoundstudio.com/software/pyo/>`_ (or compiled with latest `sources <http://code.google.com/p/pyo>`_).
- `Numpy 1.6.0 or higher <http://sourceforge.net/projects/numpy/files/NumPy/>`_.
- `WxPython 2.8.12.1 <http://sourceforge.net/projects/wxpython/files/wxPython/2.8.12.1/>`_ (Cecilia5 is not compatible with WxPython 2.9 or 3.0). 
- `Subversion <http://subversion.apache.org/packages.html>`_ (to download Cecilia5 source code).
    
Then, you can download Cecilia5's sources by checking out the source code (in a terminal window):
    
.. code-block:: bash

    svn checkout http://cecilia5.googlecode.com/svn/trunk/ cecilia5-read-only
    
This will create a folder named "cecilia5-read-only" with the source code. 
Just go inside the folder and run Cecilia!

.. code-block:: bash

    cd cecilia5-read-only
    python Cecilia5.py

