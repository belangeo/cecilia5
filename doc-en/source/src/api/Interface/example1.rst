Example 1
==============================================

.. code::

    # This example shows how to use the sampler to loop any soundfile from the disk.
    # A state-variable filter is then applied on the looped sound. 
    
    class Module(BaseModule):
        """
        "State Variable Filter"
        
        Description
    
        This module implements lowpass, bandpass and highpass filters in parallel
        and allow the user to interpolate on an axis lp -> bp -> hp.
        
        Sliders
        
            # Cutoff/Center Freq : 
                    Cutoff frequency for lp and hp (center freq for bp)
            # Filter Q : 
                    Q factor (inverse of bandwidth) of the filter
            # Type (lp->bp->hp) : 
                    Interpolating factor between filters
            # Dry / Wet : 
                    Mix between the original and the filtered signals
    
        Graph Only
        
            # Overall Amplitude : 
                    The amplitude curve applied on the total duration of the performance
        
        Popups & Toggles
        
            # Polyphony Voices : 
                    Number of voices played simultaneously (polyphony), 
                    only available at initialization time
            # Polyphony Chords : 
                    Pitch interval between voices (chords), 
                    only available at initialization time
    
        """
        def __init__(self):
            BaseModule.__init__(self)
            self.snd = self.addSampler("snd")
            self.dsp = SVF(self.snd, self.freq, self.q, self.type)
            self.out = Interp(self.snd, self.dsp, self.drywet, mul=self.env)
    
    Interface = [
        csampler(name="snd"),
        cgraph(name="env", label="Overall Amplitude", func=[(0,1),(1,1)], col="blue1"),
        cslider(name="freq", label="Cutoff/Center Freq", min=20, max=20000, init=1000, 
                rel="log", unit="Hz", col="green1"),
        cslider(name="q", label="Filter Q", min=0.5, max=25, init=1, rel="log", 
                unit="x", col="green2"),
        cslider(name="type", label="Type (lp->bp->hp)", min=0, max=1, init=0.5, 
                rel="lin", unit="x", col="green3"),
        cslider(name="drywet", label="Dry / Wet", min=0, max=1, init=1, rel="lin", 
                unit="x", col="blue1"),
        cpoly()
    ]
    
