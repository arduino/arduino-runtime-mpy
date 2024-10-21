# Arduino Runtime for MicroPython

A module to simplify and help writing MicroPython programs using the `setup()`/`loop()` paradigm.

This module also wraps machine functions in easy-to-use methods.

## Installation

### mip (MicroPython Package Manager)

This is the recommended method for boards which can connect to Internet.
Run the following MicroPython script using your favourite editor:

```py
import network
import mip
import time

SSID = 'YOUR WIFI NETWORK NAME (must be 2.4GHz)'
PWD = 'YOUR WIFI PASSWORD'

interface = network.WLAN(network.STA_IF)
interface.active(False)
time.sleep(0.1)
interface.active(True)

def connect(ssid, pwd):
  interface.connect(ssid, pwd)
  # Network Connection Progress
  max_dot_cols = 20
  dot_col = 0
  print()
  print(f"Connecting to {ssid}")
  while not interface.isconnected():
    if(dot_col % max_dot_cols == 0):
        print()
    print('.', end = '')
    dot_col +=1
    time.sleep_ms(100)
  print() 
  print(f'{"C" if interface.isconnected() else "NOT c"}onnected to network')

connect(SSID, PWD)
mip.install('github:arduino/arduino-runtime-mpy')

```

### mpremote mip

You will need to have Python and `mpremote` installed on your system, [follow these instructions](https://docs.micropython.org/en/latest/reference/mpremote.html) to do so.

Open a shell and run the following command:

```shell
mpremote mip install "github:arduino/arduino-runtime-mpy"
```

### Manual Installation

Copy the folder `arduino` and its content into your board's `lib` folder using your preferred method.

## Usage

The structure of a MicroPython program based on the Arduino Runtime for MicroPython will look as follows:

```py
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
The stop condition might be caused by a system error or by manual trigger from the user during development/testing.
The `start()` command is what causes these functions to be run as described above.

Traditionally the example code above would be written as follows in MicroPython:

```py
from time import sleep_ms

print('starting my program')

while True:
  print('loop')
  sleep_ms(1000)
```

Using the Arduino Runtime for MicroPython introduces some nice features, like the possibility to wrap user code in functions which can be tested during learning/development using the [REPL](https://docs.micropython.org/en/latest/reference/repl.html).

To debug your application interactively you can use an approach in which you define `setup()` and `loop()` but omit the `start()` command. That way you can change variables or set the property of an object through the REPL and simply call `loop()` to see the results of their changes without "restarting" the complete script.

We also introduced a new way of cleaning up and or resetting variables, objects, timers, leveraging a `cleanup()` method which will be called when the program is stopped or a system error occurs which stops the execution of the program.
Please refer to the example ["nano_esp32_advanced.py"](./examples/02_nano_esp32_advanced.py).

The runtime commands used in the example are explained in more detail below.

### setup()

Is run **once** and should contain initialisation code.

### loop()

Is run indefinitely until the program stops.

### cleanup()

Is run **once** when the program stops. This happen either when the user manually stops the execution of the program or if an error in the user code is thrown.
It should contain code such as resetting the value of variables, resetting peripherals, stopping timers, causing threads to stop running.

A version of our initial program that leverages the `cleanup()` function would look like this:

```py
from arduino import *

def setup():
  print('starting my program')

def loop():
  print('loop')
  delay(1000)

def cleanup():
  print('cleanup')

start(setup, loop, cleanup)
```

> [!NOTE]
> `cleanup()` is not invoked when the program stops because the hardware reset button on the board was pressed.

## Commands

Here's a list of commands and wrappers that can be used in your Arduino MicroPython program.

### pin_mode(PIN_NUMBER/ID, MODE)

This method is only provided as a mean to transition from Arduino C++ to MicroPython. In MicroPython a Pin object can be used directly instead.
The following methods apply the required Pin direction on the fly.

```py
pin_mode(3, INPUT)
pin_mode('D7', INPUT)
```

Will set the direction of the specified Pin and allow writing to or reading from the physical pin.

### digital_read(PIN_NUMBER/ID)

Reads a digital value from the pin with the specified number or ID.
For example:

```py
digital_read(12)
digital_read('D7')
digital_read('A3')
```

returns a value of `1` or `0` depending on the signal attached to the specified pins, for instance a button or a digital sensor.

### digital_write(PIN_NUMBER/ID, VALUE)

Writes the digital value (`HIGH|LOW|True|False|1|0`) to the pin with Number or ID specified.
For example:

```py
digital_write(12, HIGH)
digital_write('D7', 1)
digital_write('A3', 0)
```

Sets the pin to the specified value.

### analog_read(PIN_NUMBER/ID)

Reads the analog value for the Voltage applied to the pin with the specified number or ID.
For example:

```py
analog_read('A3')
analog_read('D18')
analog_read('2')
```

returns a value between `0` and the maximum resolution of the processor's ADC based on the Voltage applied to the specified Pin.
Could be used to read the Voltage of a battery or any other analog source such as a potentiometer, light or moisture sensor to name a few.

### analog_write(PIN_NUMBER/ID, VALUE)

Writes an analog value (PWM) to the pin with Number or ID specified, if the Pin supports it.
VALUE should be between 0 and the maximum allowed PWM value 255.

```py
analog_write(12, 255)
analog_write('D7', 128)
analog_write('A3', 64)
```

Will generate a pulse width modulated signal on the specified Pin.
Can be used to control small motors with low current needs, servo motors or an LED's brightness.

> [!IMPORTANT]  
> The numeric value for PIN_NUMBER is usually the processor's GPIO number, while values enclosed in quotes are "named pins" and are platform/implementation specific. A `ValueError` exception with label "invalid pin" is thrown if the pin number or ID is not valid.

### delay(MILLISECONDS)

Will halt the execution of your program for the amount of **milliseconds** specified in the parameter.
It is to be considered a code-blocking command.

```py
delay(1000) # Delay the execution for 1 second
```

## Utilities

Some utility methods are provided and are still in development:

* `map_float(x, in_min, in_max, out_min, out_max)`
  Remaps the value `x` from its input range to an output range as a float
* `map_int(x, in_min, in_max, out_min, out_max)`
  same as `map_float` but always returns an integer
* `random(low, high=None)`
  Returns a random number between `0` and `low` - 1 if no `high` is provided, otherwise a value between `low` and `high` - 1
* `constrain(val, min_val, max_val)`
  Returns a capped value of the number `val` between `min_val` and `max_val`
* `lerp(start, stop, amount)`
  Returns a linear interpolation (percentage) of `amount` between `start` and `stop`

## Convenience and scaffolding methods

### create_sketch(sketch_name = None, destination_path = '.', overwrite = False, source = None)

Creates a new Python file (`.py`) with the specified name at the provided path.
By default if a file with the same name is found, it will append a timestamp to the filename, but overwrite can be forced by setting that parameter to True.
Providing a source path it will use that file's content, effectively copying the code from the source file to the newly created one.

Examples:

```py
create_sketch('my_arduino_sketch')
create_sketch('my_arduino_sketch', 'tmp')
create_sketch('main')
```

The method returns the Python file's full path.

### copy_sketch(source_path = '', destination_path = '.', name = None, overwrite = False)

Wraps `create_sketch()` and provides a shortcut to copy a file to another path.
