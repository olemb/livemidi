from .messages import *


def ch(m):
    return (m[0] & 0xf) + 1


encoders = {
    'NoteOff': lambda msg: (0x80|msg.ch-1, msg.note, msg.velocity),
    'NoteOn': lambda msg: (0x90|msg.ch-1, msg.note, msg.velocity),

    'ControlChange': lambda msg: (0xb0|msg.ch-1, msg.number, msg.value),
    'SystemExclusive': lambda msg: (0xf0,) + tuple(msg.data) + (0xf7,),
    'Reset': lambda msg: (0xff,)
}


decoders = {
    0x80: lambda Q: NoteOff(ch(B), Q[1], Q[2]),
    0x90: lambda Q: NoteOn(ch(B), Q[1], Q[2]),
    0xa0: lambda Q: PolyPressure(ch(B), Q[1], Q[2]),
    0xb0: lambda Q: ControlChange(ch(B), Q[1], Q[2]),
    0xc0: lambda Q: ProgramChange(ch(B), Q[1]),
    0xd0: lambda Q: ChannelPressure(ch(B), Q[1]),
    0xe0: lambda Q: PitchBend(ch(B), (Q[1] | Q[2] << 7)),  # ?
    0xf0: lambda Q: SystemExclusive(bytes(Q)),
    0xf1: lambda Q: TimeCode(Q[1] >> 4, Q[1] & 15),  # ?
    0xf2: lambda Q: SongPosition((Q[1] | Q[2] << 7)),  # ?
    0xf3: lambda Q: SongSelect(Q[1]),
    0xf6: lambda Q: TuneRequest(),
    0xf8: lambda Q: MidiClock(),
    0xfa: lambda Q: Start(),
    0xfb: lambda Q: Continue(),
    0xfc: lambda Q: Stop(),
    0xfe: lambda Q: ActiveSensing(),
    0xff: lambda Q: Reset(),
}


# TODO: "asbytes()"? (seems to be the convention with dataclasses).
def as_bytes(msg):
    return encoders[msg.__class__.__name__](msg)


def from_bytes(midi_bytes):
    status = midi_bytes[0]
    if status < 0xf0:
        # Strip away channel.
        status &= 0xf0

    return decoders[status](midi_bytes)
