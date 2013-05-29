MultiBandGate
===============

Multi-band noise gate module.


.. image:: /images/Parametres_MBBandGate.png

Sliders under the graph:
    - Frequency Splitter: Split points in the frequency range for multi-band processing.
    - Threshold Band 1: Value in decibels at which the gate becomes active on the first band.
    - Gain Band 1: Gain of the gated first band (in decibels). 
    - Threshold Band 2: Value in decibels at which the gate becomes active on the second band.
    - Gain Band 2: Gain of the gated second band (in decibels).
    - Threshold Band 3: Value in decibels at which the gate becomes active on the third band.
    - Gain Band 3: Gain of the gated third band (in decibels).
    - Threshold Band 4: Value in decibels at which the gate becomes active on the fourth band.
    - Gain Band 4: Gain of the gated fourth band (in decibels).
    - Rise Time: Time taken by the gate to close (in seconds).
    - Fall Time: Time taken by the gate to re-open (in seconds).

Dropdown menus and toggles:
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
