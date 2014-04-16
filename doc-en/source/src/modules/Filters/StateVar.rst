StateVar : State Variable Filter
================================

Description
------------

This module implements lowpass, bandpass and highpass filters in parallel
and allow the user to interpolate on an axis lp -> bp -> hp.

Sliders
--------

    **Cutoff/Center Freq** : 
            Cutoff frequency for lp and hp (center freq for bp)
    **Filter Q** :
            Q factor (inverse of bandwidth) of the filter
    **Type (lp->bp->hp)** : 
            Interpolating factor between filters
    **Dry / Wet** : 
            Mix between the original and the filtered signals

Graph Only
-----------

    **Overall Amplitude** : 
            The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
            Number of voices played simultaneously (polyphony), 
            only available at initialization time
    **Polyphony Chords** : 
            Pitch interval between voices (chords), 
            only available at initialization time

    