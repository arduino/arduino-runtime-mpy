from arduino import *

item_selected = None

def inventory(open = True):
  if open:
    print('- showing inventory -')
    print('1. Potion - Get more energy')
    print('2. Key - Open a door')
    print('3. Sword - Defend from enemy')
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
  print('Start game...')

def loop():
  delay(10)

start(setup, loop)