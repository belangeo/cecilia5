Morphing : Phase Vocoder based morphing module
==============================================

Description
------------

This module performs spectral morphing between two phase vocoder analysis.

According to `Morphing Index`, the amplitudes from two PV analysis
are interpolated linearly while the frequencies are interpolated
exponentially.

Sliders
--------

    **Morphing Index** : 
        Morphing index between the two sources
    **Dry / Wet** : 
        Mix between the original signal and the morphed signal

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

    