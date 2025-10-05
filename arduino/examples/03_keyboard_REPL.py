# Keyboard use in REPL
# by Ubi de Feo
#
# This demo code shows how to implement interactive behaviour in REPL.
# When running this code in a REPL session, using keys can trigger actions.
# 
# Simply add a listener for a key (KEY_UP, KEY_DOWN, ENTER, ESC, etc.) and a callback.
# Supports variable arguments which must be handled by the callback (see setup())

from arduino import *

item_selected = None

def inventory(open = True):
  if open:
    print('- open inventory -')
    print('(a) Potion - Get more energy')
    print('(b) Key - Open a door')
    print('(c) Sword - Defend from enemy')
  else:
    print('- closing inventory -')

def select_item(item, description):
  global item_selected
  item_selected = item
  print(f'Item selected: {item}')
  print(f'Description: {description}')

def use_item():
  print(f'using {item_selected}')

def player_move(direction):
  print(f'Player moving {direction}')

def setup():
  add_key_listener(KEY_ESC, inventory, False)
  add_key_listener(KEY_ENTER, inventory)
  add_key_listener(KEY_SPACE, use_item)
  add_key_listener(KEY_UP, player_move, 'UP')
  add_key_listener(KEY_DOWN, player_move, 'DOWN')
  add_key_listener(KEY_LEFT, player_move, 'LEFT')
  add_key_listener(KEY_RIGHT, player_move, 'RIGHT')
  add_key_listener('a', select_item, 'potion', 'get more energy')
  add_key_listener('b', select_item, 'key', 'open a door')
  add_key_listener('c', select_item, 'sword', 'defend from enemy')
  print('starting...')
  print('Arrows: move')
  print('Enter: open inventory')
  print('ESC: close inventory')
  print('a: select potion')
  print('b: select key')
  print('c: select sword')

def loop():
  delay(10)

start(setup, loop)