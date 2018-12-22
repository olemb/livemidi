import rtmidi
from .bytes import as_bytes, from_bytes


def _get_port_index(names, name):
    try:
        return names.index(name)
    except ValueError:
        pass

    for i, n in enumerate(names):
        if name.lower() in n.lower():
            return i
    else:
        raise ValueError(f'unknown device {name!r}')


def list_inputs():
    return rtmidi.MidiIn().get_ports()


def list_outputs():
    return rtmidi.MidiOut().get_ports()
