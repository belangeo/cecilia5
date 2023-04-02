MaskFilter : Ranged filter module using lowpass and highpass filters
====================================================================

Description
------------

The signal is first lowpassed and then highpassed to create a bandpass
filter with independant lower and higher boundaries. The user can
interpolate between two such filters.

Sliders
--------

    **Filter 1 Limits** : 
        Range of the first filter (min = highpass, max = lowpass)
    **Filter 2 Limits** : 
        Range of the second filter (min = highpass, max = lowpass)
    **Mix** :
        Balance between filter 1 and filter 2

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Number of Stages** : 
        Amount of stacked biquad filters
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    