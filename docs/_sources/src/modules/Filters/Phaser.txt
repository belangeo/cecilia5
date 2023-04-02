Phaser : Multi-stages second-order phase shifter allpass filters
================================================================

Description
------------

Phaser implements a multi-stages second-order allpass filters,
which, when mixed with the original signal, create a serie of
peaks/notches in the sound.

Sliders
--------

    **Base Freq** : 
        Center frequency of the first notch of the phaser
    **Q Factor** : 
        Q factor (resonance) of the phaser notches
    **Notch Spread** : 
        Distance between phaser notches
    **Feedback** : 
        Amount of phased signal fed back into the phaser
    **Dry / Wet** : 
        Mix between the original signal and the phased signal

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Number of Stages** : 
        Changes notches bandwidth (stacked filters),
        only available at initialization time
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    