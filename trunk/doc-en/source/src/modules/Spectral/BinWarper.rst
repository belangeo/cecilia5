BinWarper : Phase vocoder buffer with bin independent speed playback
====================================================================

Description
------------

This module pre-analyses the input sound and keeps the
phase vocoder frames in a buffer for the playback. User
has control on playback position independently for every 
frequency bin.

Sliders
--------

    **Low Bin Speed** : 
        Lowest bin speed factor
    **High Bin Speed** : 
        Highest bin speed factor

    * For random distribution, these values are the 
      minimum and the maximum of the distribution.

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance
        
Popups & Toggles
-----------------

    **Reset** : 
        Reset pointer positions to the beginning of the buffer.
    **Speed Distribution** : 
        Speed distribution algorithm.
    **FFT Size** : 
        Size, in samples, of the FFT
    **FFT Envelope** : 
        Windowing shape of the FFT
    **FFT Overlaps** : 
        Number of FFT overlaping analysis
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    