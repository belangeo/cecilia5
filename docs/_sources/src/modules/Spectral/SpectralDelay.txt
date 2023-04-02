SpectralDelay : Phase vocoder spectral delay
============================================

Description
------------

This module applies different delay times and feedbacks for
each bin of a phase vocoder analysis. Delay times and
feedbacks are specified via grapher functions.

Sliders
--------

    **Max Delay** : 
        Maximum delay time per bin. Used to allocate memories.
        only available at initialization time
    **Dry / Wet** : 
        Mix between the original signal and the delayed signals

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance 
    **Bin Delays** : 
        Controls the delay time for every bin, 
        from left (low freq) to right (high freq) on the graph
    **Bin Feedbacks** : 
        Controls the feedback factor for every bin, from left to right on the graph

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

    