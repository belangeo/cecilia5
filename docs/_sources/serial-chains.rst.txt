Audio routing graphs
====================

The Add Module button opens the categorized module menu and adds a node to the
current session. The first module becomes a source on the left and connects directly to the
Output node on the right. Additional modules start unconnected. First-only
modules become additional sources; processing modules can also become sources
using the node context menu.

File / Open Random, File / Modules, and File / Open Recent open a single module
in a fresh session. Cecilia offers to save unsaved changes before closing the
current session. Cancel keeps the current session. Use New Session for an empty
graph. Reload Module reloads the selected module and retains matching settings.

Editing connections
-------------------

The Editor / Routing selector switches between the selected module's editor and
the routing canvas. Double-click a node or choose Edit to edit its graph,
sliders, presets, toggles, and menus. Instances of the same module retain
independent settings and automation.

Click a module's output port on its right edge, move to another module's input
port on its left edge, and click again to connect. No mouse button needs to be
held. Press Escape, right-click, or click empty canvas space to cancel. A module output can feed several modules, and several
outputs can feed the same module. Connect any module output to the Output node
to include it in the final mix. Direct source-to-Output connections are allowed,
including alongside processed branches. The graph supports multiple independent sources and does not allow feedback,
self-connections, duplicate cables, or connections into a source.

Click a cable and press Delete or Backspace to disconnect it. Drag a processing
node's body to move it; its position is saved with the session. Source and Output
positions are fixed at the left and right. Sources are stacked in the first
column, separated from processing nodes by a light vertical line. Remove deletes
a module and its cables without reconnecting its neighbors. Keep at least one
source while processing modules remain.

Only nodes on complete paths from any source to Output are rendered. Other nodes are
marked Inactive and their required input files are not checked for playback.
Connect at least one complete path before playing or rendering.

Mixing and controls
-------------------

A single incoming connection uses unity gain. When two or more connections feed
a module or Output, each incoming signal is multiplied by 0.707 before summing.
This factor stays the same for three or more inputs; it is not an average.
Use module controls and the master output gain to manage the resulting levels.
Shared effects and output gain process the final Output mix.

Each source has independent sound-file or microphone controls. Clicking a source
selects it as the reference source and shows its controls under INPUT. Editing a
processing module keeps the last reference source selected; the corresponding
source node is marked Selected. The node context menu offers Use as source for
processing nodes with no incoming cables, and Use as processor for compatible
sources when another source remains. You can also drag a compatible source
across the vertical divider into the processing area to turn it into an effect
node. Its outgoing connections are preserved. Source-only modules and the last
remaining source stay in the source column.

Processing nodes receive their connected upstream mix, so their primary sampler's
file, pitch, and looping controls are unavailable. Auxiliary files, such as
convolution impulse responses, appear below the edited module's preset panel.
OUTPUT duration and channels apply to the whole graph. All sources share one
transport and timeline and start together. Shared effects and master gain apply
to the final Output mix, independently of the selected source.

Switching editors or views during playback does not restart audio. Stop playback
or rendering before changing connections, moving or removing nodes, adding or
replacing modules, reloading, loading presets, or opening a session. Add Module
and routing edits are disabled while audio runs and become available again when
playback or batch rendering stops.

Presets, batches, and sessions
-----------------------------

Module presets affect only the selected module in a multi-module session; their
saved input, output settings, and effects do not replace session settings. With
one module, presets retain their original behavior. Batch Processing on Preset
Sequence uses the presets of the module currently selected in edit mode and
renders the routed graph for each preset. Batch Processing on Sound Folder
cycles the reference source through its sound folder while other sources keep
their inputs. Use Sound Duration on Batch Processing takes the duration of the
reference source sound for both batch modes, even when a processing module is
being edited.

Save Session preserves modules, source roles, the reference source, connections,
node positions, output connections, and settings in a ``.c5chain`` file. Settings are stored directly, rather than
as references to preset files, and module and asset paths are relative where
possible. Version 1 sessions open as equivalent serial graphs and version 2 graphs retain
their single source and routing. New saves use version 3, which older Cecilia
versions cannot read. Module sources and
required audio assets must remain available. A failed load leaves the current
session available. Open Recent Session lists the ten most recently opened or
saved sessions, separately from recent modules.

Compatible modules
------------------

Modules with a single ``csampler`` and no other input widgets can automatically
accept upstream audio. Modules whose primary input is a sound table, synthesis
modules without stream inputs, and other first-only modules can occupy the
source column. Adding a first-only module creates another independent source
without replacing existing sources or their connections. Reload Module replaces
only the edited module and preserves its source role and outgoing connections.

Authors can declare a primary stream and auxiliary file assets at module level::

    Chain = {"primary_input": "snd", "auxiliary_inputs": ["impulse"]}

The primary input must be a ``csampler`` used through ``addSampler``. Auxiliary
inputs must be ``cfilein`` widgets used as file assets. Every input widget must be
accounted for in the declaration. Downstream ``addSampler`` returns the connected
upstream mix, with its explicit ``amp`` multiplier, without adding physical-input
gain. ``getSamplerDur`` returns the session duration for that input. Multiple
stream inputs, direct hardware input, and table-only processing are not adapted
automatically for downstream use.
