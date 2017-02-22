cgraph : creates a graph only automated parameter or a shapeable envelope
=========================================================================

Initline
---------

.. code::
    
    cgraph(name='graph', label='Envelope', min=0.0, max=1.0, rel='lin', 
           table=False, size=8192, unit='x', curved=False, 
           func=[(0, 0.), (.01, 1), (.99, 1), (1, 0.)], col='red')
    
Description
------------

A graph line represents the evolution of a variable during a Cecilia 
performance. The value of the graph is passed to the module with a 
variable named `self.name`. The 'func' argument defines an initial 
break-point line shaped with time/value pairs (floats) as a list. Time 
values must be defined from 0 to 1 and are multiplied by the total_time 
of the process. When True, the 'table' argument writes the graph line in 
a PyoTableObject named with the variable `self.name`. The graph can then 
be used for any purpose in the module by recalling its variable. The 
`col` argument defines the color of the graph line using a color value.

Parameters
-----------

    **name**: str
        Name of the grapher line.
    **label**: str
        Label shown in the grapher popup.
    **min**: float
        Minimum value for the Y axis.
    **max**: float
        Maximum value for the Y axis.
    **rel**: str {'lin', 'log'}
        Y axis scaling.
    **table**: boolean
        If True, a PyoTableObject will be created instead of a 
        control variable.
    **size**: int
        Size, in samples, of the PyoTableObject.
    **unit**: str
        Unit symbol shown in the interface.
    **curved**: boolean
        If True, a cosinus segments will be drawn between points. 
        The curved mode can be switched by double-click on the curve 
        in the grapher. Defaults to Flase
    **func**: list of tuples
        Initial graph line in break-points (serie of time/value points).
        Times must be in increasing order between 0 and 1.
    **col**: str
        Color of the widget.
