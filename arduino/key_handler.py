import select
from sys import stdin

class KeyHandler:
  UP = "arrow_up"
  DOWN = "arrow_down"
  LEFT = "arrow_left"
  RIGHT = "arrow_right"
  ESC = "esc"
  ENTER = "enter"
  SPACE = " "
  ESCAPE_SEQUENCE_TIMEOUT = 0.01
  def __init__(self):
    self._key_events = {}
  
  def add_key_listener(self, key, callback, *params):
    key_event = KeyEvent(key, callback, params if params else None)
    self._key_events[key] = key_event
  
  def remove_key_listener(self, key):
    if key in self._key_events:
      del self._key_events[key]
      return True
    return False

  def remove_all_listeners(self):
    self._key_events.clear()
    return True
  
  def _key_is_down(self):
    if stdin in select.select([stdin], [], [], 0)[0]:
      ch = stdin.read(1)
      
      if ch == '\n' or ch == '\r':
        return self.ENTER
      
      if ch == '\x1b':
        # Wait briefly for escape sequence
        if stdin in select.select([stdin], [], [], KeyHandler.ESCAPE_SEQUENCE_TIMEOUT)[0]:
          next_ch = stdin.read(1)
          if next_ch == '[':
            if stdin in select.select([stdin], [], [], KeyHandler.ESCAPE_SEQUENCE_TIMEOUT)[0]:
              arrow_ch = stdin.read(1)
              if arrow_ch == 'A':
                return self.UP
              elif arrow_ch == 'B':
                return self.DOWN
              elif arrow_ch == 'C':
                return self.RIGHT
              elif arrow_ch == 'D':
                return self.LEFT
        return self.ESC
      
      return ch
    
    return None
    
  def read_keys(self):
    while True:
      detected_key = self._key_is_down()
      if detected_key is None:
        break
      if detected_key in self._key_events:
        self._key_events[detected_key].trigger()


class KeyEvent:
  def __init__(self, key=None, callback=None, args=None):
    self.key = key
    self.callback = callback
    self.callback_arguments = args
  
  def trigger(self):
    if self.callback_arguments is None:
      self.callback()
    else:
      self.callback(*self.callback_arguments)
