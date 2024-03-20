__author__ = "ubi de feo / murilo polese"
__license__ = "MPL 2.0"
__version__ = "0.1.0"
__maintainer__ = "Arduino"

from machine import Pin, ADC, PWM
from time import sleep_ms, ticks_us
from random import randrange
from math import sin, cos, radians, floor, ceil
from sys import exit

OUTPUT = Pin.OUT
INPUT = Pin.IN

# Blocking by default to allow threads to run
# If you're not using threads, you can set this to True
NON_BLOCKING = False

HIGH = 1 # Voltage level HIGH
LOW = 0 # Voltage level LOW

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
def pin_mode(_pin, _mode):
  return Pin(_pin, _mode)

def pinMode(_pin, _mode):
  return pin_mode(_pin, _mode)

def digital_write(_pin, _signal):
  p = Pin(_pin, Pin.OUT)
  p.value(_signal)

def digitalWrite(_pin, _signal):
  return digital_write(_pin, _signal)

def digital_read(_pin):
  p = Pin(_pin, Pin.IN)
  return p.value()

def digitalRead(_pin):
  return digital_read(_pin)

def analog_read(_pin):
  p = ADC(Pin(_pin))
  return p.read_u16()

def analogRead(_pin):
  return analog_read(_pin)

def analog_write(_pin, _duty_cycle):
  p = PWM(Pin(_pin))
  p.freq(1000)
  duty = mapi(_duty_cycle, 0, 255, 0, 1023)
  p.duty(floor(duty))
  if(_duty_cycle == 0):
    p.duty(0)
    p.deinit()

def analogWrite(_pin, _duty_cycle):
  return analog_write(_pin, _duty_cycle)

def delay(_ms):
  sleep_ms(_ms)


# HELPERS

def get_template_path():
  return '/'.join(__file__.split('/')[:-1]) + '/template.tpl'

def create_sketch(sketch_name = None, destination_path = '.', overwrite = False, source_path = None):

  if sketch_name is None:
    sketch_name = 'main'
  new_sketch_path = f'{destination_path}/{sketch_name}.py'
  try:
    open(new_sketch_path, 'r')
    if not overwrite:
      sketch_name = f'{sketch_name}_{ticks_us()}'
  except OSError:
    pass
  
  template_path = get_template_path() if source_path is None else source_path
  template_sketch = open(template_path, 'r')
  new_sketch_path = f'{destination_path}/{sketch_name}.py'

  with open(new_sketch_path, 'w') as f:
    sketch_line = None
    while sketch_line is not '':
      sketch_line = template_sketch.readline()
      f.write(sketch_line)
  f.close()
  template_sketch.close()
  return new_sketch_path

def copy_sketch(source_path = '', destination_path = '.', name = None, overwrite = False):
  name = name or 'main'
  return create_sketch(sketch_name = name, destination_path = destination_path, overwrite = overwrite, source_path = source_path)

# RUNTIME
def start(setup=None, loop=None, cleanup = None, preload = None):
  if setup is not None:
    setup()
  try:
    while True:
      if loop is not None:
        loop()
      if not NON_BLOCKING:
        sleep_ms(1)
  except (Exception, KeyboardInterrupt) as e:
    if cleanup is not None:
      cleanup()
    if not isinstance(e, KeyboardInterrupt):
      raise e
