BinModulator : Frequency independent amplitude and frequency modulations
========================================================================

Description
------------

This module modulates both the amplitude and the frequency of 
each bin from a phase vocoder analysis with an independent 
oscillator. Power series are used to compute modulating 
oscillator frequencies.

Sliders
--------

    **AM Base Freq** : 
        Base amplitude modulation frequency, in Hertz.
    **AM Spread** : 
        Spreading factor for AM oscillator frequencies. 0 means every 
        oscillator has the same frequency.
    **FM Base Freq** : 
        Base frequency modulation frequency, in Hertz.
    **FM Spread** : 
        Spreading factor for FM oscillator frequencies. 0 means every 
        oscillator has the same frequency.
    **FM Depth** : 
        Amplitude of the modulating oscillators.
    **Dry / Wet** : 
        Mix between the original signal and the delayed signals

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Reset** : 
        On mouse down, this button reset the phase of all 
        bin's oscillators to 0. 
    **Routing** : 
        Path of the sound
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
    
    