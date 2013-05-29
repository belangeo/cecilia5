Menubar
==============

This is a short description of the menus that the user will find in the upper part of the screen.

Cecilia5 Menu
-----------------

The "Cecilia5" menu ("Python" if run from sources) gives access to the Preferences window. There are also commands to hide the graphical interface (see "Hide Python") or the other applications (see "Hide Others"); the user can also quit Cecilia5 (see "Quit Python").

.. image:: /images/Menu_python.png

File Menu
-----------------

.. image:: /images/Menu_file.png

The "File" menu gives access to the following commands:
    - Open: Opens a Cecilia5 file (with the extension .c5) saved by the user.
    - Open Random: Chooses a random Cecilia5 module and opens it.
    - Open Module: In this menu, the user can choose a Cecilia5 module. The modules fall in eight categories. For more information on modules, please see chapters 4 to 11.

        .. image:: /images/ModulesCategories.png

    - Open Recent: Opens a Cecilia5 file which has been recently modified and saved by the user.
    - Save and Save as: Saves the module on which the user is currently working. The saved file will be in Cecilia5 (.c5) format.
    - Open Module as Text: Opens a text file that contains the source code of the module, for more information on it or if the user wishes to modify it. (For more information on modifications on those files, please see chapter 12.) If no text editor has been selected in the Preferences yet, a dialog window will appear to let the user choose one.

        .. image:: /images/ChooseTextEditor.png

    - Reload module: Reloads the module from the source code. The user should execute this command if the module source code has been modified.

Edit Menu
-----------------

The "Edit" menu gives access to the Undo, Redo, Copy and Paste commands. These commands will only have an effect on the graph and are not related to the other parameters of the module.  Check the "Remember input sound" if you wish that Cecilia5 remembers the input sound you chose for each new module opening.

.. image:: /images/Menu_edit.png

Action Menu
-----------------

In the "Action" menu, the commands "Play/Stop" and "Bounce to Disk" are equivalent to the "Play" and "Record" buttons of the transport bar.

.. image:: /images/Menu_Action.png

The command "Batch Processing on Sound Folder" applies the module's current settings to all sound files present in the folder that contains the input sound file.  The command "Batch Processing on Preset Sequence" applies all saved presets of the module to the chosen input sound file.  These two commands processes more than one sound file at a time. Before executing one of these commands, Cecilia5 will ask the user to enter a suffix to identify the new created sound files.

.. image:: /images/ChooseFilenameSuffix.png

The "Use MIDI" indicates if Cecilia5 has already found a MIDI device.

Window Menu
-----------------

In the "Window" menu, the user can minimize the graphical interface window (see "Minimize"), zoom in this window (see "Zoom" - click once to zoom in and twice to zoom out) and bring all Cecilia5 windows to fromt (see "Bring All to Front").  The command "Eh Oh Mario!" changes a little something in the graphical interface that could make the user smile. The command "interface - nameofthemodule.c5" is part of the system's properties that makes all open windows of the application available to the user.

.. image:: /images/Menu_Window.png

Help Menu
-----------------

In the "Help" menu, the user can search for a command in the different menus; please enter a key word in the search box.  Click on "Show module info" to access a short description of the module that is currently used.  Click on "Show API Documentation" to access the documentation related to Cecilia5's programming interface.  This documentation contains all classes and methods declarations and information on all menus and commands related to the currently used module. For more information on Cecilia5's API, please see chapter 12.

.. image:: /images/Menu_Help.png

List of shortcuts:
    - cmd-h: Hide Cecilia5' window
    - alt-cmd-h: Hide the other applications' windows
    - cmd-o: Open a Cecilia5 file
    - shift-cmd-o: Open a random Cecilia5 file
    - cmd s: Save the current file
    - shift-cmd-s: Save the current file as...
    - cmd-e: Open the text file that contains the source code of the module
    - cmd-r: Reload module with all saved modifications in the source code
    - cmd-c: Copy (graph only)
    - cmd-v: Paste (graph only)
    - cmd-z: Undo (graph only)
    - shift-cmd-z: Redo (graph only)
    - cmd-.: Play/Stop
    - cmd-b: Bounce to disk ("Record" button)
    - cmd-m: Minimize window
    - shift-cmd-e: Eh Oh Mario!
    - cmd-i: Open module documentation
    - cmd-d: Open API Documentation
