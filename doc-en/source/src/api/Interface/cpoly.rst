cpoly : creates two popup menus used as polyphony manager
=========================================================

Initline
---------

.. code::
    
    cpoly(name='poly', label='Polyphony', min=1, max=10, init=1, help='')
    
Description
------------

cpoly is a widget conceived to help manage the voice polyphony of a 
module. cpoly comes with a popup menu that allows the user to choose how 
many instances (voices) of a process will be simultaneously playing. It 
also provides another popup to choose the type of polyphony (phasing, 
chorus, out-of-tune or one of the provided chords).

cpoly has two values that are passed to the processing module: the number 
of voices and the voice spread. The number of voices can be collected 
using `self.number_of_voices`. `self.polyphony_spread` gives access to 
the transposition factors defined by the type of polyphony.

If a csampler is used, you don't need to take care of polyphony, it's 
automatically handled inside the csampler. Without a csampler, user can 
retrieve polyphony popups values with these builtin reserved 
variables :
    
    **self.number_of_voices** : int
        Number of layers of polyphony
    **self.polyphony_spread** : list of floats
        Transposition factors as a list of floats
    **self.polyphony_scaling** : float
        An amplitude factor based on the number of voices

Notes 
-------

The cpoly interface object and its associated variables can be used in 
the dsp module any way one sees fit.

No more than one `cpoly` can be declared in a module.

Parameters
-----------

    **name** : str
        Name of the widget.
    **label** : str
        Label shown in the interface.
    **min** : int
        Minimum value for the number of layers slider.
    **max** : int
        Maximum value for the number of layers slider.
    **init** : int
        Initial value for the number of layers slider.
    **help** : str
        Help string shown in the cpoly tooltip.

    