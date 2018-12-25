"""
pip install python-rtmidi
"""
import rtmidi
from .bytes import as_bytes, from_bytes


def _find_port(rt, name):
    names = rt.get_ports()
    try:
        return names.index(name)
    except ValueError:
        pass

    for index, fullname in enumerate(names):
        if name.lower() in fullname.lower():
            return index
    else:
        raise ValueError(f'unknown device {name!r}')


def _open_port(rt, name, virtual=False):
    if virtual:
        rt.open_virtual_port(name)
    else:
        rt.open_port(_find_port(rt, name))


def list_inputs():
    return rtmidi.MidiIn().get_ports()


def list_outputs():
    return rtmidi.MidiOut().get_ports()


def open_input(name):
    return Input(name)


def open_output(name):
    return Output(name)


def create_input(name):
    return Input(name, virtual=True)


def create_output(name):
    return Output(name, virtual=True)


class Input:
    def __init__(self, name, virtual=False):
        self.rt = rtmidi.MidiIn()
        _open_port(self.rt, name, virtual=virtual)


class Output:
    def __init__(self, name, virtual=False):
        self.rt = rtmidi.MidiOut()
        _open_port(self.rt, name, virtual=virtual)

    def send(self, msg):
        self.rt.send_message(as_bytes(msg))


__all__ = ['list_inputs', 'list_outputs',
           'open_input', 'open_output',
           'create_input', 'create_output']
