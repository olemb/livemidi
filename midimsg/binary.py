# TODO: add some safety?
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
    0x80: lambda m: NoteOff(ch(m), m[1], m[2]),
    0x90: lambda m: NoteOn(ch(m), m[1], m[2]),
    0xb0: lambda m: ControlChange(ch(m), m[1], m[2]),
    0xf0: lambda m: SystemExclusive(bytes(m[1:-1])),
    0xff: lambda m: Reset()
}


def as_bytes(msg):
    return encoders[msg.__class__.__name__](msg)


def from_bytes(midi_bytes):
    status = midi_bytes[0]
    if status < 0xf0:
        # Strip away channel.
        status &= 0xf0

    return decoders[status](midi_bytes)
