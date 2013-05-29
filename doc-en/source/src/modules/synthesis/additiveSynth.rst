AdditiveSynth
==============

Additive synthesis module.

.. image:: /images/Parametres_AddSynth.png

Sliders under the graph:
    - Base Frequency: Base pitch of the synthesis (in Hertz).
    - Partials Spread: Spread factor that determines the distance between the partials.
    - Partials Freq Rand Amp: Amplitude of the jitter applied to the partials pitch.
    - Partials Freq Rand Speed: Frequency of the jitter applied to the partials pitch.
    - Partials Amp Rand Amp: Amplitude of the jitter applied to the jitter amplitude.
    - Partials Amp Rand Speed: Frequency of the jitter applied to the partials amplitude.
    - Amplitude Factor: Spread of amplitude between the partials.

Dropdown menus and toggles:
    - # of Partials: Number of partials present in the generated signal (5, 10, 20, 40, 80, 160, 320 or 640).
    - Wave Shape: Shape of the soundwaves used for the synthesis (sine, sawtooth, square, complex 1, 2 or 3 or custom).
    - Custom Wave: Click in the box to enter amplitude values that will create the shape of a custom wave.
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
