cbutton : creates a button that can be used as an event trigger
===============================================================

Initline
---------

.. code::
    
    cbutton(name='button', label='Trigger', col='red', help='')
    
Description
------------

A button has no state, it only sends a trigger when it is clicked.

When the button is clicked, a function is called with the current 
state of the mouse (down or up) as argument.

If `name` is set to 'foo', the function should be defined like this :


.. code::

        def foo(self, value):
        
value is True on mouse pressed and False on mouse released.

Parameters
-----------

    **name** : str
        Name of the widget. Used to defined the function.
    **label** : str
        Label shown in the interface.
    **col** : str
        Color of the widget.
    **help** : str
        Help string shown in the button tooltip.

    