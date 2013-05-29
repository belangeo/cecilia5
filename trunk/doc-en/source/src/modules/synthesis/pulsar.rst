Pulsar
==========

Pulsar synthesis module.

.. image:: /images/Parametres_Pulsar.png

Sliders under the graph:
    - Base Frequency: Base pitch of the synthesis (in Hertz).
    - Pulsar Width: Amount of silence added to one period.
    - Detune Factor: Amount of jitter applied to the pitch.
    - Detune Speed: Frequency of the jitter applied to the pitch.
    - Source index: Position in the input soundfile where the sound pulsar is taken. 

Dropdown menus and toggles:
    - Window Size: Size of the pulsar window (in samples - 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384 or 32768).
    - Window Type: Type of the pulsar window (rectangular, Hanning, Hamming, Bartlett, Blackman 3, 4 or 7, Tuckey or sine).
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
