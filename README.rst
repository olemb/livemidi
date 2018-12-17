midimsg - MIDI messages for Python
==================================

* requires Python 3.7.1 or later.
* messages are implemented with Python data classes.
* messages are always immutable. Great news for concurrency.
* 100% pure functional code (no side effects)
* channels are 1-16.
* attribute types and values are not checked (at least for now).
* integrates nicely with Geert Bevin's SendMIDI and ReceiveMIDI
  tools. (Also uses same naming conventions.)

Author: Ole Martin Bjorndalen
