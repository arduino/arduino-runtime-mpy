from arduino import *

led_pin = 10

def setup():
  print('starting my program')
  pinMode(led_pin, OUTPUT)

def loop():
  print('loopy loop')
  digitalWrite(led_pin, HIGH)
  delay(1000)
  digitalWrite(led_pin, LOW)
  delay(1000)

start(setup, loop)