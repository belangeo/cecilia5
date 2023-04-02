UpDistoRes : Arctangent distortion module with upsampling and resonant lowpass filter
=====================================================================================

Description
-----------

This module applies an arctangent distortion on an upsampled signal and pass
the result through a 24dB/oct lowpass resonant filter.

Sliders
-------

    **Pre-Filter Freq** : 
        Center frequency of the filter applied before distortion
    **Pre-Filter Q** : 
        Q factor of the filter applied before distortion
    **Pre-Gain** : 
        Gain control applied before the distortion
    **Drive** : 
        Amount of distortion applied on the signal
    **Lowpass Freq** : 
        Cutoff frequency of the 24dB/oct lowpass filter applied after distortion
    **Lowpass Res** : 
        Resonance factor of the 24dB/oct lowpass filter applied after distortion
    **Dry / Wet** : 
        Mix between the original signal and the degraded signal

Graph Only
----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
----------------

    **Pre Filter Type** : 
        Type of filter used before distortion
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Upsampling** :
        The resampling factor. The process will be applied with a virtual
        sampling rate of the current sampling rate times this factor.
    **Interpolation** :
        Defines the FIR lowpass kernel length used for interpolation and decimation.
        The kernel length will be the upsampling factor times this value. 
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time
