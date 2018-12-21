import os
import re
import subprocess
from . import messages


def dashname(camelname):
    """Convert CamelName to dash-name."""
    return re.sub(r'([a-z])([A-Z])', r'\1-\2', camelname).lower()


def camelname(dashname):
    """Convert dash-name to CamelName."""
    return ''.join(part.capitalize() for part in dashname.split('-'))


templates = {
    'NoteOff': 'channel {ch} note-off {note} {velocity}',
    'NoteOn': 'channel {ch} note-on {note} {velocity}',
    'PolyPressure': 'channel {ch} poly-pressure {note} {value}',
    'ControlChange': 'channel {ch} control-change {number} {value}',
    'ProgramChange': 'channel {ch} program-change {number}',
    'ChannelPressure': 'channel {ch} channel-pressure {value}',
    'PitchBend': 'channel {ch} pitch-bend {value}',
    'TimeCode': 'time-code {type} {value}',
    'SongPosition': 'song-position {beats}',
    'SongSelect': 'song-select {number}',
    'TuneRequest': 'tune-request',
    'MidiClock': 'midi-clock',
    'Start': 'start',
    'Continue': 'continue',
    'Stop': 'stop',
    'ActiveSensing': 'active-sensing',
    'Reset': 'reset',
}

class_lookup = {dashname(name): getattr(messages, name) for name in templates}

def _parse_syx_line(line):
    # Example: "system-exclusive hex 01 02 03 dec"

    data = [byte for byte in line.split() if len(byte) == 2]
    return SystemExclusive(bytes(int(byte, 16) for byte in data))


def from_line(line):
    if 'system-exclusive' in line:
        return _parse_syx_line(line)
    else:
        for name, cls in class_lookup.items():
            if name in line:
                args = [int(arg) for arg in re.findall('(\d+)', line)]
                return cls(*args)
        else:
            raise ValueError(f'unknown message: {line.strip()!r}')

    
def as_line(msg):
    if msg.type == 'SystemExclusive':
        data = ' '.join(f'{byte:02x}' for byte in msg.data)
        return f'system-exclusive hex {data} dec'
    else:
        return templates[msg.type].format(**vars(msg))


class Input:
    @classmethod
    def names(cls):
        return [n.rstrip() for n in os.popen('receivemidi list').readlines()]

    @classmethod
    def dev(self, name):
        return Input('dev', name)

    @classmethod
    def virt(self, name):
        return Input('virt', name)
    
    def __init__(self, devtype, name):
        assert devtype in {'dev', 'virt'}

        self._proc = subprocess.Popen(['receivemidi', devtype, name, 'nn'],
                                      stdout=subprocess.PIPE)

    def __iter__(self):
        while True:
            line = self._proc.stdout.readline()
            yield from_line(line.decode('ascii'))


class Output:
    @classmethod
    def names(cls):
        return [n.rstrip() for n in os.popen('sendmidi list').readlines()]
        
    @classmethod
    def dev(self, name):
        return Output(name, 'dev')

    @classmethod
    def virt(self, name):
        return Output(name, 'virt')
    
    def __init__(self, name, devtype):
        assert devtype in {'dev', 'virt'}

        self._proc = subprocess.Popen(['sendmidi', devtype, name, '--'],
                                      stdin=subprocess.PIPE)

    def send(self, msg):
        line = as_line(msg) + '\n'
        self._proc.stdin.write(line.encode('ascii'))
        self._proc.stdin.flush()
