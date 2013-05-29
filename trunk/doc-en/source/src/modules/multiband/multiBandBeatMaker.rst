MultiBandBeatMaker
======================

Multi-band algorithmic beatmaker module.


.. image:: /images/Parametres_MBBeatMaker.png

Sliders under the graph:
    - Frequency splitter: Split points of the frequency range for multi-band processing.
    - # of Taps: Number of taps in a measure.
    - Tempo: Speed of taps (in beats per minute).
    - Tap Length: Length of taps (in seconds).
    - Beat 1 Index: Soundfile index of the first beat.
    - Beat 2 Index: Soundfile index of the second beat.
    - Beat 3 Index: Soundfile index of the third beat.
    - Beat 4 Index: Soundfile index of the fourth beat.
    - Beat 1 Distribution: Repartition of taps for the first beat (100 % weak --> 100 % down).
    - Beat 2 Distribution: Repartition of taps for the second beat (100 % weak --> 100 % down).
    - Beat 3 Distribution: Repartition of taps for the third beat (100 % weak --> 100 % down).
    - Beat 4 Distribution: Repartition of taps for the fourth beat (100 % weak --> 100 % down).
    - Beat 1 Gain: Gain of the first beat.
    - Beat 2 Gain: Gain of the second beat.
    - Beat 3 Gain: Gain of the third beat.
    - Beat 4 Gain: Gain of the fourth beat.
    - Global Seed: Seed value for the algorithmic beats; using the same seed with the same distributions will yield the exact same beats.

Dropdown menus and toggles:
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Beat 1 ADSR: Envelope of taps for the first beat in breakpoint fashion.
    - Beat 2 ADSR: Envelope of taps for the second beat in breakpoint fashion.
    - Beat 3 ADSR: Envelope of taps for the third beat in breakpoint fashion.
    - Beat 4 ADSR: Envelope of taps for the fourth beat in breakpoint fashion.
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
