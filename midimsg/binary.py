from .messages import *


def ch(m):
    return (m[0] & 0xf) + 1


encoders = {
    'NoteOff': lambda msg: (0x80|msg.ch-1, msg.note, msg.velocity),
    'NoteOn': lambda msg: (0x90|msg.ch-1, msg.note, msg.velocity),
    'PolyPressure': lambda msg: (0xa0|msg.ch-1, msg.note, msg.value),
    'ControlChange': lambda msg: (0xb0|msg.ch-1, msg.number, msg.value),
    'ProgramChange': lambda msg: (0xc0|msg.ch-1, msg.number),
    'ChannelPressure': lambda msg: (0xd0|msg.ch-1, msg.value),
    'PitchBend' :lambda msg: (0xe0|msg.ch-1, msg.value & 0x7f, msg.value >> 7),
    'SystemExclusive': lambda msg: (0xf0,) + tuple(msg.data) + (0xf7,),
    'TimeCode': lambda msg: (0xf1, msg.type << 4 | msg.value),
    'SongPosition': lambda msg: (0xf2, msg.value & 0x7f, msg.value >> 7),
    'SongSelect': lambda msg: (0xf3, msg.number),
    'TuneRequest': lambda msg: (0xf6,),
    'MidiClock': lambda msg: (0xf8,),
    'Start': lambda msg: (0xfa,),
    'Continue': lambda msg: (0xfb,),
    'Stop': lambda msg: (0xfc,),
    'ActiveSensing': lambda msg: (0xfe,),
    'Reset': lambda msg: (0xff,),
}


decoders = {
    0x80: lambda m: NoteOff(ch(m), m[1], m[2]),
    0x90: lambda m: NoteOn(ch(m), m[1], m[2]),
    0xa0: lambda m: PolyPressure(ch(m), m[1], m[2]),
    0xb0: lambda m: ControlChange(ch(m), m[1], m[2]),
    0xc0: lambda m: ProgramChange(ch(m), m[1]),
    0xd0: lambda m: ChannelPressure(ch(m), m[1]),
    0xe0: lambda m: PitchBend(ch(m), (m[1] | m[2] << 7)),
    0xf0: lambda m: SystemExclusive(bytes(m)),
    0xf1: lambda m: TimeCode(m[1] >> 4, m[1] & 0xf),
    0xf2: lambda m: SongPosition((m[1] | m[2] << 7)),
    0xf3: lambda m: SongSelect(m[1]),
    0xf6: lambda m: TuneRequest(),
    0xf8: lambda m: MidiClock(),
    0xfa: lambda m: Start(),
    0xfb: lambda m: Continue(),
    0xfc: lambda m: Stop(),
    0xfe: lambda m: ActiveSensing(),
    0xff: lambda m: Reset(),
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
