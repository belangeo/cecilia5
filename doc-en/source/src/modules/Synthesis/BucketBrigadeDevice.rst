BucketBrigadeDevice : Cross-fed bucket-brigade delay synthesis
==============================================================

Description
-----------

Based on pyo's ``08_bucket_brigade_device.py`` example, with the regular Cecilia
sampler replacing the input oscillator. Two delay lines feed themselves and each
other through ring modulators and lowpass filters. Feedback sets self-feedback;
Cross Feedback sets feedback from the opposite branch. Lowpass Frequency controls
both filters. The output is compressed with threshold -30 dB, ratio 4, and knee
0.5, matching the example.

Delay Time 1 and 2 set the center delay times. Slow sine modulation adds 0.05 and
0.08 seconds at 0.005 and 0.003 Hz respectively. Ring Frequency 1 and 2 set the
center ring-modulator frequencies, with drift of 50 and 40 Hz at 0.007 and 0.008 Hz.
Delay times are limited to one sample through 2 seconds; ring frequencies are
limited to 1 through 5000 Hz after modulation.

The sampler input is scaled by 0.025 before entering the feedback network. The
two filtered branches alternate across output channels; mono output averages
both.

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
   * - Delay Time 1
     - 0.001 to 2
     - 0.25
     - sec
   * - Delay Time 2
     - 0.001 to 2
     - 0.3
     - sec
   * - Ring Frequency 1
     - 1 to 5000
     - 250
     - Hz
   * - Ring Frequency 2
     - 1 to 5000
     - 200
     - Hz
   * - Feedback
     - 0 to 0.999
     - 0.8
     - x
   * - Cross Feedback
     - 0 to 0.999
     - 0.99
     - x
   * - Lowpass Freq 1
     - 20 to 20000
     - 3000
     - Hz
   * - Lowpass Freq 2
     - 20 to 20000
     - 3000
     - Hz
   * - Delay 1 Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Delay 1 Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Delay 2 Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Delay 2 Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Ring 1 Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Ring 1 Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Ring 2 Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Ring 2 Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Feedback Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Feedback Jit Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Cross Feed Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Cross Feed Jit Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Lowpass Jit Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Lowpass Jit Freq
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

**Polyphony Voices** sets the number of simultaneous sampler voices.

**Polyphony Spread** sets the pitch relationship between voices. Both polyphony
controls are set at initialization.
