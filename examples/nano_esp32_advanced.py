# Arduino Nano ESP32
#   
# Timers and free running loop
#   
# Author: Ubi de Feo
#   
#   This example shows how to use the Timer class to create blinking LEDs and
#   periodic messages. It also shows how to use the free running loop to read
#   the state of a button and control the onboard red LED accordingly.
#   
#   It demonstrates how to use the start() function to run the setup() and loop()
#   functions and the cleanup() function when the program is interrupted. 
#   The cleanup() function has the responsibility to reset the timers and turn
#   off the LEDs.
#   
#   Connect a button between pin D6 and VCC
#   The button needs to have a pull-down resistor (10k Ohm) connected to GND
#   

from arduino import *
from machine import Timer

led_builtin = 'LED_BUILTIN'
led_builtin_state = False
led_red = 'LED_RED'

button = 'D6'

blink_timer = Timer(0)
message_timer = Timer(1)

def blink_me(_timer):
	global led_builtin_state
	print('blink')
	led_builtin_state = not led_builtin_state
	if led_builtin_state:
		digital_write(led_builtin, HIGH)
	else:
		digital_write(led_builtin, LOW)

def timed_message(_timer):
  print('hello')

def setup():
  print('my first program')
  blink_timer.init(period = 500, mode = Timer.PERIODIC, callback = blink_me)
  message_timer.init(period = 2000, mode = Timer.PERIODIC, callback = timed_message)

def loop():
  if digital_read(button):
    digital_write(led_red, LOW)
  else:
    digital_write(led_red, HIGH)  

def cleanup():
  print("*** cleaning up ***")
  blink_timer.deinit()
  message_timer.deinit()
  digital_write(led_builtin, LOW)
  digital_write(led_red, HIGH)

start(setup, loop, cleanup)
