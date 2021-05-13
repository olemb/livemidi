meep - MIDI messages for Python
===============================

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
    >>> c.type
    'ControlChange'
    >>> c.alias
    'cc'
Author: Ole Martin Bjorndalen
.. code-block:: python

    >>> c.copy(value=0)
    ControlChange(number=64, value=0)

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
    meep.TimeCode(frame_type=0, frame_value=0)
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


Ole Martin Bjørndalen
