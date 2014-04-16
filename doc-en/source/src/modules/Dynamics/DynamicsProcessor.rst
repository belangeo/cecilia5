DynamicsProcessor : Dynamic compression and gate module
=======================================================

Description
------------

This module can be used to adjust the dynamic range of a signal by applying a compressor
followed by a gate.

Sliders
--------

    **Input Gain** : 
        Adjust the amount of signal sent to the processing chain
    **Comp Thresh** : 
        dB value at which the compressor becomes active
    **Comp Rise Time** : 
        Time taken by the compressor to reach compression ratio
    **Comp Fall Time** : 
        Time taken by the compressor to reach uncompressed state
    **Comp Knee** : 
        Steepness of the compression curve
    **Gate Thresh** : 
        dB value at which the gate becomes active
    **Gate Rise Time** : 
        Time taken to open the gate
    **Gate Fall Time** : 
        Time taken to close the gate
    **Output Gain** : 
        Makeup gain applied after the processing chain

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Compression Ratio** : 
        Ratio between the compressed signal and the uncompressed signal
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    