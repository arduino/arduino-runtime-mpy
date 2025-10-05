# The following functions are used for testing only
# and provide a faux implementation of the user's functions
from arduino import *

def preload():
  print('preload')

def setup():
  add_key_listener(KEY_UP, print, 'key:', 'up')
  add_key_listener(KEY_DOWN, print, 'key:', 'down')
  add_key_listener(KEY_LEFT, print, 'key:', 'left')
  add_key_listener(KEY_RIGHT, print, 'key:', 'right')
  print('setup')

def loop():
  print('loop')
  delay(100)

def cleanup():
  print('cleanup')

start(setup, loop, cleanup, preload)
