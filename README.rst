meep - MIDI messages for Python
===============================

Experimental MIDI library using Python 3.7 dataclasses.

Current API (may change in the future)::

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
* attribute types and values are not checked (at least for now).
* integrates nicely with Geert Bevin's
  https://github.com/gbevin/SendMIDI and
  https://github.com/gbevin/ReceiveMIDI tools. (Also uses same naming
  conventions.)

This is very experimental code. API details may change.


Author: Ole Martin Bjorndalen
