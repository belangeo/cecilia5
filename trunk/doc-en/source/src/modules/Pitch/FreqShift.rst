FreqShift : Two frequency shifters with optional cross-delay and feedback
=========================================================================

Description
------------

This module implements two frequency shifters from which the output 
sound of both one can be fed back in the input of the other. Cross-
feedback occurs after a user-defined delay of the output sounds.  

Sliders
--------

    **Filter Freq** :
        Cutoff or center frequency of the pre-filtering stage
    **Filter Q** :
        Q factor of the pre-filtering stage
    **Frequency Shift 1** : 
        Frequency shift, in Hz, of the first voice
    **Frequency Shift 2** : 
        Frequency shift, in Hz, of the second voice
    **Feedback Delay** :
        Delay time before the signal is fed back into the delay lines
    **Feedback** :
        Amount of signal fed back into the delay lines
    **Feedback Gain** :
        Amount of delayed signal cross-fed back into the frequency shifters.
        Signal from delay 1 into shifter 2 and signal from delay 2 into shifter 1.
    **Dry / Wet** : 
        Mix between the original signal and the shifted signals

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Filter Type** : 
        Type of filter
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    