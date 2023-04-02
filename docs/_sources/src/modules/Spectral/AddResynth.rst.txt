AddResynth : Phase vocoder additive resynthesis
===============================================

Description
------------

This module uses the magnitudes and true frequencies of a
phase vocoder analysis to control amplitudes and frequencies 
envelopes of an oscillator bank.

Sliders
--------

    **Transpo** : 
        Transposition factor
    **Num of Oscs** : 
        Number of oscillators used to synthesize the sound
    **First bin** : 
        First synthesized bin
    **Increment** : 
        Step between synthesized bins
    **Dry / Wet** : 
        Mix between the original signal and the processed signal

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
    
    