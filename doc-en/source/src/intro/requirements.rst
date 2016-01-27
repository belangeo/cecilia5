Installation - Requirements
============================

Cecilia5 is compatible with the following systems:

- Mac OS X (from 10.5 to 10.10) 
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

- `Python 2.6 <https://www.python.org/download/releases/2.6.6>`_ or `Python 2.7 <https://www.python.org/download/releases/2.7.8>`_. 
- `Pyo 0.7.8 <http://ajaxsoundstudio.com/software/pyo/>`_ (or compiled with latest `sources <http://code.google.com/p/pyo>`_).
- `Numpy 1.6.0 or higher <http://sourceforge.net/projects/numpy/files/NumPy/>`_ (but below 1.9).
- `WxPython 3.0 <http://wxpython.org/download.php>`_. 
- `Git client <https://git-scm.com/downloads>`_.
    
Then, you can download Cecilia5's sources by checking out the source code (in a terminal window):
    
.. code-block:: bash

    git clone https://github.com/belangeo/cecilia5.git
    
This will create a folder named "cecilia5" with the source code. 
Just go inside the folder and run Cecilia!

.. code-block:: bash

    cd cecilia5
    python Cecilia5.py

