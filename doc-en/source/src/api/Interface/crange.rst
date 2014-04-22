crange : two-sided slider, with its own graph lines, for time-varying controls
==============================================================================

Initline
---------

.. code::
    
    crange(name='range', label='Pitch', min=20.0, max=20000.0, 
           init=[500.0, 2000.0], rel='log', res='float', gliss=0.025, 
           unit='x', up=False, func=None, midictl=None, col='red', help='')
    
Description
------------

This function creates a two-sided slider used to control a minimum and 
a maximum range at the sime time. When created, the range slider is 
stacked in the slider pane of the main Cecilia window in the order it 
is defined. The values of the range slider are passed to the module 
with a variable named `self.name`. The range minimum is collected using 
`self.name[0]` and the range maximum is collected using `self.name[1]`. 
The `up` argument passes the values of the range on mouse up if set to 
True or continuously if set to False. The `gliss` argument determines 
the duration of the portamento (in sec) applied on a new value. The 
resolution of the range slider can be set to 'int' or 'float' using the 
`res` argument. Slider color can be set using the `col` argument and a 
color value. However, sliders with `up` set to True are greyed out and 
the `col` argument is ignored.

Every time a range slider is defined, two graph lines are automatically 
defined for the grapher in the Cecilia interface. One is linked to the 
minimum value of the range, the other one to the maximum value of the 
range. The recording and playback of an automated slider is linked to its 
graph line.

Notes 
-------

In order to quickly select the minimum value (and graph line), the user 
can click on the left side of the crange label, and on the right side of 
the label to select the maximum value (and graph line).

Parameters
-----------

    **name** : str
        Name of the range slider.
    **label** : str
        Label shown in the crange label and the grapher popup.
    **min** : float
        Minimum value of the range slider.
    **max** : float
        Maximum value of the range slider.
    **init** : list of float
        Range slider minimum and maximum initial values.
    **rel** : str {'lin', 'log'}
        Range slider scaling. Defaults to 'lin'.
    **res** : str {'int', 'float'}
        Range slider resolution. Defaults to 'float'
    **gliss** : float
        Portamento between values in seconds. Defaults to 0.025.
    **unit** : str
        Unit symbol shown in the interface.
    **up** : boolean
        Value passed on mouse up if True. Defaults to False.
    **func** : list of list of tuples
        Initial automation in break-points format (serie of time/value 
        points). Times must be in increasing order between 0 and 1.
        The list must contain two lists of points, one for the minimum
        value and one for the maximum value.
    **midictl** : list of int
        Automatically map two midi controllers to this range slider. 
        Defaults to None.
    **col** : str
        Color of the widget.
    **help** : str
        Help string shown in the crange tooltip.

    