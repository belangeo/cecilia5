WGuideBank
===============

Multiple waveguide models module.

.. image:: /images/Parametres_WGuideBank.png


Sliders under the graph:
    - Base Freq: Base pitch of the waveguides (in Hertz).
    - WG Expansion: Spread factor that determines the range between the waveguides.
    - WG Feedback: Amount of output sound sent back into the delay lines.
    - Filter Cutoff: Cutoff or center frequency of the filter (in Hertz).
    - Amp Dev Amp: Amplitude of the jitter applied to the waveguides amplitudes.
    - Amp Dev Speed: Frequency of the jitter applied to the waveguides amplitudes.
    - Freq Dev Amp: Amplitude of the jitter applied to the waveguides pitch.
    - Freq Dev Speed: Frequency of the jitter applied to the waveguides pitch.
    - Dry/Wet: Mix betwwen the original signal and the waveguides signals.

Dropdown menus and toggles:
    - Filter Type: Type of the filter used in the module (lowpass, highpass, bandpass or bandstop).
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.