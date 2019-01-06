from numbers import Integral
from dataclasses import dataclass, replace


class MidiMsg:
    @property
    def type(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return replace(self, *args, **kwargs)

    def is_cc(self, number=None):
        if not isinstance(self, ControlChange):
            return False
        elif number is None:
            return True
        else:
            return self.number == number

    def is_syx(self):
        return isinstance(self, SystemExclusive)


@dataclass(frozen=True, eq=True)
class NoteOff(MidiMsg):
    ch: Integral = 1
    note: Integral = 0
    velocity: Integral = 64
    alias = 'off'


@dataclass(frozen=True, eq=True)
class NoteOn(MidiMsg):
    ch: Integral = 1
    note: Integral = 0
    velocity: Integral = 64
    alias = 'on'


@dataclass(frozen=True, eq=True)
class PolyPressure(MidiMsg):
    ch: Integral = 1
    note: Integral = 0
    value: Integral = 0
    alias = 'pp'


@dataclass(frozen=True, eq=True)
class ControlChange(MidiMsg):
    ch: Integral = 1
    number: Integral = 0
    value: Integral = 0
    alias = 'cc'


@dataclass(frozen=True, eq=True)
class ProgramChange(MidiMsg):
    ch: Integral = 1
    number: Integral = 0
    alias = 'pc'


@dataclass(frozen=True, eq=True)
class ChannelPressure(MidiMsg):
    ch: Integral = 1
    value: Integral = 0
    alias = 'cp'


@dataclass(frozen=True, eq=True)
class PitchBend(MidiMsg):
    ch: Integral = 1
    value: Integral = 0
    alias = 'pb'


@dataclass(frozen=True, eq=True)
class SystemExclusive(MidiMsg):
    data: bytes = b''
    alias = 'syx'


@dataclass(frozen=True, eq=True)
class TimeCode(MidiMsg):
    type: Integral = 0
    value: Integral = 0
    alias = 'tc'


@dataclass(frozen=True, eq=True)
class SongPosition(MidiMsg):
    beats: Integral = 0
    alias = 'spp'


@dataclass(frozen=True, eq=True)
class SongSelect(MidiMsg):
    number: Integral = 0
    alias = 'ss'


@dataclass(frozen=True, eq=True)
class TuneRequest(MidiMsg):
    alias = 'tun'


@dataclass(frozen=True, eq=True)
class MidiClock(MidiMsg):
    alias = 'mc'


@dataclass(frozen=True, eq=True)
class Start(MidiMsg):
    alias = 'start'


@dataclass(frozen=True, eq=True)
class Continue(MidiMsg):
    alias = 'cont'


@dataclass(frozen=True, eq=True)
class Stop(MidiMsg):
    alias = 'stop'


@dataclass(frozen=True, eq=True)
class ActiveSensing(MidiMsg):
    alias = 'as'


@dataclass(frozen=True, eq=True)
class Reset(MidiMsg):
    alias = 'rst'


classes = [
    NoteOff,
    NoteOn,
    PolyPressure,
    ControlChange,
    ProgramChange,
    ChannelPressure,
    PitchBend,
    SystemExclusive,
    TimeCode,
    SongPosition,
    SongSelect,
    TuneRequest,
    MidiClock,
    Start,
    Continue,
    Stop,
    ActiveSensing,
    Reset,
]


def get_class(name):
    # TODO: add a lookup table.
    for cls in classes:
        if name in [cls.__name__, cls.alias]:
            return cls
    else:
        raise ValueError(f'unknown MIDI message {name!r}')


def new(name, *args, **kwargs):
    return get_class(name)(*args, **kwargs)


__all__ = [_.__name__ for _ in classes]
