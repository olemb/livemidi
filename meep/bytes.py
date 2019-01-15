from .messages import *


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
    'SongPosition': lambda msg: (0xf2, msg.beats & 0x7f, msg.beats >> 7),
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
    0x80: lambda msg: NoteOff(msg[1], msg[2], (msg[0]&15)+1),
    0x90: lambda msg: NoteOn(msg[1], msg[2], (msg[0]&15)+1),
    0xa0: lambda msg: PolyPressure(msg[1], msg[2], (msg[0]&15)+1),
    0xb0: lambda msg: ControlChange(msg[1], msg[2], (msg[0]&15)+1),
    0xc0: lambda msg: ProgramChange(msg[1], (msg[0]&15)+1),
    0xd0: lambda msg: ChannelPressure(msg[1], (msg[0]&15)+1),
    0xe0: lambda msg: PitchBend((msg[1] | msg[2] << 7), (msg[0]&15)+1),
    0xf0: lambda msg: SystemExclusive(bytes(msg[1:-1])),
    0xf1: lambda msg: TimeCode(msg[1] >> 4, msg[1] & 0xf),
    0xf2: lambda msg: SongPosition((msg[1] | msg[2] << 7)),
    0xf3: lambda msg: SongSelect(msg[1]),
    0xf6: lambda msg: TuneRequest(),
    0xf8: lambda msg: MidiClock(),
    0xfa: lambda msg: Start(),
    0xfb: lambda msg: Continue(),
    0xfc: lambda msg: Stop(),
    0xfe: lambda msg: ActiveSensing(),
    0xff: lambda msg: Reset(),
}


def as_bytes(msg):
    return encoders[msg.__class__.__name__](msg)


def from_bytes(midi_bytes):
    status = midi_bytes[0]
    if status < 0xf0:
        # Strip away channel.
        status &= 0xf0

    return decoders[status](midi_bytes)
