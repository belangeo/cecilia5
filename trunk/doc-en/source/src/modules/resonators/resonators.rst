Resonators
============

Module with eight resonators with jitter control.

.. image:: /images/Parametres_Resonators.png

Sliders under the graph:
    - Pitch offset: Base pitch of all the resonators (in cents).
    - Pitch Voice 1: Pitch of the first resonator compared to the original signal (in semi-tones).
    - Pitch Voice 2: Pitch of the second resonator compared to the original signal (in semi-tones).
    - Pitch Voice 3: Pitch of the third resonator compared to the original signal (in semi-tones).
    - Pitch Voice 4: Pitch of the fourth resonator compared to the original signal (in semi-tones).
    - Pitch Voice 5: Pitch of the fifth resonator compared to the original signal (in semi-tones).
    - Pitch Voice 6: Pitch of the sixth resonator compared to the original signal (in semi-tones).
    - Pitch Voice 7: Pitch of the seventh resonator compared to the original signal (in semi-tones).
    - Pitch Voice 8: Pitch of the eighth resonator compared to the original signal (in semi-tones).
    - Amp Rand Amp: Amplitude of the jitter applied to the resonators amplitude.
    - Amp Rand Speed: Frequency (in Hertz) of the jitter applied to the resonators amplitude.
    - Delay Rand Amp: Amplitude of the jitter applied to the resonators delay; this has an effect on the pitch of each resonator.
    - Delay Rand Speed: Frequency (in Hertz) of the jitter applied to the resonators delay; this has an effect on the pitch of each resonator.
    - Feedback: Amount of the resonators signal fed back into the resonators (between 0 and 1).
    - Dry/Wet: Mix between the original signal and the processed signals.

Dropdown menus and toggles:
    - Balance: Adjust the signal amplitude by comparing it with a sinusoidal wave with a fixed amplitude (see "compress") or with the amplitude of the source (see "source").
    - Voice Activation (1 to 8): Check the boxes to activate the voices (first to eighth); uncheck to mute them.
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.
