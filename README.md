# LED-Strip-Driver-Module-RaspberryPI

Simple Python driver for P9813 RGB LED strips on Raspberry Pi.

This library is made for this kind of modules (diymore RGB LED)
![RGB LED Strip Driver Module Shield](https://raw.githubusercontent.com/MrKrabat/LED-Strip-Driver-Module/master/images/shield.jpg "RGB LED Strip Driver Module Shield")

## Quick Setup

1. Install: pip install RPi.GPIO
2. Connect:
   LED VCC -> Raspberry Pi 3.3V
   LED GND -> Raspberry Pi GND
   LED DIN -> Raspberry Pi GPIO 23
   LED CIN -> Raspberry Pi GPIO 24
3. Test: python demo.py

## Basic Code Example

from led_strip_driver import LEDStripDriver

led = LEDStripDriver()
led.set_color(255, 0, 0)    # Red
led.set_color_hex("#00FF00") # Green
led.set_brightness(0.7)      # 70% brightness
led.clear()                  # Turn off

## Features

- Set any RGB color (0-255)
- Use HEX color codes
- Adjustable brightness
- Special effects:
  * Breathing (pulsing)
  * Rainbow colors
  * Police flashing lights
  * Smooth color fades

## Interactive Demo

Run: python demo.py

This gives you a menu to:
- Set colors manually
- Test all effects
- Adjust brightness
- Turn LED on/off

## Customize Pins

Use different GPIO pins:
led = LEDStripDriver(din_pin=17, cin_pin=27)

## Notes

- Works with P9813 chips
- Colors: Red, Green, Blue (0-255 each)
- Brightness: 0.0 (off) to 1.0 (max)
- Automatically cleans up on exit

## Files

- led_strip_driver.py - Main controller
- demo.py - Interactive test program
