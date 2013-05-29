Mask Filter
============

Ranged filter module using band-pass filtering made with lowpass and highpass filters.


.. image:: /images/Parametres_MaskFilter.png

Sliders under the graph:
    - Filter 1 limits: Range of the first filter (minimum value = cut-off frequency of the highpass filter; maximum value = cut-off frequency of the lowpass filter).
    - Filter 2 limits: Range of the first filter (minimum value = cut-off frequency of the highpass filter; maximum value = cut-off frequency of the lowpass filter).
    - Mix: Balance between dry sound and processed sound.

Dropdown menus and toggles:
    - Number of Stages: Amount of stacked biquad filters.
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
