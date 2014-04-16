Degrade : Sampling rate and bit depth degradation with optional mirror clipping
===============================================================================

Description
------------

This module allows the user to degrade a sound with artificial resampling
and quantization. This process emulates the artifacts caused by a poor
sampling frequency or bit depth resolution. It optionally offers a simple
mirror distortion, if the degradation is not enough! 

Sliders
--------

    **Bit Depth** : 
            Resolution of the amplitude in bits
    **Sampling Rate Ratio** : 
            Ratio of the new sampling rate compared to the original one
    **Mirror Threshold** : 
            Clipping limits between -1 and 1 (signal is reflected around the thresholds)
    **Filter Freq** : 
            Center frequency of the filter
    **Filter Q** : 
            Q factor of the filter
    **Dry / Wet** : 
            Mix between the original signal and the degraded signal

Graph Only
-----------

    **Overall Amplitude** : 
            The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Filter Type** : 
            Type of filter
    **Clip Type** : 
            Choose between degradation only or with mirror clipping
    **Polyphony Voices** : 
            Number of voices played simultaneously (polyphony), 
            only available at initialization time
    **Polyphony Chords** : 
            Pitch interval between voices (chords), 
            only available at initialization time

    