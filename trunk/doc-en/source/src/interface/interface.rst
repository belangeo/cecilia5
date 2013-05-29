Interface
=============

In Cecilia5, all built-in modules come with a graphical interface, which is divided in different sections, common to all treatment and synthesis modules of the software: the transports bar, the In/Out, Pre-processing and Post-Processing tabs, the presets section, the graphic and the sliders that control the parameters of the module. All these sections will be described in this chapter.


.. image:: /images/Interface-graphique.png

Transport panel
-----------------

The transport section contains a window that indicates the current time of playback of the output sound file and two buttons: "Play/stop" and "Record".

.. image:: /images/Transport.png

 
-"Play/stop" button: Press to launch playback of the output sound file.  Click again to stop.


-"Record" button: Press to record output to a file.  No sound will be heard.  A "Save audio file as ..." dialog window will appear. By default, all sound files will be recorded in AIFF format and will be named by the name of the module (with the extension .aif).

.. image:: /images/SaveAudioFileAs.png

Input - Output
----------------

The In/Out tab, which is situated below the transports bar, features different control options related to the input/output sound files.

Input
********

.. image:: /images/Input.png

This section is only provided with the treatment modules. To import an audio file from hard drive, click on the "Audio" menu and select your file from the standard dialog. Only WAV and AIFF files will be accepted by the module. All audio files located in the same folder as the chosen file will be loaded in the popup menu.  

In the Input section, these icons are shortcuts to some features of Cecilia5:

.. image:: /images/Icones-In.png


Click on the loudspeaker to listen to the imported sound file or to the output sound file with another sound player or sequencer application. If no application has been selected in the Preferences yet, a dialog window will appear.  Please select a sound player in the Application folder.

.. image:: /images/ChooseSoundfilePlayer.png

Click on the scissors to edit the sound file in an editor application. If no application has been selected in the Preferences yet, a dialog window will appear.  Please select a sound editor in the Application folder. 

.. image:: /images/ChooseSoundfileEditor.png


Click on the triangle to open the "Sound source controls" dialog window for more options on the source sound file:

.. image:: /images/SourceSoundControls.png

In this window, as in the main Input section, click on the loudspeaker to play the source sound file or on the scissors to edit the source sound file with an external application. Click on the icon clock to set the duration of the output sound to the source sound duration.

.. image:: /images/Icones-SSC.png

The "Audio Offset" slider sets the offset time into the source sound (start position in the source sound file).  In the "Loop" menu, there are four options available: Off (no loop), Forward (forward loop), Backward (backward loop) and Back & Forth (forward and backward loop in alternance).

If the "Start from loop" box is checked, Cecilia will start reading the sound file from the loop point.  If the "Xfade" box is checked, Cecilia will make a crossfade between loops.

The "Loop In" slider sets the start position of the loop in the source soundfile.

The "Loop Time" slider sets the duration (in seconds) of the loop.

The "Loop X" slider sets the duration of the crossfade between two loops (percentage of the total loop time).

The "Gain" slider sets the intensity (in decibels) of the sound source.

Move the "Transpo" slider to transpose (direct transposition) the original sound file.  The duration of the sound file is affected by the transposition, as while reading a tape at different speeds.

All settings can be controlled through automations.  To record an automation, click on the red circle on the left side of the slider and press play (on the transport bar) to read the sound file.  All slider variations will then be recorded in real time in the graphic of the interface.  Afterwards, you can modify the automation curve in the graphic (see the corresponding following section).  Then, click on the green triangle to enable automation while playing the sound file.

Output
**********


.. image:: /images/Output.png

This section contains all options for recording the audio file on hard drive. Click on the "file name" label to choose the name, format and repertory of the audio file to record.
Then, two sliders allows you to choose the duration (in seconds) and the gain (in decibels) of the output file.  Enter the number of audio channels in the "Channels" bar.  The "Peak" bar indicates the maximum intensity of the audio signal.

In the Output section, these icons are shortcuts to some features of Cecilia5:

.. image:: /images/Icones-Out.png

In the Output section, as in the Input section, click on the loudspeaker to play the source sound file or on the scissors to edit the source sound file with an external application (see above). Click on the arrows to use the output sound file as the source sound.
