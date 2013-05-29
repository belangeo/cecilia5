Distortion
======================

Distortion module with pre and post filters.


.. image:: /images/Parametres_Distorsion.png

Sliders under the graph:
    - Pre-Filter Freq: Center or cut-off frequency of the filter applied before distortion.
    - Pre-Filter Q: Q factor of the filter applied before distorsion.
    - Drive: Amount of distortion applied on the signal.
    - Post-Filter Freq: Center or cut-off frequency of the filter applied after distortion.
    - Post-Filter Q: Q factor of the filter applied after distortion.

Dropdown menus and toggles:
    - Pre-Filter Type: Type of filter used before distortion (lowpass, highpass, bandpass or bandstop).
    - Post-Filter Type: Type of filter used after distortion (lowpass, highpass, bandpass or bandstop).
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
