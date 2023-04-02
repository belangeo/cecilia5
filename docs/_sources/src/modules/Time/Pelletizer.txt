Pelletizer : Another granulation module
=======================================

Description
------------

A granulation module where the number of grains (density) and
the grain duration can be set independently. Useful to stretch 
a sound without changing the pitch or to transposition without 
changing the duration.

Sliders
--------

    **Transpose** : 
        Base pitch of the grains
    **Density of grains** : 
        Number of grains per second
    **Grain Position** : 
        Grain start position in the position 
    **Grain Duration** : 
        Duration of the grain in seconds
    **Pitch Random** : 
        Jitter applied on the pitch of the grains
    **Density Random** : 
        Jitter applied on the density
    **Position Random** : 
        Jitter applied on the grain start position
    **Duration Random** : 
        Jitter applied on the duration of the grain
    **Filter Freq** : 
        Cutoff or center frequency of the filter (post-processing)
    **Filter Q** : 
        Q of the filter

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance
    **Grain Envelope** : 
        Emplitude envelope of the grains

Popups & Toggles
-----------------

    **Filter Type** : 
        Type of the post filter
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Discreet Transpo** : 
        List of pitch ratios
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    