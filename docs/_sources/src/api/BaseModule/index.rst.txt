BaseModule API
===============

Here are the explanations about the processing class under every cecilia5 module.

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
and feeds it to the next stage in a serial module chain. Only the final stage
is sent through the shared Post-Processing plugins and output gain. Playback,
recording, offline bounce, metering, and spectrum use this final output path.
Do not call out() on stage objects; assign the stage signal to self.out.

Here is an example of a typical output variable, where 'self.snd' is the dry
sound and 'self.dsp' is the processed sound. 'self.drywet' is a mixing slider
and 'self.env' is the overall gain from a grapher's line:

.. code::

    self.out = Interp(self.snd, self.dsp, self.drywet, mul=self.env)


Serial module chains
---------------------

A session can contain several ordered instances of the same or different modules.
Each instance has its own execution namespace, controls, automation graphs,
preset selection, and file assets. Module code must use its BaseModule methods
and control attributes rather than looking up the currently selected editor.
Changing the editor selection does not change audio routing.

Only the first stage uses the INPUT section's soundfile or external audio.
Each later stage receives the previous stage's self.out through its primary
csampler. All stages use the shared OUTPUT duration and channel count;
self.totalTime is the session duration, including for downstream automation.
With one module, sampler and preset behavior remains unchanged.

Declare routing metadata at module level, alongside Module and Interface:

.. code::

    Chain = {"primary_input": "snd", "auxiliary_inputs": ["impulse"]}


The primary_input name must identify a csampler used with self.addSampler().
Each auxiliary_inputs name must identify a cfilein used with self.addFilein(),
for example an impulse-response table. The declaration must account for every
csampler and cfilein in Interface. Use an empty auxiliary_inputs list when the
module has no auxiliary files. Auxiliary file selectors belong to the instance
and remain available when the module is downstream.

Without Chain metadata, Cecilia infers compatibility only for modules with
exactly one csampler and no other input widgets. Modules with ambiguous inputs
need explicit metadata. Primary sound-table processors and generators without
a stream input can run first or alone; they cannot be placed downstream.
Tables are not automatically rendered from upstream audio. Serial routing has
no branching, bypass, or per-stage output gain.

For a downstream primary sampler, self.addSampler(name, pitch, amp) returns the
upstream signal multiplied by amp. The pitch argument is ignored; file seeking,
looping, sampler gain, pitch, and polyphonic sampler playback are unavailable.
Module processing controls and module-defined polyphony remain usable.
self.getSamplerDur(name) returns the shared session duration for that input.
First-stage samplers retain their normal soundfile and live-input behavior.

In a multi-module session, loading a module preset changes only that instance's
controls, graphs, and auxiliary files. Saved primary-input and shared output,
duration, channels, gain, and effects settings are ignored. Save Session stores
the complete chain and settings in a .c5chain file; it does not embed module
source or audio assets. A .c5 file continues to define a single module.

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
    Shared OUTPUT duration in seconds, used by every stage and its automation.
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
    Creates a sampler/looper, or returns upstream audio for a downstream primary input.
**self.getSamplerDur(name)**
    Returns the source sound duration, or session duration for downstream/live input.
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


