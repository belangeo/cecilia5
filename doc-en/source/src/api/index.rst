Cecilia5 API Documentation
=============================

What is a Cecilia module
-------------------------

A Cecilia module is a python file (with the extension 'C5', associated to
the application) containing a class named `Module`, within which the audio
processing chain is developed, and a list called `Interface`, telling the
software what are the graphical controls necessary for the proper operation
of the module. the file can then be loaded by the application to apply the
process on different audio signals, whether coming from sound files or from
the microphone input. Processes used to manipulate the audio signal must be
written with the Python's dedicated signal processing module 'pyo'.

Serial module chains
---------------------

A session connects independently editable module instances in serial order.
Each stage's self.out feeds the next stage's primary csampler; only the first
stage reads the INPUT selection. OUTPUT duration, channels, effects, and gain
are shared. See BaseModule_API for Chain metadata, compatible input types,
auxiliary file assets, and downstream addSampler/getSamplerDur behavior.

The grid's Add module menu appends a stage. File / Open Random, File / Modules,
and File / Open Recent open a single module in a fresh session after confirmation.
Save Session preserves the chain in a .c5chain file; .c5 files define modules.

API Documentation Structure
----------------------------

This API is divided into two parts: firstly, there is the description of the
parent class, named `BaseModule`, from which every module must inherit. This
class implements a lot of features that ease the creation of a dsp chain.
Then, the various available GUI elements (widgets) are presented.


.. toctree::
   :maxdepth: 2

   BaseModule/index
   Interface/index
