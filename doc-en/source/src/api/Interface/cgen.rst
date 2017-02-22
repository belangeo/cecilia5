cgen : creates a list entry useful to generate list of arbitrary values
=======================================================================

Initline
---------

.. code::
    
    cgen(name='gen', label='Wave shape', init=[1,0,.3,0,.2,0,.143,0,.111], 
             rate='k', popup=None, col='red', help='')
    
Description
------------

Widget that can be used to create a list of floating-point values. A 
left click on the widget will open a floating window to enter the desired
values. Values can be separated by commas or by spaces.

If `rate` argument is set to 'i', a built-in reserved variable is created 
at initialization time. The variable name is constructed like this :


.. code::

        self.widget_name + '_value' for retrieving a list of floats.

If `name` is set to 'foo', the variable name will be:


.. code::

        self.foo_value (this variable is a list of floats)

If `rate` argument is set to 'k', a module method using one argument
must be defined with the name `name`. If `name` is set to 'foo', the 
function should be defined like this :


.. code::

        def foo(self, value):
            value -> list of strings

Parameters
-----------

    **name**: str
        Name of the widget. 
        Used to defined the function or the reserved variable.
    **label**: str
        Label shown in the interface.
    **init**: int
        An array of number, separated with commas, with which to 
        initialize the widget.
    **rate**: str {'k', 'i'}
        Indicates if the widget is handled at initialization time only 
        ('i') with a reserved variable or with a function ('k') that can 
        be called at any time during playback.
    **popup**: tuple (str, int) -> (popup's name, index)
        If a tuple is specified, and cgen is modified, the popup will 
        be automatically set to the given index.
    **col**: str
        Color of the widget.
    **help**: str
        Help string shown in the widget's tooltip.

    