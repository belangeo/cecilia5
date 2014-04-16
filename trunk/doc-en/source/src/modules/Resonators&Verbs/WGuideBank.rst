WGuideBank : Multiple waveguide models module
=============================================

Description
------------

Resonators whose frequencies are controlled with an expansion expression.

freq[i] = BaseFreq * pow(WGExpansion, i)

Sliders
--------

    **Base Freq** : 
        Base pitch of the waveguides
    **WG Expansion** : 
        Spread between waveguides
    **WG Feedback** : 
        Length of the waveguides
    **WG Filter** : 
        Center frequency of the filter
    **Amp Deviation Amp** : 
        Amplitude of the jitter applied on the waveguides amplitude
    **Amp Deviation Speed** : 
        Frequency of the jitter applied on the waveguides amplitude
    **Freq Deviation Amp** : 
        Amplitude of the jitter applied on the waveguides pitch
    **Freq Deviation Speed** : 
        Frequency of the jitter applied on the waveguides pitch
    **Dry / Wet** : 
        Mix between the original signal and the waveguides

Graph Only
-----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance

Popups & Toggles
-----------------

    **Filter Type** : 
        Type of the post-process filter
    **Balance** :
        Compression mode. Off, balanced with a fixed signal
        or balanced with the input source.
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time

    