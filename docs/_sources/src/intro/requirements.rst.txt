Installation - Requirements
===========================

Python
------

Python 3.11 or newer must be installed before installing Cecilia.
You can download Python from https://www.python.org/downloads/.

Cecilia is compatible with the following systems:

- MacOS 
- Windows
- Linux

Install with pip
----------------

Install Cecilia from PyPI using the command for your operating system.
Replace ``3.14`` with the Python version installed on your system.

Windows:

.. code-block:: bash

    py -3.14 -m pip install -U cecilia

Linux/macOS:

.. code-block:: bash

    python3.14 -m pip install -U cecilia

Then run it:

.. code-block:: bash

    cecilia

Desktop registration
--------------------

On Linux, Windows or macOS, register Cecilia in your application menu by running once
after installation::

    cecilia-register-desktop

On Linux, this creates ``~/.local/share/applications/cecilia.desktop`` for your
user. On Windows, it creates a ``Cecilia5`` shortcut in your Start menu using
Windows PowerShell. The shortcut launches Cecilia without a console window.
On macOS, this creates a lightweight ``~/Applications/Cecilia5.app`` launcher
with the Cecilia icon, which you can open in Finder or drag to the Dock. It uses
the current Python installation without opening Terminal. Registration refreshes
an existing launcher but refuses to overwrite a standalone application.

If you installed Cecilia in a virtual environment, run the command from that
environment and keep it installed for the menu entry to work. Run the command
again if you move or reinstall Cecilia in a different environment.

The macOS launcher uses the built-in ``osacompile`` and ``codesign`` tools to
create a locally ad hoc signed applet; it is not Developer ID signed or notarized.
It includes a microphone usage description, but audio input still requires your
permission in System Settings > Privacy & Security > Microphone. Permission
attribution and persistence depend on your Python installation; this launcher
does not provide the signing or entitlement guarantees of a standalone app.

Running Cecilia from the latest sources
----------------------------------------

Before running Cecilia from the latest sources, install its dependencies using
the command for your operating system. Replace ``3.14`` with the Python version
installed on your system in both the installation and launch commands below.

Windows:

.. code-block:: bash

    py -3.14 -m pip install -U pyo wxPython numpy

Linux/macOS:

.. code-block:: bash

    python3.14 -m pip install -U pyo wxPython numpy

Then, you can download Cecilia's sources by checking out the source code (in a terminal window):
    
.. code-block:: bash

    git clone https://github.com/belangeo/cecilia5.git
    
This will create a folder named "cecilia5" with the source code. 
Go inside the folder and run Cecilia using the same Python version as above.

Windows:

.. code-block:: bash

    cd cecilia5
    py -3.14 Cecilia5.py

Linux/macOS:

.. code-block:: bash

    cd cecilia5
    python3.14 Cecilia5.py
