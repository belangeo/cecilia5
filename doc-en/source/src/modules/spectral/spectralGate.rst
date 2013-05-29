SpectralGate
==============

Spectral noise gate module based on fast-Fourier-transform (FFT) operations.

.. image:: /images/Parametres_SpectralGate.png

Sliders under the graph:
    - Gate Threshold: value (in decibels) at which the gate becomes active.
    - Gate Attenuation: Gain (in decibels) of the gated signal.
    - Dry/Wet: Mix between the original signal and the delayed signals.

Dropdown menus and toggles:
    - FFT Size: Window size of the FFT (in samples - 16, 32, 64, 128, 256, 512, 1024, 2048, 4096 or 8192).
    - FFT Envelope: Envelope type for the FFT (rectangular, Hanning, Hamming, Bartlett, Blackmann 3, 4 or 7, Tuckey or sine).
    - FFT Overlaps: Number of FFT overlaps (1, 2, 4, 8 or 16).
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.