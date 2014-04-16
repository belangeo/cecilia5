CrossSynth2 : Phase Vocoder based cross synthesis module
========================================================

Description
------------

Performs cross-synthesis between two phase vocoder streaming objects.

The amplitudes from `Source Exciter` and `Spectral Envelope`, scaled
by `Crossing Index`, are applied to the frequencies of `Source Exciter`.

Sliders
--------

    **Crossing Index** : 
        Morphing index between the two source's magnitudes
    **Exc Pre Filter Freq** : 
        Frequency of the pre-FFT filter
    **Exc Pre Filter Q** : 
        Q of the pre-FFT filter
    **Dry / Wet** : 
        Mix between the original signal and the processed signal

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Exc Pre Filter Type** : 
        Type of the pre-FFT filter
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

    