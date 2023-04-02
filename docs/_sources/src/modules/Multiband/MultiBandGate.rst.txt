MultiBandGate : Multi-band noise gate module
============================================

Description
------------

MultiBandGate implements four separated spectral band 
noise gaters with independent threshold and gain.

Sliders
--------

    **Frequency Splitter** : 
        Split points for multi-band processing
    **Threshold Band 1** : 
        dB value at which the gate becomes active on the first band
    **Gain Band 1** : 
        Gain of the gated first band
    **Threshold Band 2** : 
        dB value at which the gate becomes active on the second band
    **Gain Band 2** : 
        Gain of the gated second band
    **Threshold Band 3** : 
        dB value at which the gate becomes active on the third band
    **Gain Band 3** : 
        Gain of the gated third band
    **Threshold Band 4** : 
        dB value at which the gate becomes active on the fourth band
    **Gain Band 4** : 
        Gain of the gated fourth band
    **Rise Time** : 
        Time taken by the gate to close
    **Fall Time** : 
        Time taken by the gate to open
    **Dry / Wet** : 
        Mix between the original signal and the shifted signals

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

    