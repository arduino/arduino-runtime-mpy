from arduino import *

def key_pressed(key, description):
  print(f'Key pressed: {key} {description}')

def cursor_move(direction):
  print(f'moving {direction}')

def setup():
  add_key_listener('esc', key_pressed, 'ESC', 'exit action')
  add_key_listener('a', key_pressed, 'a', 'is a key')
  add_key_listener('arrow_up', cursor_move, 'UP')
  add_key_listener('arrow_down', cursor_move, 'DOWN')
  add_key_listener('arrow_left', cursor_move, 'LEFT')
  add_key_listener('arrow_right', cursor_move, 'RIGHT')

def loop():
  delay(10)

start(setup, loop)