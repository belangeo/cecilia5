Granulator : Granulation module
===============================

Description
------------

A classic granulation module. Useful to stretch a sound without changing
the pitch or to transposition without changing the duration.

Sliders
--------

    **Transpose** : 
        Base pitch of the grains
    **Grain Position** : 
        Soundfile index
    **Position Random** : 
        Jitter applied on the soundfile index
    **Pitch Random** : 
        Jitter applied on the pitch of the grains using the discreet transpo list
    **Grain Duration** : 
        Length of the grains
    **Num of Grains** : 
        Number of overlapping grains

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
    **Discreet Transpo** : 
        List of pitch ratios    
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    