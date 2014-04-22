cfilein : creates a popup menu to load a soundfile in a table
=============================================================

Initline
---------

.. code::
    
    cfilein(name='filein', label='Audio', help='')
    
Description
------------

This interactive menu allows the user to import a soundfile into the 
processing module. When the user chooses a sound using the interface,
Cecilia will scan the whole folder for soundfiles. A submenu containing 
all soundfiles present in the folder will allow a quicker access to them 
later on.

More than one cfilein can be defined in a module. They will appear under 
the input label in the left side panel of the main window, in the order 
defined. 

In the processing class, use the BaseModule's method `addFilein` to 
retrieve the SndTable filled with the selected sound.


.. code::

        BaseModule.addFilein(name)

For a cfilein created with name='mysound', the table is retrieved 
using a call like this one:


.. code::

        self.table = self.addFilein('mysound')

Parameters
-----------

    **name** : str
        A string passed to the parameter `name` of the BaseModule.addFilein
        method. This method returns a SndTable object containing Cecilia's
        number of channels filled with the selected sound in the interface.
    **label** : str
        Label shown in the interface.
    **help** : str
        Help string shown in the widget's popup tooltip.

    