Vocoder : Time domain vocoder effect
====================================

Description
------------

Applies the spectral envelope of a first sound to the spectrum of a second sound.

The vocoder is an analysis/synthesis system, historically used to reproduce
human speech. In the encoder, the first input (spectral envelope) is passed
through a multiband filter, each band is passed through an envelope follower,
and the control signals from the envelope followers are communicated to the
decoder. The decoder applies these (amplitude) control signals to corresponding
filters modifying the second source (exciter).

Sliders
--------

    **Base Frequency** :
        Center frequency of the first band. This is the base 
        frequency used tocompute the upper bands.
    **Frequency Spread** :
        Spreading factor for upper band frequencies. Each band is 
        `freq * pow(order, spread)`, where order is the harmonic rank of the band.
    **Q Factor** :
        Q of the filters as `center frequency / bandwidth`. Higher values 
        imply more resonance around the center frequency.
    **Time Response** :
        Time response of the envelope follower. Lower values mean smoother changes,
        while higher values mean a better time accuracy.
    **Gain** :
        Output gain of the process in dB.
    **Num of Bands** : 
        The number of bands in the filter bank. Defines the number of notches in
        the spectrum.

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
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    