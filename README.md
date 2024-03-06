# Arduino Runtime for MicroPython

A module to simplify and help writing MicroPython programs using the setup()/loop() paradigm.

## Commands
This module also wraps machine functions in easy-to-use methods

### pin_mode(PIN_NUMBER/ID, MODE)

This method is only provided as a mean to transition from Arduino C++ to MicroPython, but is redundant and unnecessary.
Might be still used with no harm to slowly drop the habit.
The following methods apply the required Pin direction on the fly.

```Python
pin_mode(3, INPUT)
pin_mode('D7', INPUT)
```

Will set the direction of the specified Pin and allow writing to or reading from the physical pin.

### digital_read(PIN_NUMBER/ID)

Reads a digital value from the pin with Number or ID specified.
For example:

```Python
digital_read(12)
digital_read('D7')
digital_read('A3')
```

return a value of `1` or `0` depending on the signal attached to the specified pins, for instance a button or a digital sensor.


### digital_write(PIN_NUMBER/ID, VALUE)

Writes the digital value (`HIGH|LOW|True|False|1|0`) to the pin with Number or ID specified.
For example:

```Python
digital_write(12, HIGH)
digital_write('D7', 1)
digital_write('A3', 0)
```

Will set the pin to the specified value.


### analog_read(PIN_NUMBER/ID)

Reads the analog value for the Voltage applied to the pinpin with Number or ID specified.
For example:

```Python
analog_read('A3')
analog_read('D18')
analog_read('2')
```

return a value between `0` and the maximum allowed by the processor's ADC based on the Voltage applied to the specified Pin.
Could be used to read the Voltage of a battery or any other analog source such as a potentiometer, light or moisture sensor to name a few.

### analog_write(PIN_NUMBER/ID, VALUE)

Writes an analog value (PWM) to the pin with Number or ID specified, if the Pin supports it.
VALUE should be between 0 and the maximum allowed PWM value and it's highly platform specific.
The method makes a conversion betwen the number and `frequency`/`duty_cycle`.

```Python
analog_write(12, 255)
analog_write('D7', 128)
analog_write('A3', 64)
```

Will generate a modulated signal on the specified Pin.
Can be used to control small motors with low current needs as well as servo motors.

#### IMPORTANT:

The numeric value for PIN_NUMBER is usually the processor's GPIO number, while values enclosed in quotes are "named pins" and are platform/implementation specific, not guaranteed to be valid.
A `ValueError` exception with label "invalid pin" is thrown if the pin number or ID is not valid.

### delay(MILLISECONDS)

Will halt the execution of your program for the amount of _milliseconds_ specified in the parameter.
It is to be considered a code-blocking command.


## Usage

The structure of an Arduino MicroPython program will look as follows:

```Python
from arduino import *

def setup():
  print('starting my program')

def loop():
  print('loop')
  delay(1000)

start(setup, loop)
```

The program above will define two main methods: `setup()` and `loop()`.
`setup()` will be invoked once at the execution of the program, while `loop()` will be invoked over and over until the program is stopped.
The stop condition might be caused by a system error or by manual trigger from the user during development/test.

The `start()` command is what causes the program to run, and is to be considered of high value in the MicroPython world.
While traditionally the code above would be written as follows

```Python
from time import sleep_ms

print('starting my program)

while True:
  print('loop')
  sleep_ms(1000)
```

Using the Arduino Runtime for MicroPython introduces some nice features, like the possibility to wrap user code in functions which can be tested during learning/development using the REPL.
Running the Arduino formatted code, omitting the `start()` command, would create the functions and every variable or object in the MicroPython board and allow the user to simply change a variable, set the property of an object and simply call `loop()` to see the results of their changes.
A more interactive approach to learning/testing/debugging.

We also introduce a new way of cleaning up and or resetting variables, objects, timers, leveraging a `cleanup()` method which will be called when the program is stopped or a system error happens which stops the execution of the program.
Please refer to the example "nano_esp32_advanced.py".

This brings the implemented runtime commands to the three described below

### setup()

Is run _once_ and should contain initialisation code.

### loop()
Is run indefinitely until the program stops.

### cleanup()
Is run _once_ when the program stops.
It should contain code such as resetting the value of variables, stopping timers, causing threads to stop running.

A `cleanup()` enchanced version of our initial program would look like this

```Python
from arduino import *

def setup():
  print('starting my program')

def loop():
  print('loop')
  delay(1000)

def cleanup():
  print('cleanup')

start(setup, loop)
```

## Utilities

Some utility methods are provided and are still in development:
* `map(x, in_min, in_max, out_min, out_max)`
  will remap the value `x` from its input range to an output range
* `mapi(x, in_min, in_max, out_min, out_max)`
  same as `map` but always returns an integer
* `random(low, high=None)`
  will return a random number between `0` and `low` - 1 if no `high` is provide, otherwise a value between `low` and `high` - 1
* `constrain(val, min_val, max_val)`
  will return a capped value of the number `val` between `min_val` and `max_val`
* `lerp(start, stop, amount)`
  will return a linear interpolation (percentage) of `amount` between `start` and `stop`

## Convenience and scaffolding methods

### create_sketch(SKETCH_NAME, PATH)

Will create a new Python file (`.py`) with the specified name at the provided path.
Example:

```Python
create_sketch('my_arduino_sketch')
create_sketch('my_arduino_sketch', 'tmp')
create_sketch('main')
```

If the destination `.py` file exists, a timestamp in _microseconds_ will be appended to the name.
The method returns the Python file's full path.

