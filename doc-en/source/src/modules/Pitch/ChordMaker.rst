ChordMaker : Sampler-based harmonizer module with multiple voices
=================================================================

Description
------------

The input sound is mixed with five real-time, non-stretching,
harmonization voices.

Sliders
--------

    **Transpo Voice 1** : 
        Pitch shift of the first voice
    **Gain Voice 1** : 
        Gain of the transposed first voice
    **Transpo Voice 2** : 
        Pitch shift of the second voice
    **Gain Voice 2** : 
        Gain of the transposed second voice
    **Transpo Voice 3** : 
        Pitch shift of the third voice
    **Gain Voice 3** : 
        Gain of the transposed third voice
    **Transpo Voice 4** : 
        Pitch shift of the fourth voice
    **Gain Voice 4** : 
        Gain of the transposed fourth voice
    **Transpo Voice 5** : 
        Pitch shift of the fifth voice
    **Gain Voice 5** : 
        Gain of the transposed fifth voice
    **Feedback** : 
        Amount of transposed signal fed back into the harmonizers
        (feedback is voice independent)
    **Dry / Wet** : 
        Mix between the original signal and the harmonized signals

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Win Size** :
        Harmonizer window size in seconds
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    # Voice Activation (1 --> 5)
        Mute or unmute each voice independently
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    