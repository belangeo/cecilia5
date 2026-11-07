FrequencyModulation : Frequency modulation synthesis
====================================================

Description
-----------

Based on pyo's ``FM`` object and Chowning frequency modulation synthesis. Carrier
Frequency sets the carrier pitch. Frequency Ratio multiplies that frequency to
set the modulator frequency. Modulation Index multiplies the modulator frequency
to set its modulation amplitude.

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
   * - Carrier Frequency
     - 20 to 20000
     - 100
     - Hz
   * - Frequency Ratio
     - 0.01 to 20
     - 0.5
     - x
   * - Modulation Index
     - 0 to 50
     - 5
     - x
   * - Carrier Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Carrier Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Ratio Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Ratio Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Index Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Index Jitter Freq
     - 0.01 to 20
     - 1
     - Hz

Parameter jitter
----------------

Each synthesis parameter has independent smooth random jitter. Amplitudes are
relative: ``parameter * random(1 - amplitude, 1 + amplitude)``, clipped to the
parameter range. For the FM modules, carrier jitter precedes polyphony pitch
transposition.

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
