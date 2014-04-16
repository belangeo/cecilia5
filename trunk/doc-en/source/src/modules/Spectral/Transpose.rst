Transpose : Phase Vocoder based two voices transposer
=====================================================

Description
------------

This module transpose the frequency components of a phase 
vocoder analysis.

Sliders
--------

    **Transpo 1** : 
        Transposition factor of the first voice
    **Transpo 2** : 
        Transposition factor of the second voice
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

    