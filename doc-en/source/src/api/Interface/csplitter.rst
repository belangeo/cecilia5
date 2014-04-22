csplitter : creates a multi-knobs slider used to split the spectrum in sub-regions
==================================================================================

Initline
---------

.. code::
    
    csplitter(name='splitter', label='Pitch', min=20.0, max=20000.0, 
              init=[500.0, 2000.0, 5000.0], rel='log', res='float', 
              gliss=0.025, unit='x', up=False, num_knobs=3, col='red', help='')
    
Description
------------

When created, the splitter is stacked in the slider pane of the main 
Cecilia window in the order it is defined. The values of the splitter 
slider are passed to the module with a variable named `self.name`. The 
knob values are collected using `self.name[0]` to `self.name[num-knobs-1]`.
The `up` argument passes the values of the splitter on mouse up if set to 
True or continuously if set to False. The `gliss` argument determines the 
duration of the portamento (in seconds) applied between values. The 
resolution of the splitter slider can be set to int or float using the 
`res` argument. The slider color can be set using the `col` argument and 
a color value. However, sliders with `up` set to True are greyed out and 
the `col` argument is ignored.

The csplitter is designed to be used with the FourBand() object in
order to allow multi-band processing. Although the FourBand() parameters 
can be changed at audio rate, it is not recommended. This filter is CPU 
intensive and can have erratic behavior when boundaries are changed too 
quickly.

Parameters
-----------

    **name** : str
        Name of the splitter slider.
    **label** : str
        Label shown in the csplitter label.
    **min** : float
        Minimum value of the splitter slider.
    **max** : float
        Maximum value of the splitter slider.
    **init** : list of float
        Splitter knobs initial values. List must be of length `num_knobs`.
        Defaults to [500.0, 2000.0, 5000.0].
    **rel** : str {'lin', 'log'}
        Splitter slider scaling. Defaults to 'lin'.
    **res** : str {'int', 'float'}
        Splitter slider resolution. Defaults to 'float'
    **gliss** : float
        Portamento between values in seconds. Defaults to 0.025.
    **unit** : str
        Unit symbol shown in the interface.
    **up** : boolean
        Value passed on mouse up if True. Defaults to False.
    **num_knobs** : int
        Number of junction knobs. Defaults to 3.
    **col** : str
        Color of the widget.
    **help** : str
        Help string shown in the csplitter tooltip.

    