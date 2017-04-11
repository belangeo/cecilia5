Menu Options
==============

This is a short description of the menus that the user will find in the upper part of the screen.


File Menu
-----------------

The *File* menu gives access to the following commands:

- **Open**: Opens a Cecilia file (with the extension .c5) saved by the user.
- **Open Random**: Chooses a random Cecilia module and opens it.
- **Open Module**: In this menu, the user can choose a Cecilia module. The modules fall in eight categories:

    #. **Dynamics**: Modules related to waveshaping and amplitude manipulations.
    #. **Filters**: Filtering and subtractive synthesis modules.
    #. **Multiband**: Various processing applied independently to four spectral regions.
    #. **Pitch**: Modules related to playback speed and pitch manipulations.
    #. **Resonators&Verbs**: Artificial spaces generation modules.
    #. **Spectral**: Spectral streaming processing modules.
    #. **Synthesis**: Additive synthesis and particle generators.
    #. **Time**: Granulation based time-stretching and delay related modules.

- **Open Recent**: Opens a Cecilia file which has been recently modified and saved by the user.
- **Save** and **Save as**: Saves the module on which the user is currently working. The saved file is plain text file with the ".c5" extension.
- **Open Module as Text**: Opens a text file that contains the source code of the module, for more information on it or if the user 
  wishes to modify it. If no text editor has been selected in the Preferences yet, a dialog window will appear to let the user choose one.
- **Reload module**: Reloads the module from the source code. The user should execute this command if the module source code has been modified.
- **Preferences...**: Opens the preferences window (Useful to comfigure the application's behaviour for a specific operating system).
- **Quit**: Properly quit the application.

Edit Menu
-----------------

The *Edit* menu gives access to the following commnds:
    
- **Undo**: Revert the grapher to the previous state.
- **Redo**: Redo the last action undo'ed.
- **Copy**: Copy to the clipboard the list of points of the grapher's current line.
- **Paste**: Set the grapher's current line to the clipboard content (assumed to be a valid list of points). 
- **Select All Points**: Select all points in the grapher's current line.
- **Remember Input Sound**: Check this option if you wish that Cecilia5 remembers the input sound you chose for each new module opening.


Action Menu
-----------------

The *Action* menu gives access to the following commnds:

- **Play/Stop**: Start and stop the playback of the process.
- **Bounce to Disk**: Computes the process as fast as possible and writes the result in a soundfile.
- **Batch Processing on Preset Sequence**: Applies all saved presets of the module to the current input soundfile.  
- **Batch Processing on Sound Folder**: Applies the module's current settings to all soundfiles present in the folder that contains the current input soundfile.  

The two previous commands processes more than one sound file at a time. Before executing one of these commands, Cecilia will ask the user to enter a 
suffix to identify the new created soundfiles. A folder with the name of the suffix given by the user will be created in the same directory as the current 
input soundfile. If the module doesn't have an input soundfile (a synthesis module), the desktop will be used as the root directory.

- **Use Sound Duration on Folder Batch Processing**: When processing a folder of sounds in batch mode, if this option is checked, the total duration will
  be automatically adjusted to the duration of the processed sound. 
- **Show Spectrum**: Open a window showing the spectral component of the sound that is heard.

The **Use MIDI** menu item indicates if Cecilia has already found a MIDI device.


Help Menu
-----------------

The *Help* menu gives access to the following commnds:

- **Show module info**: Opens the module documentation window at the page of the module that is currently used.
- **Show API Documentation**: Opens the documentation related to Cecilia's Application Programming Interface (API).  
  This documentation contains all classes and functions declarations available to design new custom module.

List of Shortcuts
-------------------

- **Ctrl+O**: Open a Cecilia file
- **Shift+Ctrl+O**: Open a Cecilia file randomly
- **Ctrl+S**: Save the current file
- **Shift+Ctrl+S**: Save the current file as...
- **Ctrl+E**: Open the text file that contains the source code of the module
- **Ctrl+R**: Reload module with all saved modifications in the source code
- **Ctrl+,**: Open the preferences window
- **Ctrl+Q**: Quit the application
- **Ctrl+Z**: Undo (grapher only)
- **Shift+Ctrl+Z**: Redo (grapher only)
- **Ctrl+C**: Copy (grapher only)
- **Ctrl+V**: Paste (grapher only)
- **Ctrl+A**: Paste (grapher only)
- **Ctrl+.**: Play/Stop
- **Ctrl+B**: Bounce to disk
- **Shift+Ctrl+E**: Eh Oh Mario!
- **Ctrl+I**: Open module documentation
- **Ctrl+D**: Open API Documentation
