cpopup : creates a popup menu offering a limited set of choices
===============================================================

Initline
---------

.. code::
    
    cpopup(name='popup', label='Chooser', value=['1', '2', '3', '4'],
               init='1', rate='k', col='red', help='')
    
Description
------------

A popup menu offers a limited set choices that are available to modify
the state of the current module.

If `rate` argument is set to 'i', two built-in reserved variables are 
created at initialization time. The variables' names are constructed 
like this :


.. code::

        self.widget_name + '_index' for the selected position in the popup.
        self.widget_name + '_value' for the selected string in the popup.

If `name` is set to 'foo', the variables names will be:


.. code::

        self.foo_index (this variable is an integer)
        self.foo_value (this variable is a string)

If `rate` argument is set to 'k', a module method using two arguments
must be defined with the name `name`. If `name` is set to 'foo', the 
function should be defined like this :


.. code::

        def foo(self, index, value):
            index -> int
            value -> str

Parameters
-----------

    **name**: str
        Name of the widget. 
        Used to defined the function or the reserved variables.
    **label**: str
        Label shown in the interface.
    **value**: list of strings
        An array of strings with which to initialize the popup.
    **init**: int
        Initial state of the popup.
    **rate**: str {'k', 'i'}
        Indicates if the popup is handled at initialization time only 
        ('i') with reserved variables or with a function ('k') that can 
        be called at any time during playback.
    **col**: str
        Color of the widget.
    **help**: str
        Help string shown in the popup tooltip.

    