Chorus : Eight modulated delay lines
====================================

Description
-----------

Based on pyo's ``Chorus`` object. Depth controls modulation depth, Feedback
recirculates the delayed signal, and Dry / Wet blends the original input with the
chorus. At Dry / Wet zero, only the original input is heard.

Input
-----

The standard Cecilia sampler provides sound-file or live input, with its normal
looping, pitch, and polyphony controls. In the routing view, this module can also
process audio from upstream modules.

Sliders
-------

.. list-table:: Parameter ranges and defaults
   :header-rows: 1
   :widths: 40 25 20 15

   * - Control
     - Range
     - Default
     - Unit
   * - Depth
     - 0 to 5
     - 1
     - x
   * - Feedback
     - 0 to 1
     - 0.25
     - x
   * - Depth Jitter Amp
     - 0.0001 to 5
     - 0.0001
     - x
   * - Depth Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Feed Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Feed Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Dry / Wet
     - 0 to 1
     - 0.5
     - x

Parameter jitter
----------------

Depth and feedback have independent smooth random jitter. Their amplitudes are
additive offsets in the parameter's units: depth jitter spans ``-amplitude`` to
``+amplitude`` around Depth, and feedback jitter behaves the same way around
Feedback. The resulting depth stays within 0 to 5 and feedback within 0 to 1.

Each jitter uses a pair of half-width amplitude and frequency sliders. Amplitude
sliders are logarithmic, start at 0.0001, and use ``gliss=0.0`` so their values
apply immediately at initialization. Frequency sliders set the jitter rate in Hz.

Graph Only
----------

**Overall Amplitude** controls the output amplitude over the performance duration.

Popups & Toggles
----------------

**Polyphony Voices** sets the number of simultaneous sampler voices.

**Polyphony Spread** sets the pitch relationship between voices. Both polyphony
controls are set at initialization.
