Serial module chains
====================

The Add module button in the grid opens the same categorized menu as
File / Modules and appends the chosen module to the current chain.
File / Open Random, File / Modules, and File / Open Recent instead open a single
module in a fresh session. Cecilia asks before closing the current session and
offers to save unsaved changes; Cancel keeps the current session. Open Recent
lists recently loaded modules, including built-in modules.
Use New Session to start with an empty chain. Reload Module reloads only the
selected stage and retains matching control settings.

The Graph / Chain selector above the graph switches between the selected
module's editor and a numbered grid. Signals flow in numbered order, left to
right and then to the next row. Edit or double-click a card to edit its graph,
sliders, presets, toggles, and menus. Move earlier, Move later, and Remove change the chain.
Two instances of the same module have independent settings and automation.

INPUT always controls the first stage. Later stages receive the previous stage's
output directly, so their sampler playback, pitch, and looping controls are
unavailable. File assets such as convolution impulse responses appear below the
selected stage's preset panel. OUTPUT duration and channels apply to every stage.
The effects section and output gain process the final stage only. Opening the
effects section selects the first editor, which hosts the shared effects curves.

Switching editors or views during playback does not restart audio. Stop playback
before reordering, removing, reloading, loading presets, or opening a session.
Opening a module through the File menu stops playback before opening the new
session. The grid's Add module button is unavailable during playback.

Module presets affect only the selected stage in a multi-module session; their
saved input, output settings, and effects do not replace session settings. With
one module, presets retain their original behavior. Use Save Session to preserve
the complete chain and its settings in a ``.c5chain`` file. Session files include
settings directly, rather than references to preset files, and use relative
module and asset paths where possible. Module source files and audio assets must
remain available. A failed load leaves the existing session available.
File / Open Recent Session lists the ten most recently opened or saved sessions,
separately from recent modules. The window title includes the session filename
after opening or saving a session and retains it when switching module editors.

Compatible modules
------------------

Modules with a single ``csampler`` and no other input widgets can automatically
accept upstream audio. Modules whose primary input is a sound table remain usable
first or alone. When adding such a module, Cecilia offers to insert it first
if the existing first stage can accept upstream audio. If the current first
stage is also first-stage-only, Cecilia offers to replace it and retain the
remaining stages. Cancel keeps the chain unchanged. Modules with several stream inputs require adaptation before
they can be used downstream. Other invalid downstream placements are rejected.

Authors can declare a primary stream and auxiliary file assets at module level::

    Chain = {"primary_input": "snd", "auxiliary_inputs": ["impulse"]}

The primary input must be a ``csampler`` used through ``addSampler``. Auxiliary
inputs must be ``cfilein`` widgets used as file assets. Every input widget must be
accounted for in the declaration. Downstream ``addSampler`` returns the upstream
signal, with its explicit ``amp`` multiplier, without adding physical-input gain.
``getSamplerDur`` returns the session duration for that input. Direct hardware
input and table-only processing are not adapted automatically.
