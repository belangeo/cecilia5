SpectralGate : Spectral gate (Phase Vocoder)
============================================

Description
------------

For each frequency band of a phase vocoder analysis, if the amplitude
of the bin falls below a given threshold, it is attenuated according
to the `Gate Attenuation` parameter.

Sliders
--------

    **Gate Threshold** : 
        dB value at which the gate becomes active
    **Gate Attenuation** : 
        Gain in dB of the gated signal

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

    