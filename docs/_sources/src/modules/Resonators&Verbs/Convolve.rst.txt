Convolve : Circular convolution filtering module
================================================

Description
------------

Circular convolution filter where the filter kernel is extract from a soundfile segments.

Circular convolution is very expensive to compute, so the impulse response must be kept 
very short to run in real time.

Sliders
--------

    **Impulse index 1** : 
        Position of the first impulse response in the soundfile (mouse up)
    **Impulse index 2** : 
        Position of the second impulse response in the soundfile (mouse up)
    **Imp 1 <--> Imp 2** : 
        Morphing between the two impulse responses
    **Dry / Wet** : 
        Mix between the original signal and the convoluted signal

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Size** : 
        Buffer size of the convolution
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    