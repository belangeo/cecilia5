Run the session model tests from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

To include the integration tests, install Cecilia's normal wxPython and pyo
dependencies and run with an available desktop display:

```sh
CECILIA_GUI_TESTS=1 python3 -m unittest discover -s tests -v
```

The integration suite creates a temporary preferences profile, module fixtures,
audio files and session files. It exercises persistent editors, running pyo
processing with a manual server, offline rendering, recording, spectrum routing,
presets, shipped module declarations, and session recovery. Physical audio and
MIDI devices require a separate manual check.
