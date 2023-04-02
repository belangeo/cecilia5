BaseModule API
===============

Here are the explanations about the processing class under every cecilia module.

Declaration of the module's class
----------------------------------

Every module must contain a class named 'Module', where the audio processing
will be developed. In order to work properly inside the environment, this 
class must inherit from the `BaseModule` class, defined inside the Cecilia 
source code. The BaseModule's internals create all links between the interface 
and the module's processing. A Cecilia module must be declared like this:

.. code::

    class Module(BaseModule):
        '''
        Module's documentation
        '''
        def __init__(self):
            BaseModule.__init__(self)
            ### Here comes the processing chain...


The module file will be executed in an environment where both `BaseModule` and
`pyo` are already available. No need to import anything specific to define the
audio process of the module.

Module's output
----------------

The last object of the processing chain (ie the one producing the output sound) 
must be called 'self.out'. The audio server gets the sound from this variable 
and sends it to the Post-Processing plugins and from there, to the soundcard.

Here is an example of a typical output variable, where 'self.snd' is the dry 
sound and 'self.dsp' is the processed sound. 'self.drywet' is a mixing slider 
and 'self.env' is the overall gain from a grapher's line:

.. code::

    self.out = Interp(self.snd, self.dsp, self.drywet, mul=self.env)


Module's documentation
-----------------------

The class should provide a __doc__ string giving relevant information about
the processing implemented by the module. The user can show the documentation
by selecting 'Help Menu' ---> 'Show Module Info'. Here is an example:

.. code::

        '''
        "Convolution brickwall lowpass/highpass/bandpass/bandstop filter"
        
        Description
    
        Convolution filter with a user-defined length sinc kernel. This
        kind of filters are very CPU expensive but can give quite good
        stopband attenuation.
        
        Sliders
    
            # Cutoff Frequency :
                Cutoff frequency, in Hz, of the filter.
            # Bandwidth :
                Bandwith, in Hz, of the filter. 
                Used only by bandpass and pnadstop filters.
            # Filter Order :
                Number of points of the filter kernel. A longer kernel means
                a sharper attenuation (and a higher CPU cost). This value is
                only available at initialization time.
    
        Graph Only
        
            # Overall Amplitude : 
                The amplitude curve applied on the total duration of the performance
    
        Popups & Toggles
    
            # Filter Type :
                Type of the filter (lowpass, highpass, bandpass, bandstop)
            # Balance :
                Compression mode. Off, balanced with a fixed signal
                or balanced with the input source.
            # Polyphony Voices : 
                Number of voices played simultaneously (polyphony), 
                only available at initialization time
            # Polyphony Spread : 
                Pitch variation between voices (chorus), 
                only available at initialization time
    
        '''


Public Attributes
------------------

These are the attributes, defined in the BaseModule class, available to the 
user to help in the design of his custom modules.

**self.sr** 
    Cecilia's current sampling rate.
**self.nchnls** 
    Cecilia's current number of channels.
**self.totalTime** 
    Cecilia's current duration.
**self.filepath**
    Path to the directory where is saved the current cecilia file.
**self.number_of_voices** 
    Number of voices from the cpoly widget.
**self.polyphony_spread** 
    List of transposition factors from the cpoly widget.
**self.polyphony_scaling** 
    Amplitude value according to polyphony number of voices.

Public Methods
---------------

These are the methods, defined in the BaseModule class, available to the 
user to help in the design of his custom modules.

**self.addFilein(name)** 
    Creates a SndTable object from the name of a cfilein widget.
**self.addSampler(name, pitch, amp)** 
    Creates a sampler/looper from the name of a csampler widget.
**self.getSamplerDur(name)** 
    Returns the duration of the sound used by the sampler `name`. 
**self.duplicate(seq, num)** 
    Duplicates elements in a sequence according to the `num` parameter.
**self.setGlobalSeed(x)** 
    Sets the Server's global seed used by objects from the random family.

Template
---------

This template, saved in a file with the extension '.c5', created a basic 
module where a sound can be load in a sampler for reading, with optional 
polyphonic playback. A graph envelope modulates the amplitude of the sound 
over the performance duration.
 
.. code::

    class Module(BaseModule):
        '''
        Module's documentation
        '''
        def __init__(self):
            BaseModule.__init__(self)
            ### get the sound from a sampler/looper
            self.snd = self.addSampler('snd')
            ### mix the channels and apply the envelope from the graph
            self.out = Mix(self.snd, voices=self.nchnls, mul=self.env)
    
    Interface = [
        csampler(name='snd'),
        cgraph(name='env', label='Amplitude', func=[(0,1),(1,1)], col='blue1'),
        cpoly()
    ]


