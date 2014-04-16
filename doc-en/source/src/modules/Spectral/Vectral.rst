Vectral : Phase Vocoder based vectral module (spectral gate and verb)
=====================================================================

Description
------------

This module implements a spectral gate followed by a spectral reverb.

Sliders
--------

    **Gate Threshold** : 
        dB value at which the gate becomes active
    **Gate Attenuation** : 
        Gain in dB of the gated signal
    **Time Factor** : 
        Filter coefficient for decreasing bins
    **High Freq Damping** : 
        High frequencies damping factor
    **Dry / Wet** : 
        Mix between the original signal and the delayed signals

Graph Only
-----------

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

    