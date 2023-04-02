csampler : creates a popup menu to load a soundfile in a sampler
================================================================

Initline
---------

.. code::
    
    csampler(name='sampler', label='Audio', help='')
    
Description
------------

This menu allows the user to choose a soundfile for processing in the 
module. More than one csampler can be defined in a module. They will 
appear under the input label in the left side panel of the main window, 
in the order they have been defined. When the user chooses a sound using 
the interface, Cecilia will scan the whole folder for soundfiles. A 
submenu containing all soundfiles present in the folder will allow a 
quicker access to them later on. Loop points, pitch and amplitude 
parameters of the loaded soundfile can be controlled by the csampler 
window that drops when clicking the triangle just besides the name of 
the sound.

A sampler returns an audio variable containing Cecilia's number of 
output channels regardless of the number of channels in the soundfile. 
A distribution algorithm is used to assign X number of channels to Y 
number of outputs.

In the processing class, use the BaseModule's method `addSampler` to 
retrieve the audio variable containing all channels of the looped sound.


.. code::

        BaseModule.addSampler(name, pitch, amp)

For a csampler created with name='mysound', the audio variable is 
retrieved using a call like this one:


.. code::

        self.snd = self.addSampler('mysound')
  
Audio LFOs on pitch and amplitude of the looped sound can be passed 
directly to the addSampler method:


.. code::

        self.pitlf = Sine(freq=.1, mul=.25, add=1)
        self.amplf = Sine(freq=.15, mul=.5, add=.5)
        self.snd = self.addSampler('mysound', self.pitlf, self.amplf)
        
Parameters
-----------

    **name**: str
        A string passed to the parameter `name` of the BaseModule.addSampler
        method. This method returns a Mix object containing Cecilia's 
        number of channels as audio streams from a Looper object 
        controlled with the sampler window of the interface.
    **label**: str
        Label shown in the interface.
    **help**: str
        Help string shown in the sampler popup's tooltip.

    