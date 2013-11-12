Preferences panel
======================

The Preferences window is accessible by opening the Python menu, in the upper part of the screen:

.. image:: /images/Menu_preferences.png

Path
--------

In the "Path" tab, the user can choose a sound file player (or audio sequencer - see "Soundfile Player"), a sound file editor (see "Soundfile editor") and a text editor (see "Text Editor") to be used with Cecilia5. To choose an application, enter the path of the application in the appropriate space or click on "set" button. A dialog window will then appear for choosing the application.

The user can also enter a path in the "Preferred paths" box to save new modules (.c5 files) in a specific folder; Cecilia5 will then save these modules in the Files -> Modules menu.


.. image:: /images/Onglet_dossier.png

Audio
--------

The "Speaker" tab offers different options related to the audio parameters of Cecilia5. The user can choose an audio driver (see "Audio Driver") and the input and output devices (see "Input Device" and "Output Device").
The boxes "Sample Precision" and "Buffer Size" contains different values to set the sample precision in bits (32 or 64) and the buffer size in samples (64, 128, 256, 512, 1024 or 2048). The user can also choose the default number of audio channels (up to 36 - see "Default # of channels") and the sample rate (22 050, 44 100, 48 000, 88 200 or 96 000 Hertz - see "Sample Rate").

.. image:: /images/Onglet_haut-parleur.png

MIDI
-------

In the MIDI tab, the user can choose a MIDI driver (Port MIDI, for example - see "Midi Driver") and a MIDI controller for input (see "Input Device" - Warning! The MIDI controller should be already connected and detected by the computer to be detected by Cecilia5). For an automatic detection of your MIDI controller by Cecilia5, check the "Automatic Midi Bindings" box.

.. image:: /images/Onglet_MIDI.png

Export
----------

In the "Export" tab, the user can set the default file format (WAV, AIFF, FLAC, OGG, SD2, AU, CAF - see "File Format") and the bit depth (16, 24 or 32 bits integer, or 32 bits float) of the output sound files that will be exported to hard drive.

.. image:: /images/Onglet_export.png

Cecilia
--------

The "Cecilia5" tab provides different settings:
    - The default duration (10, 30, 60, 120, 300, 600, 1200, 2400 or 3600 seconds - see "Total time default (sec)" of the output sound file and its default fadein/fadeout duration (0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.05, 0.075, 0.1, 0.2, 0.3, 0.4 or 0.5 seconds - see "Global fadein/fadeout (sec)").
    - Check the "Use tooltips" box to see the yellow information windows appear in the graphical interface during using Cecilia5.
    - Check the "Use grapher texture" to obtain a precise grid on the graph.
    - Check the "Verbose" box to obtain more information when you work with Cecilia5 from the terminal, which can be useful for debugging.

.. image:: /images/Onglet_Cecilia5.png
