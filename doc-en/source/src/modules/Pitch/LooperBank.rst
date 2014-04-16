LooperBank : Sound looper bank with independant pitch and amplitude random
==========================================================================

Description
------------

Huge oscillator bank (up to 500 players) looping a soundfile stored in a waveform 
table. The frequencies and amplitudes can be modulated by two random generators 
with interpolation (each partial have a different set of randoms).

Sliders
--------

    **Transposition** : 
        Transposition of the base frequency of the process, given by the sound length.
    **Frequency Spread** : 
        Coefficient of expansion used to compute partial frequencies. If 0, all 
        partials will be at the base frequency. A value of 1 will generate integer 
        harmonics, a value of 2 will skip even harmonics and non-integer values will 
        generate different series of inharmonic frequencies.
    **Amplitude Slope** : 
        Specifies the multiplier in the series of amplitude coefficients.
    **Boost / Cut** : 
        Controls the overall amplitude.
    **Freq Rand Speed** : 
        Frequency, in cycle per second, of the frequency modulations.
    **Freq Rand Gain** : 
        Maximum frequency deviation (positive and negative) in portion of the partial 
        frequency. A value of 1 means that the frequency can drift from 0 Hz to twice 
        the partial frequency. A value of 0 deactivates the frequency deviations.
    **Amp Rand Speed** : 
        Frequency, in cycle per second, of the amplitude modulations.
    **Amp Rand Gain** : 
        Amount of amplitude deviation. 0 deactivates the amplitude modulations 
        and 1 gives full amplitude modulations.
    **Voices Per Channel** : 
        Number of loopers created for each output channel. Changes will be 
        effective on next start.

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Partials Freq Jitter** : 
        If active, a small jitter is added to the frequency of each partial. For a 
        large number of oscillators and a very small `Frequency Spread`, the
        periodicity between partial frequencies can cause very strange artefact. 
        Adding a jitter breaks the periodicity.

    