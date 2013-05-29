DelayMod
==========

Stereo delay module with jitter control.

.. image:: /images/Parametres_DelayMod.png

Sliders under the graph:
    - Delay Left: Delay time of the first delay (in seconds).
    - Delay Right: Delay time of the second delay (in seconds).
    - AmpModDepth L: Range of the amplitude jitter for the first delay.
    - AmpModDepth R: Range of the amplitude jitter for the second delay.
    - AmpModFreq L: Speed of the amplitude jitter for the first delay.
    - AmpModFreq R: Speed of the amplitude jitter for the second delay.
    - DelModDepth L: Range of the delay time jitter for the first delay.
    - DelModDepth R: Range of the delay time jitter for the second delay.
    - DelModFreq L: Speed of the delay time jitter for the first delay.
    - DelModFreq R: Speed of the delay time jitter for the second delay.
    - Feedback: Amount of delayed signal fed back into the delay chain.
    - Dry/Wet: Mix between the original signal and the delayed signals.

Dropdown menus and toggles:
    - # of Polyphony: Number of voices played simultaneously (polyphony); only available at initialization time.
    - Polyphony Spread: Pitch variation between polyphony voices (chorus); only available at initialization time.

Graph only parameters:
    - Overall Amplitude: The amplitude curve applied on the total duration of the performance.