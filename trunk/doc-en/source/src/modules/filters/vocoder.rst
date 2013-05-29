Vocoder
============

Vocoder module in which the user will have to choose two inputs: a source signal (see "Spectral Envelope" - a signal with a preferably rich spectral envelope) and an exciter (see "Exciter" - preferably a dynamic signal).


.. image:: /images/Parametres_Vocoder.png

Sliders under the graph:
    - Base Frequency: Frequency of the first filter of the analyzer.
    - Frequency Spread: Frequency spread factor - exponential operator that determinates the frequency of all other filters of the analyzer.
    - Q Factor: Q factor of the filters of the analyzer.
    - Time Response: Time response of the envelope followers.
    - Gain: Gain of the vocoder filters.
    - Num of Bands: Number of filters for analyzing the signal.

Dropdown menus and toggles:
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
