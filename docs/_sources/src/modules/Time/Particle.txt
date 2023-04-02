Particle : A full-featured granulation module
=============================================

Description
-----------

This module offers more controls than the classic granulation module. 
Useful to generate clouds, to stretch a sound without changing the pitch 
or to transpose without changing the duration.

`Density per Second * Grain Duration` defines the overall overlaps.

Sliders
-------

    **Density per Second** :
        How many grains to play per second
    **Transpose** : 
        Overall transposition, in cents, of the grains
    **Grain Position** : 
        Soundfile index
    **Grain Duration** :
        Duration of each grain, in seconds
    **Start Time Deviation** :
        Maximum deviation of the starting time of the grain
    **Panning Random** :
        Random added to the panning of each grain
    **Density Random** :
        Jitter applied to the density per second
    **Pitch Random** : 
        Jitter applied on the pitch of the grains
    **Position Random** : 
        Jitter applied on the soundfile index
    **Duration Random** : 
        Jitter applied to the grain duration

Graph Only
----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance
    **Grain Envelope** : 
        Emplitude envelope of the grains

Popups & Toggles
----------------

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
