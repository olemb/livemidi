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


class Input:
    @classmethod
    def names(cls):
        return rtmidi.MidiIn.get_ports()

    @classmethod
    def dev(cls, name):
        return Input('dev', name)

    @classmethod
    def virt(cls, name):
        return Input('virt', name)

    def __init__(self, devtype, name):
        self.name = name

        assert devtype in {'dev', 'virt'}

        self._rt = rtmidi.MidiIn()

        if devtype == 'dev':
            index = _get_port_index(self._rt.get_ports(), name)
            self._rt.open_port(index)
        elif devtype == 'virt':
            self._rt.open_virtual_port(name)

    def get(self):
        data = self._rt.get_message()
        if data:
            return from_bytes(data[0])
        else:
            return None

    def __iter__(self):
        while True:
            msg = self.get()
            if msg is None:
                return
            else:
                yield msg


class Output:
    @classmethod
    def names(cls):
        return rtmidi.MidiOut().get_ports()
    
    @classmethod
    def dev(cls, name):
        return Output('dev', name)

    @classmethod
    def virt(cls, name):
        return Output('virt', name)
    
    def __init__(self, devtype, name):
        self.name = name

        assert devtype in {'dev', 'virt'}

        self._rt = rtmidi.MidiOut()

        if devtype == 'dev':
            index = _get_port_index(self._rt.get_ports(), name)
            self._rt.open_port(index)
        elif devtype == 'virt':
            self._rt.open_virtual_port(name)

    def send(self, msg):
        self._rt.send_message(as_bytes(msg))
