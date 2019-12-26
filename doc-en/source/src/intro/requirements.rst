Installation - Requirements
============================

Cecilia is compatible with the following systems:

- Mac OS X (10.12+) 
- Windows (7, 8, 8.1, 10)
- Linux (at least Debian-based distros but should work with other linux flavours)
    

Installing Cecilia on Windows or OSX
---------------------------------------

Windows and OSX users can download self-contained binaries of the latest version of 
Cecilia `here <http://ajaxsoundstudio.com/software/cecilia/>`_.

Older binaries for the 5.3.x serie can be downloaded on `github <https://github.com/belangeo/cecilia5/releases/>`_.

Running Cecilia from the lastest sources
-------------------------------------------

Before running Cecilia from the latest sources, 
please check if all these elements are installed on your computer:

- `Python 3.7 <https://www.python.org/downloads/release/python-376/>`_
- `Pyo 1.0.1 <http://ajaxsoundstudio.com/software/pyo/>`_
- `Numpy 1.18 <https://pypi.python.org/pypi/numpy>`_
- `WxPython 4.0.7 <https://wxpython.org/pages/downloads/>`_ (install with `pip install wxPython`)
- `Git client <https://git-scm.com/downloads>`_
    
Then, you can download Cecilia's sources by checking out the source code (in a terminal window):
    
.. code-block:: bash

    git clone https://github.com/belangeo/cecilia5.git
    
This will create a folder named "cecilia5" with the source code. 
Just go inside the folder and run Cecilia!

.. code-block:: bash

    cd cecilia5
    python3 Cecilia5.py

