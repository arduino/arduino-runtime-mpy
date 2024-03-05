from machine import Pin, ADC, PWM
from time import sleep_ms, ticks_us
from random import randrange
from math import sin, cos, radians, floor, ceil
from sys import exit

frame_count = 0
OUTPUT = Pin.OUT
INPUT = Pin.IN

HIGH = 1
LOW = 0

arduino_analog_inverted = False

# UTILITY
def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def mapi(x, in_min, in_max, out_min, out_max):
  return int(map(x, in_min, in_max, out_min, out_max))

def random(low, high=None):
  if high == None:
    return randrange(0, low)
  else:
    return randrange(low, high)

def constrain(val, min_val, max_val):
  return min(max_val, max(min_val, val))

def lerp(start, stop, amount):
  return start + amount * (stop - start)

# IO
def pinMode(_pin, _mode):
  return Pin(_pin, _mode)

def digitalWrite(_pin, _signal):
  p = Pin(_pin, Pin.OUT)
  p.value(_signal)

def digitalRead(_pin):
  p = Pin(_pin, Pin.IN)
  return p.value()

def delay(_ms):
  sleep_ms(_ms)

def analogRead(_pin):
  p = ADC(Pin(_pin))
  return p.read_u16()

def analogWrite(_pin, _duty_cycle):
  p = PWM(Pin(_pin))
  p.freq(1000)
  duty = mapi(_duty_cycle, 0, 255, 0, 1023)
  p.duty(floor(duty))
  if(_duty_cycle == 0):
    p.duty(0)
    p.deinit()

# the following methods are just for testing
# will produce output when this module is run as __main__
def preload():
  print()
  print()
  print()
  print('preload test')

def setup():
  print('setup test')

def loop():
  print('loop test')
  delay(1000)

def cleanup():
  print()
  print('cleanup test')
  print()
  print()

  
def frame_counter(_arg):
  global frame_count
  frame_count += 1
  sleep_ms(1)

# RUNTIME
def start(setup=None, loop=None, cleanup = None, preload = None):
  if preload is not None:
    preload()
  if setup is not None:
    setup()
  while True:
    try:
      if loop is not None:
        loop()
      ticks_st = ticks_us()
      while True:
        if ticks_us() - ticks_st > 1000:
          break
    except (Exception, KeyboardInterrupt) as e:
      if cleanup is not None:
        cleanup()
      if not isinstance(e, KeyboardInterrupt):
        raise e
      else:
        break

if __name__ == '__main__':
  start(setup = setup, loop = loop, cleanup = cleanup, preload = preload)