Shifter : Phase Vocoder based frequency shifters
================================================

Description
------------

This module implements two voices that linearly moves the analysis bins 
by the amount, in Hertz, specified by the the `Shift 1` and `Shift 2` 
parameters.

Sliders
--------

    **Shift 1** : 
        Shifting, in Hertz, of the first voice
    **Shift 2** : 
        Shifting, in Hertz, of the second voice
    **Dry / Wet** : 
        Mix between the original signal and the delayed signals

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

    