Degrade
==========

Sampling rate and bit depth degradation module with optional waveform aliasing around a clipping threshold.


.. image:: /images/Parametres_Degrade.png

Sliders under the graph:
    - Bit Depth: Resolution of the amplitude in bits.
    - Sampling Rate Ratio: Ratio of the new sampling rate compared to the original one.
    - Wrap Threshold: Clipping limit (for the waveform aliasing) between -1 and 1 (signal then wraps around the thresholds).
    - Filter Freq: Center or cut-off frequency of the filter.
    - Filter Q: Q factor of the filter
    - Dry/Wet: Mix between the original signal and the degraded signal.

Dropdown menus and toggles:
    - Filter Type: Type of filter (lowpass, highpass, bandpass or bandstop).
    - Clip Type: Choose between degradation only or degradation with waveform aliasing.
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
