Resonators : Eight resonators with jitter control
=================================================

Description
------------

This module implements a resonator (waveguide) bank with random controls.

This waveguide model consists of one delay-line with a simple
lowpass filtering and lagrange interpolation.

Sliders
--------

    **Pitch Offset** : 
        Base pitch of all the resonators
    **Amp Random Amp** : 
        Amplitude of the jitter applied on the resonators amplitude
    **Amp Random Speed** : 
        Frequency of the jitter applied on the resonators amplitude
    **Delay Random Amp** : 
        Amplitude of the jitter applied on the resonators delay (pitch)
    **Delay Random Speed** : 
        Frequency of the jitter applied on the resonators delay (pitch)
    **Pitch Voice 1** : 
        Pitch of the first resonator
    **Pitch Voice 2** : 
        Pitch of the second resonator
    **Pitch Voice 3** : 
        Pitch of the third resonator
    **Pitch Voice 4** : 
        Pitch of the fourth resonator
    **Pitch Voice 5** : 
        Pitch of the fifth resonator
    **Pitch Voice 6** : 
        Pitch of the sixth resonator
    **Pitch Voice 7** : 
        Pitch of the seventh resonator
    **Pitch Voice 8** : 
        Pitch of the eigth resonator
    **Feedback** : 
        Amount of resonators fed back in the resonators
    **Dry / Wet** : 
        Mix between the original signal and the resonators

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Voice Activation ( 1 --> 8 )** :
        Mute or unmute each of the eigth voices independently
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    