meep - MIDI messages for Python
===============================

Experimental MIDI library using Python 3.7 dataclasses.

*Note:* I have no plans for a formal release of Meep but if there's
interest it could be used as a starting point for a real
library. There may also be ideas here that could be reused in Mido.

.. code-block:: python

    >>> import meep
    >>> from meep import NoteOn, NoteOff, ControlChange
    >>> meep.list_outputs()
    ['Midi Through Port-0', 'reface CS MIDI 1']
    >>> out = meep.open_output('reface')  # Part of the name is enough.
    >>> out.send(NoteOn(60))              # Positional or keyword arguments.
    >>> out.send(NoteOff(note=60, ch=1))  # Channels are 1-16.

.. code-block:: python

    >>> c = ControlChange(number=64, value=127)  # Sustain pedal down.
    >>> c.value
    127
    >>> c.is_cc()
    True
    >>> c.is_cc(64)
    True
    >>> c.is_syx()
    False

.. code-block:: python

    >>> meep.new('ControlChange', 64, 127, 2)
    ControlChange(number=64, value=127, ch=2)
    >>> meep.new('cc', 64, 127, 2)
    ControlChange(number=64, value=127, ch=2)

.. code-block:: python

    >>> meep.as_bytes(c)
    (176, 64, 127)
    >>> meep.from_bytes((176, 64, 127))
    ControlChange(number=64, value=127, ch=1)

.. code-block:: python

    >>> import meep.rtmidi
    >>> meep.rtmidi.list_outputs()
    ['Midi Through:Midi Through Port-0 14:0',
     'reface CS:reface CS MIDI 1 20:0']
    >>> out = meep.rtmidi.open_output('reface cs')

Current API (may change in the future):

.. code-block:: python

    meep.NoteOff(note=0, velocity=64, ch=1)
    meep.NoteOn(note=0, velocity=64, ch=1)
    meep.PolyPressure(note=0, value=0, ch=1)
    meep.ControlChange(number=0, value=0, ch=1)
    meep.ProgramChange(number=0, ch=1)
    meep.ChannelPressure(value=0, ch=1)
    meep.PitchBend(value=0, ch=1)
    meep.SystemExclusive(data=b'')
    meep.TimeCode(type=0, value=0)
    meep.SongPosition(beats=0)
    meep.SongSelect(number=0)
    meep.TuneRequest()
    meep.MidiClock()
    meep.Start()
    meep.Continue()
    meep.Stop()
    meep.ActiveSensing()
    meep.Reset()

    meep.new(name, *args, **kwargs)  # create new message from name or alias

    meep.as_bytes(msg)               # encode message as bytes
    meep.from_bytes(midi_bytes)      # decode bytes and return message

    meep.list_inputs()
    meep.open_input(name)
    meep.create_input(name)
    meep.list_outputs()
    meep.open_output(name)
    meep.create_output(name)

* requires Python 3.7.1 or later.
* messages are implemented with Python data classes.
* messages are always immutable. Great news for concurrency.
* channels are 1-16.
* integrates nicely with Geert Bevin's
  https://github.com/gbevin/SendMIDI and
  https://github.com/gbevin/ReceiveMIDI tools. (Also uses same naming
  conventions.)
* type and value checking ensures that you always have a valid message.

This is very experimental code. API details may change.


Open Questions
--------------

* Where and how should type and value checking be done?

* What methods should the port classes have? What's a good minimal API that
  can be used equally well with async, threads and multiprocessing?

* What's a good API for copying messages? ``replace(msg, note=20)``?
  ``msg(note=20)``?  ``msg.copy(note=20)``?

* The ``__hash__()`` method created by ``dataclasses`` ignores the
  message type, which means for example ``hash(NoteOn(40)) ==
  hash(NoteOff(40))`` and ``hash(Start())`` == ``hash(Stop())``. This
  could be a problem.


Author: Ole Martin Bjorndalen
