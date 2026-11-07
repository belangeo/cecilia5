Flanger : Four parallel flangers
================================

Description
-----------

Four independently enabled flangers mix the input with a sine-modulated recursive
delay. Frequency sets the modulation rate; Mid-delay sets its center time in
milliseconds; Depth scales the delay excursion; Feedback recirculates the delay.
The excursion is mid-delay multiplied by ``1 - depth`` to ``1 + depth``, with a
minimum of one sample. Feedback is limited to 0.999 internally.

Enabled branches are averaged, with smoothed gain changes. When all four are off,
the original input passes through. The Overall Amplitude envelope and the module's
0.7 output gain apply to both processed and pass-through audio.

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
   * - Frequency 1
     - 0.01 to 20
     - 0.2
     - Hz
   * - Mid-delay 1
     - 1 to 10
     - 5
     - ms
   * - Depth 1
     - 0 to 1
     - 0.95
     - x
   * - Feedback 1
     - 0 to 1
     - 0.5
     - x
   * - Frequency 2
     - 0.01 to 20
     - 0.3
     - Hz
   * - Mid-delay 2
     - 1 to 10
     - 4
     - ms
   * - Depth 2
     - 0 to 1
     - 0.95
     - x
   * - Feedback 2
     - 0 to 1
     - 0.5
     - x
   * - Frequency 3
     - 0.01 to 20
     - 0.4
     - Hz
   * - Mid-delay 3
     - 1 to 10
     - 3
     - ms
   * - Depth 3
     - 0 to 1
     - 0.95
     - x
   * - Feedback 3
     - 0 to 1
     - 0.5
     - x
   * - Frequency 4
     - 0.01 to 20
     - 0.5
     - Hz
   * - Mid-delay 4
     - 1 to 10
     - 2
     - ms
   * - Depth 4
     - 0 to 1
     - 0.95
     - x
   * - Feedback 4
     - 0 to 1
     - 0.5
     - x

Graph Only
----------

**Overall Amplitude** controls the output amplitude over the performance duration.

Popups & Toggles
----------------

**Flanger 1** enables its flanger. Defaults to On.

**Flanger 2** enables its flanger. Defaults to Off.

**Flanger 3** enables its flanger. Defaults to Off.

**Flanger 4** enables its flanger. Defaults to Off.

**Polyphony Voices** sets the number of simultaneous sampler voices.

**Polyphony Spread** sets the pitch relationship between voices. Both polyphony
controls are set at initialization.
