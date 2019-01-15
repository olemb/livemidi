meep - MIDI messages for Python
===============================

Experimental MIDI library using Python 3.7 dataclasses.

Current API (may change in the future)::

    NoteOff(note=0, velocity=64, ch=1)
    NoteOn(note=0, velocity=64, ch=1)
    PolyPressure(note=0, value=0, ch=1)
    ControlChange(number=0, value=0, ch=1)
    ProgramChange(number=0, ch=1)
    ChannelPressure(value=0, ch=1)
    PitchBend(value=0, ch=1)
    SystemExclusive(data=b'')
    TimeCode(type=0, value=0)
    SongPosition(beats=0)
    SongSelect(number=0)
    TuneRequest()
    MidiClock()
    Start()
    Continue()
    Stop()
    ActiveSensing()
    Reset()

    new(name, *args, **kwargs)  # create new message from name or alias

    as_bytes(msg)               # encode message as bytes
    from_bytes(midi_bytes)      # decode bytes and return message

    list_inputs()
    open_input(name)
    create_input(name)
    list_outputs()
    open_output(name)
    create_output(name)

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
