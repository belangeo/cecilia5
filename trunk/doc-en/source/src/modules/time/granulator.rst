Granulator
============

Granulation module.

.. image:: /images/Parametres_Granulator.png

Sliders under the graph:
    - Transpose: Base pitch of the grains compared to the original signal (in cents).
    - Grain Position: Input soundfile index for the beginning of the grains.
    - Position Random: Jitter applied on the soundfile index.
    - Pitch Random: Jitter applied on the pitch of the grains using a discreet transposition list (see below).
    - Filter Freq: Center or cut-off frequency of the filter.
    - Filter Q: Q factor of the filter.
    - Grain Duration: Length of the grains (in seconds).
    - # of Grains: Number of grains.

Dropdown menus and toggles:
    - Filter Type: Type of the filter (lowpass, highpass, bandpass or bandstop).
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - Discreet Transpo: Click in the box to enter a list of discreet values for transposition (see "Pitch Random" above).
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.