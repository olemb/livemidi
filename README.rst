meep - MIDI messages for Python
===============================

Experimental MIDI library using Python 3.7 dataclasses.

>>> import meep
>>> meep.
meep.ActiveSensing(    meep.NoteOff(          meep.Reset(            meep.SystemExclusive(  meep.create_input(     meep.messages
meep.ChannelPressure(  meep.NoteOn(           meep.SongPosition(     meep.TimeCode(         meep.create_output(    meep.new(
meep.Continue(         meep.PitchBend(        meep.SongSelect(       meep.TuneRequest(      meep.from_bytes(       meep.open_input(
meep.ControlChange(    meep.PolyPressure(     meep.Start(            meep.as_bytes(         meep.list_inputs(      meep.open_output(
meep.MidiClock(        meep.ProgramChange(    meep.Stop(             meep.bytes             meep.list_outputs(     meep.sendmidi

* requires Python 3.7.1 or later.
* messages are implemented with Python data classes.
* messages are always immutable. Great news for concurrency.
* channels are 1-16.
* attribute types and values are not checked (at least for now).
* integrates nicely with Geert Bevin's
  https://github.com/gbevin/SendMIDI and
  https://github.com/gbevin/ReceiveMIDI tools. (Also uses same naming
  conventions.)

This is a prerelease. API details may change.


Author: Ole Martin Bjorndalen
