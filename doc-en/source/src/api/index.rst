Cecilia5 API documentation
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
