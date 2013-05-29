BeatMaker
============

Algorithmic beatmaker module.

.. image:: /images/Parametres_BeatMaker.png

Sliders under the graph:
    - # of Taps: Number of taps in each bar.
    - Tempo: Speed of taps (in bpm).
    - Beat Tap Length: Length of taps (in seconds - for beats one to four).
    - Beat Index: Input soundfile index for each beat (from 0 to 1 - for beats one to four).
    - Beat Gain: Gain (in decibels) of the beat (for beats one to four).
    - Beat Distribution: Repartition of taps for each beat (from 100% weak to 100% down - for beats one to four).
    - Global seed: Seed value for the algorithmic beats, using the same seed with the same distribution will yield the exact same beats.

Dropdown menus and toggles:
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Beat 1 ADSR: Amplitude envelope of taps for the first beat in breakpoint fashion.
    - Beat 2 ADSR: Amplitude envelope of taps for the second beat in breakpoint fashion.
    - Beat 3 ADSR: Amplitude envelope of taps for the third beat in breakpoint fashion.
    - Beat 4 ADSR: Amplitude envelope of taps for the fourth beat in breakpoint fashion.
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
