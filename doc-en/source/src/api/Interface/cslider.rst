cslider : creates a slider, and its own graph line, for time-varying controls
=============================================================================

Initline
---------

.. code::
    
    cslider(name='slider', label='Pitch', min=20.0, max=20000.0, init=1000.0, 
            rel='lin', res='float', gliss=0.025, unit='x', up=False, 
            func=None, midictl=None, half=False, col='red', help='')
    
Description
------------

When created, the slider is stacked in the slider pane of the main Cecilia
window in the order it is defined. The value of the slider is passed to 
the module with a variable named `self.name`. The `up` argument passes 
the value of the slider on mouse up if set to True or continuously if set 
to False. The `gliss` argument determines the duration of the portamento 
(in seconds) applied between values. The portamento is automatically set 
to 0 if `up` is True. The resolution of the slider can be set to int or 
float using the `res` argument. Slider color can be set using the `col` 
argument and a color value. However, sliders with `up` set to True are 
greyed out and the `col` argument is ignored.

If `up` is set to True, the cslider will not create an audio rate signal,
but will call a method named `widget_name` + '_up'. This method must be 
defined in the class `Module`. For a cslider with the name 'grains', the
method should be declared like this:


.. code::

    def grains_up(self, value):

Every time a slider is defined with `up` set to False, a corresponding 
graph line is automatically defined for the grapher in the Cecilia 
interface. The recording and playback of an automated slider is linked 
to its graph line.

Parameters
-----------

    **name** : str
        Name of the slider.
    **label** : str
        Label shown in the slider label and the grapher popup.
    **min** : float
        Minimum value of the slider.
    **max** : float
        Maximum value of the slider.
    **init** : float
        Slider's initial value.
    **rel** : str {'lin', 'log'}
        Slider scaling. Defaults to 'lin'.
    **res** : str {'int', 'float'}
        Slider resolution. Defaults to 'float'
    **gliss** : float
        Portamento between values in seconds. Defaults to 0.025.
    **unit** : str
        Unit symbol shown in the interface.
    **up** : boolean
        Value passed on mouse up if True. Defaults to False.
    **func** : list of tuples
        Initial automation in break-points format (serie of time/value 
        points). Times must be in increasing order between 0 and 1.
    **midictl** : int 
        Automatically map a midi controller to this slider. 
        Defaults to None.
    **half** : boolean
        Determines if the slider is full-width or half-width. Set to True
        to get half-width slider. Defaults to False.
    **col** : str
        Color of the widget.
    **help** : str
        Help string shown in the cslider tooltip.

    