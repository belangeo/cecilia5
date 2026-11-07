SuperSaw : Seven detuned sawtooth oscillators
=============================================

Description
-----------

Based on pyo's ``SuperSaw`` emulation of the Roland JP-8000 Supersaw. Frequency
sets the central pitch, Detune spreads six side oscillators around the central
oscillator, and Oscillator Balance controls their relative levels. At balance
zero, only the central oscillator is heard.

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
   * - Frequency
     - 20 to 20000
     - 100
     - Hz
   * - Detune
     - 0 to 1
     - 0.5
     - x
   * - Oscillator Balance
     - 0 to 1
     - 0.7
     - x
   * - Freq Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Freq Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Detune Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Detune Jitter Freq
     - 0.01 to 20
     - 1
     - Hz
   * - Balance Jitter Amp
     - 0.0001 to 1
     - 0.0001
     - x
   * - Balance Jitter Freq
     - 0.01 to 20
     - 1
     - Hz

Parameter jitter
----------------

Frequency, detune, and oscillator balance have independent smooth random jitter.
Frequency jitter is relative: ``frequency * random(1 - amplitude, 1 + amplitude)``.
Detune and balance jitter are additive offsets between ``-amplitude`` and
``+amplitude``. The resulting base frequency stays within 20 to 20000 Hz; detune
and balance stay within 0 to 1. Polyphony transposition follows frequency jitter.

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
