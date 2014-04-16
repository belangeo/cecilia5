FeedbackLooper : Frequency self-modulated sound looper
======================================================

Description
------------

This module loads a sound in a table and apply a frequency self-modulated
playback of the content. A Frequency self-modulation occurs when the
output sound of the playback is used to modulate the reading pointer speed.
That produces new harmonics in a way similar to waveshaping distortion. 

Sliders
--------

    **Transposition** : 
            Transposition, in cents, of the input sound
    **Feedback** : 
            Amount of self-modulation in sound playback
    **Filter Frequency** : 
            Frequency, in Hertz, of the filter
    **Filter Q** : 
            Q of the filter (inverse of the bandwidth)

Graph Only
-----------

    **Overall Amplitude** : 
            The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Filter Type** : 
            Type of the filter
    **Polyphony Voices** : 
            Number of voices played simultaneously (polyphony), 
            only available at initialization time
    **Polyphony Chords** : 
            Pitch interval between voices (chords), 
            only available at initialization time

    