SpectralWarper : Phase Vocoder buffer and playback with transposition
=====================================================================

Description
------------

This module pre-analyses the input sound and keeps the
phase vocoder frames in a buffer for the playback. User
has control on playback position and transposition.

Sliders
--------

    **Position** : 
        Normalized position (0 -> 1) inside the recorded PV buffer.
        Buffer length is the same as the sound duration.
    **Transposition** : 
        Pitch of the playback sound.

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **FFT Size** : 
        Size, in samples, of the FFT
    **FFT Envelope** : 
        Windowing shape of the FFT
    **FFT Overlaps** : 
        Number of FFT overlaping analysis
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    