# Any Arduino board
#   
# Blinking LED
#   
# Author: Ubi de Feo
#   
#   This example shows how to blink the onboard LED of an Arduino board.
#   The LED will stay on for 500ms and off for 500ms, then the cycle repeats
#   creating a blinking effect.
#   

from arduino import *

led = 'LED_BUILTIN'
def setup():
  print('starting my program')

def loop():
  print('loopy loop')
  digital_write(led, HIGH)
  delay(500)
  digital_write(led, LOW)
  delay(500)

start(setup, loop)