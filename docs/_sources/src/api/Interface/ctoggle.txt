ctoggle : creates a two-states button
=====================================

Initline
---------

.. code::
    
    ctoggle(name='toggle', label='Start/Stop', init=True, rate='k', 
            stack=False, col='red', help='')
    
Description
------------

A toggle button is a two-states switch that can be used to start and stop
processes.

If `rate` argument is set to 'i', a built-in reserved variable is created 
at initialization time. The variable's name is constructed like this :
    

.. code::

        self.widget_name + '_value'
    
If `name` is set to 'foo', the variable's name will be:


.. code::

        self.foo_value

If `rate` argument is set to 'k', a module method using one argument
must be defined with the name `name`. If `name` is set to 'foo', the 
function should be defined like this :


.. code::

        def foo(self, value):
        
value is an integer (0 or 1).

Parameters
-----------

    **name**: str
        Name of the widget used to defined the function or the 
        reserved variable.
    **label**: str
        Label shown in the interface.
    **init**: int
        Initial state of the toggle.
    **rate**: str {'k', 'i'}
        Indicates if the toggle is handled at initialization time only 
        ('i') with a reserved variable or with a function ('k') that can 
        be called at any time during playback.
    **stack**: boolean
        If True, the toggle will be added on the same row as the last 
        toogle with stack=True and a label not empty. Defaults to False.
    **col**: str
        Color of the widget.
    **help**: str
        Help string shown in the toggle tooltip.

    