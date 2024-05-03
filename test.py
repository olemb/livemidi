from livemidi.sendmidi import open_input

for msg in open_input('MPK'):
    print(msg)
