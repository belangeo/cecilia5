PitchLooper : Table-based transposition module with multiple voices
===================================================================

Description
------------

This module implements five sound loopers playing in parallel.
Loopers are table-based so a change in pitch will produce a 
change in sound duration. This can be useful to create rhythm
effects as well as harmonic effects.

Sliders
--------

    **Transpo Voice 1** : 
        Playback speed of the first voice
    **Gain Voice 1** : 
        Gain of the transposed first voice
    **Transpo Voice 2** : 
        Playback speed of the second voice
    **Gain Voice 2** : 
        Gain of the transposed second voice
    **Transpo Voice 3** : 
        Playback speed of the third voice
    **Gain Voice 3** : 
        Gain of the transposed third voice
    **Transpo Voice 4** : 
        Playback speed of the fourth voice
    **Gain Voice 4** : 
        Gain of the transposed fourth voice
    **Transpo Voice 5** : 
        Playback speed of the fifth voice
    **Gain Voice 5** : 
        Gain of the transposed fifth voice

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Voice Activation 1 --> 5** :
        Mute or unmute each voice independently
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    