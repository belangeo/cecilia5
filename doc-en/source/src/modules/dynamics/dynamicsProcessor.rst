Dynamics Processor
=====================

Compression and noise gate module.


.. image:: /images/Parametres_Dynamics.png

Sliders under the graph:
    - Input Gain: Adjust the amount of signal sent to the processing chain.
    - Compression Thresh: Value in decibels at which the compressor becomes active.
    - Compression Rise Time: Time taken by the compressor to reach compression ratio.
    - Compression Fall Time: Time taken by the compressor to reach uncompressed state.
    - Compression Knee: Steepness of the compression curve.
    - Gate Thresh: Value in decibels at which the noise gate becomes active.
    - Gate Slope: Shape of the gate (rise time and fall time).
    - Output Gain: Makeup gain applied after the processing chain.

Dropdown menus and toggles:
    - Compression Ratio: Ratio between the compressed signal and the uncompressed signal.
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Transfer Function: Table used for waveshaping
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
