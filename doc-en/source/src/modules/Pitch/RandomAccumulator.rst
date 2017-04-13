Variable speed recording accumulator module
===========================================

Description
-----------

This module records the sound from the sampler in a table at a varying
position and speed. The feedback parameter indicates how much of the
previous recording at the current position is kept back in the table.
The recorded table is read in loop at the normal speed, with possibility
to activate a 180 degrees out-of-phase overlap.

Sliders
-------

    **Pre-Filter Freq** : 
        Center frequency of the filter applied before the recording
    **Pre-Filter Q** : 
        Q factor of the filter applied before the recording
    **Accum Feedback** :
        The amount of previous signal in the table that is kept back,
        mixed with the new recording.
    **Record Time Rand** :
        The time it took to the recording head to reach the new position
        target in the table. The target is chosen randomly between 0 and 
        the end of the table. If the time is longer than the distance to 
        run, the signal will be write slowly, so the playback (at regular 
        speed) will give an upward transposition. When the target is reached, 
        a new target and a new recording duration are chosen.
    **Buffer Length** :
        The size of the table in seconds. This parameter is updated only
        at the start of the performance.
    **Global Seed** :
        Root of stochatic generators. If 0, a new value is chosen randomly each
        time the performance starts. Otherwise, the same root is used every 
        performance, making the generated sequences the same every time.

Graph Only
----------

    **Overall Amplitude** : 
        The amplitude curve applied on the total duration of the performance
    **Recording Envelope** :
        The envelope applied to each recording segment

Popups & Toggles
----------------

    **Pre-Filter Type** : 
        Type of filter used before the recording
    **Overlapped** :
        If "On", a second player, 180 degrees out-of-phase, will read the 
        recorded buffer. The signals of both players are summed and sent to 
        the output
    **Polyphony Voices** : 
        Number of voices played simultaneously (polyphony), 
        only available at initialization time
    **Polyphony Spread** : 
        Pitch variation between voices (chorus), 
        only available at initialization time
