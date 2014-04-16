StochGrains : Stochastic granular synthesis with different instrument tone qualities
====================================================================================

Description
------------

This module implements a stochastic granular synthesis. Different synthesis
engine are available and the user has control over the range of every 
generation parameters and envelopes.

Sliders
--------

    **Pitch Offset** : 
        Base transposition, in semitones, applied to every grain
    **Pitch Range** : 
        Range, in semitone, over which grain pitches are chosen randomly
    **Speed Range** : 
        Range, in second, over which grain start times are chosen randomly
    **Duration Range** : 
        Range, in second, over which grain durations are chosen randomly
    **Brightness Range** : 
        Range over which grain brightness factors (high frequency power) 
        are chosen randomly
    **Detune Range** : 
        Range over which grain detune factors (frequency deviation between
        voices) are chosen randomly
    **Intensity Range** : 
        Range, in dB, over which grain amplitudes are chosen randomly
    **Pan Range** : 
        Range over which grain spatial positions are chosen randomly
    **Density** :
        Density of active grains, expressed as percent of the total generated grains
    **Global Seed** :
        Root of stochatic generators. If 0, a new value is chosen randomly each
        time the performance starts. Otherwise, the same root is used every 
        performance, making the generated sequences the same every time.

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance
    **Grain Envelope** :
        Amplitude envelope of each grain
    **Brightness Envelope** :
        Brightness (high frequency power) envelope of each grain

Popups & Toggles
-----------------

    **Synth Type** : 
        Choose between the different synthesis engines
    **Pitch Scaling** :
        Controls the possible values (as chords or scales) of the pitch generation
    **Pitch Algorithm** :
        Noise distribution used by the pitch generator
    **Speed Algorithm** :
        Noise distribution used by the speed generator
    **Duration Algorithm** :
        Noise distribution used by the duration generator
    **Intensity Algorithm** :
        Noise distribution used by the intensity generator
    **Max Num of Grains** :
        Regardless the speed generation and the duration of each grain, there will
        never be more overlapped grains than this value. The more CPU power you have,
        higher this value can be.

    