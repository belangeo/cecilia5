ChordMaker
==============

Sampler based harmonizer module with multiple voices.


.. image:: /images/Parametres_ChordMaker.png

Sliders under the graph:
    - Transpo Voice 1: Pitch shift of the first voice.
    - Gain Voice 1: Gain of the transposed first voice.
    - Transpo Voice 2: Pitch shift of the second voice.
    - Gain Voice 2: Gain of the transposed second voice.
    - Transpo Voice 3: Pitch shift of the third voice.
    - Gain Voice 3: Gain of the transposed third voice.
    - Transpo Voice 4: Pitch shift of the fourth voice.
    - Gain Voice 4: Gain of the transposed fourth voice.
    - Transpo Voice 5: Pitch shift of the fifth voice.
    - Gain Voice 5: Gain of the transposed fifth voice.
    - Feedback: Amount of transposed signal fed back into the harmonizers (feedback is voice independent).
    - Dry/Wet: Mix between the original signal and the harmonized signals.

Dropdown menus and toggles:
    - Voice 1: Mute or unmute the first voice 
    - Voice 2: Mute or unmute the second voice
    - Voice 3: Mute or unmute the third voice
    - Voice 4: Mute or unmute the fourth voice
    - Voice 5: Mute or unmute the fifth voice
    - # of Polyphony: Number of voices played simultaneously (in polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.