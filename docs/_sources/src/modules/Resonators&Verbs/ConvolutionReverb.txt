ConvolutionReverb : FFT-based convolution reverb
================================================

Description
------------

This module implements a convolution based on a uniformly partitioned overlap-save
algorithm. It can be used to convolve an input signal with an impulse response 
soundfile to simulate real acoustic spaces.

Sliders
--------

    **Dry / Wet** : 
        Mix between the original signal and the convoluted signal

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    