import time
from livemidi.messages import *
from livemidi.sendmidi import open_output

out = open_output('GM')

for i in range(10):
    note = i + 2
    out.send(NoteOn())
    time.sleep(0.3)
    out.send(NoteOff())
    time.sleep(0.1)
