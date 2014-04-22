Example 2
==============================================

.. code::

    # This example shows how to load a sound in a table (RAM) in order to apply
    # non-streaming effects. Here a frequency self-modulated reader is used to
    # create new harmonics, in a way similar to waveshaping distortion.
    
    class Module(BaseModule):
        """
        "Self-modulated frequency sound looper"
        
        Description
        
        This module loads a sound in a table and apply a frequency self-modulated
        playback of the content. A Frequency self-modulation occurs when the
        output sound of the playback is used to modulate the reading pointer speed.
        That produces new harmonics in a way similar to waveshaping distortion. 
        
        Sliders
        
            # Transposition : 
                    Transposition, in cents, of the input sound
            # Feedback : 
                    Amount of self-modulation in sound playback
            # Filter Frequency : 
                    Frequency, in Hertz, of the filter
            # Filter Q : 
                    Q of the filter (inverse of the bandwidth)
        
        Graph Only
        
            # Overall Amplitude : 
                    The amplitude curve applied on the total duration of the performance
    
        Popups & Toggles
        
            # Filter Type : 
                    Type of the filter
            # Polyphony Voices : 
                    Number of voices played simultaneously (polyphony), 
                    only available at initialization time
            # Polyphony Chords : 
                    Pitch interval between voices (chords), 
                    only available at initialization time
    
        """
        def __init__(self):
            BaseModule.__init__(self)
            self.snd = self.addFilein("snd")
            self.trfactor = CentsToTranspo(self.transpo, mul=self.polyphony_spread)
            self.freq = Sig(self.trfactor, mul=self.snd.getRate())
            self.dsp = OscLoop(self.snd, self.freq, self.feed*0.0002, 
                               mul=self.polyphony_scaling * 0.5)
            self.mix = self.dsp.mix(self.nchnls)
            self.out = Biquad(self.mix, freq=self.filt_f, q=self.filt_q, 
                              type=self.filt_t_index, mul=self.env)
    
        def filt_t(self, index, value):
            self.out.type = index
    
    Interface = [
        cfilein(name="snd"),
        cgraph(name="env", label="Overall Amplitude", func=[(0,1),(1,1)], col="blue1"),
        cslider(name="transpo", label="Transposition", min=-4800, max=4800, init=0, 
                unit="cnts", col="red1"),
        cslider(name="feed", label="Feedback", min=0, max=1, init=0.25, unit="x", 
                col="purple1"),
        cslider(name="filt_f", label="Filter Frequency", min=20, max=18000, 
                init=10000, rel="log", unit="Hz", col="green1"),
        cslider(name="filt_q", label="Filter Q", min=0.5, max=25, init=1, 
                rel="log", unit="x", col="green2"),
        cpopup(name="filt_t", label="Filter Type", init="Lowpass", 
               value=["Lowpass", "Highpass", "Bandpass", "Bandreject"], col="green1"),
        cpoly()
    ]
    
