AMFMFilter
============

Filtering module that works with an amplitude modulation (AM filter) or a frequency modulation (FM filter).


.. image:: /images/Parametres_AMFilter.png

Sliders under the graph:
    - Filter Freq: Center or cut-off frequency of the filter.
    - Resonance: Q factor (resonance) of the filter.
    - Mod Depth: Amplitude of the modulating wave (LFO - Low frequency oscillator).
    - Mod Freq: Frequency of the modulating wave (LFO).
    - Dry/Wet: Mix between the original signal and the filtered signal.

Dropdown menus and toggles:
    - Filter Type: Type of the filter (lowpass, highpass, bandpass or bandstop).
    - AM Mod Type: Waveform of the modulating LFO for amplitude modulation (saw up, saw down, square, triangle, pulse, bi-polar pulse, sample & hold or modulated sine).
    - FM Mod Type: Waveform of the modulating LFO for frequency modulation (saw up, saw down, square, triangle, pulse, bi-polar pulse, sample & hold or modulated sine).
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
