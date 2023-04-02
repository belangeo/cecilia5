MultiBandBeatMaker : Multi-band algorithmic beatmaker
=====================================================

Description
------------

MultiBandBeatMaker uses four algorithmic beat generators to play
spectral separated chunks of a sound. 

Sliders
--------

    **Frequency Splitter** : 
        Split points for multi-band processing
    **Num of Taps** : 
        Number of taps in a measure
    **Tempo** : 
        Speed of taps
    **Tap Length** : 
        Length of taps
    **Beat 1 Index** : 
        Soundfile index of the first beat
    **Beat 2 Index** : 
        Soundfile index of the second beat
    **Beat 3 Index** : 
        Soundfile index of the third beat
    **Beat 4 Index** : 
        Soundfile index of the fourth beat
    **Beat 1 Distribution** : 
        Repartition of taps for the first beat (100% weak --> 100% down)
    **Beat 2 Distribution** : 
        Repartition of taps for the second beat (100% weak --> 100% down)
    **Beat 3 Distribution** : 
        Repartition of taps for the third beat (100% weak --> 100% down)
    **Beat 4 Distribution** : 
        Repartition of taps for the fourth beat (100% weak --> 100% down)
    **Beat 1 Gain** : 
        Gain of the first beat
    **Beat 2 Gain** : 
        Gain of the second beat
    **Beat 3 Gain** : 
        Gain of the third beat
    **Beat 4 Gain** : 
        Gain of the fourth beat
    **Global Seed** : 
        Seed value for the algorithmic beats, using the same seed with 
        the same distributions will yield the exact same beats
    
Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance
    **Beat 1 ADSR** : 
        Envelope of taps for the first beat in breakpoint fashion
    **Beat 2 ADSR** : 
        Envelope of taps for the second beat in breakpoint fashion
    **Beat 3 ADSR** : 
        Envelope of taps for the third beat in breakpoint fashion
    **Beat 4 ADSR** : 
        Envelope of taps for the fourth beat in breakpoint fashion

Popups & Toggles
-----------------

    **Polyphony per Voice** :
        The number of streams used for each voice's polpyhony. High values
        allow more overlaps but are more CPU expensive, only available at 
        initialization time.

    