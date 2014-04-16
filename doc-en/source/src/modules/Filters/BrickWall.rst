BrickWall : Convolution brickwall lowpass/highpass/bandpass/bandstop filter
===========================================================================

Description
------------

Convolution filter with a user-defined length sinc kernel. This
kind of filters are very CPU expensive but can give quite good
stopband attenuation.

Sliders
--------

    **Cutoff Frequency** :
        Cutoff frequency, in Hz, of the filter.
    **Bandwidth** :
        Bandwith, in Hz, of the filter. 
        Used only by bandpass and pnadstop filters.
    **Filter Order** :
        Number of points of the filter kernel. A longer kernel means
        a sharper attenuation (and a higher CPU cost). This value is
        only available at initialization time.

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Filter Type** :
        Type of the filter (lowpass, highpass, bandpass, bandstop)
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    