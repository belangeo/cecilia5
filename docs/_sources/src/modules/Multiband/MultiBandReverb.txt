MultiBandReverb : Multi-band reverberation module
=================================================

Description
------------

MultiBandReverb implements four separated spectral band 
harmonizers with independent reverb time, cutoff and gain.

Sliders
--------

    **Frequency Splitter** : 
        Split points for multi-band processing
    **Reverb Time 1** : 
        Amount of reverb (tail duration) applied on first band
    **Lowpass Cutoff 1** : 
        Cutoff frequency of the reverb's lowpass filter (damp) for the first band
    **Gain 1** : 
        Gain of the reverberized first band
    **Reverb Time 2** : 
        Amount of reverb (tail duration) applied on second band
    **Lowpass Cutoff 2** : 
        Cutoff frequency of the reverb's lowpass filter (damp) for the second band
    **Gain 2** : 
        Gain of the reverberized second band
    **Reverb Time 3** : 
        Amount of reverb (tail duration) applied on third band
    **Lowpass Cutoff 3** : 
        Cutoff frequency of the reverb's lowpass filter (damp) for the third band
    **Gain 3** : 
        Gain of the reverberized third band
    **Reverb Time 4** : 
        Amount of reverb (tail duration) applied on fourth band
    **Lowpass Cutoff 4** : 
        Cutoff frequency of the reverb's lowpass filter (damp) for the fourth band
    **Gain 4** : 
        Gain of the reverberized fourth band
    **Dry / Wet** : 
        Mix between the original signal and the harmonized signals

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

    