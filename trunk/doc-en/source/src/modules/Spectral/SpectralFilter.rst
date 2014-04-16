SpectralFilter : Phase Vocoder based filter
===========================================

Description
------------

This module filters frequency components of a phase
vocoder analysed sound according to the shape drawn 
in the grapher function.

Sliders
--------

    **Dry / Wet** : 
        Mix between the original signal and the processed signal

Graph Only
-----------

    **Spectral Filter** : 
        Shape of the filter (amplitude of analysis bins)
    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

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

    