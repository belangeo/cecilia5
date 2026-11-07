SpitSideBandSynth : Two-stage split-sideband synthesis
======================================================

Description
-----------

Based on pyo's ``07_split_sideband_synthesis.py`` example, combining waveshaping,
single-sideband modulation, and frequency modulation. The first stage's odd lower
sideband drives the second stage. Modulation Frequency, the two Carrier Frequency
controls, and the two Modulation Index controls shape the resulting spectrum.

The second stage's lower and upper sidebands alternate across output channels;
mono output averages both. Polyphony transposes the modulation frequency and both
carriers. The synthesis follows the split-sideband technique described by Victor
Lazzarini, Joseph Timoney, and Thomas Lysaght (2008).

This module generates its own audio and requires no input sound file. In the
routing view, it is a source module.

Sliders
-------

.. list-table:: Parameter ranges and defaults
   :header-rows: 1
   :widths: 40 25 20 15

   * - Control
     - Range
     - Default
     - Unit
   * - Mod Freq
     - 0.01 to 2000
     - 30
     - Hz
   * - Carrier Freq 1
     - 20 to 20000
     - 150
     - Hz
   * - Carrier Freq 2
     - 20 to 20000
     - 484.324
     - Hz
   * - Mod Index 1
     - 0 to 20
     - 12.649
     - x
   * - Mod Index 2
     - 0 to 20
     - 9
     - x
   * - Mod Freq Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Mod Freq Jit Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Carrier 1 Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Carrier 1 Jit Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Carrier 2 Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Carrier 2 Jit Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Index 1 Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Index 1 Jit Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Index 2 Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Index 2 Jit Freq
     - 0.01 to 20
     - 1
     - Hz

Parameter jitter
----------------

Each parameter has independent smooth random jitter. Amplitudes are relative:
``parameter * random(1 - amplitude, 1 + amplitude)``, clipped to the parameter
range.

Each jitter uses a pair of half-width amplitude and frequency sliders. Amplitude
sliders are logarithmic, start at 0.0001, and use ``gliss=0.0`` so their values
apply immediately at initialization. Frequency sliders set the jitter rate in Hz.

Graph Only
----------

**Overall Amplitude** controls the output amplitude over the performance duration.

Popups & Toggles
----------------

**Polyphony Voices** sets the number of simultaneous synthesis voices.

**Polyphony Spread** sets the pitch relationship between voices. Both polyphony
controls are set at initialization.
