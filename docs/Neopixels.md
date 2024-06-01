# Neopixels

Normally the Pixelbot, as designed, has a 12 led neopixel ring but the length can be set in Config.sys

All commands return True on success and False otherwise. On failure a message is displayed on stdout. If you are monitoring the Pixelbot using Thonny (or similar) the messages appear in the REPL window.

## neopixels.colourCandle(colour)

colour may be an rgb tuple (r,g,b) or a named colour ("R","G","B","Y","M","C","W","K"). The neopixels will all be set to the same colour but with gentle flickering.

## neopixels.flicker(speed)

This command controls the speed of flickering. Speed should have a value between 1 and 20

## neopixels.off()

Turns off the neopixels.

## neopixels.setPixel(index,rgb)

Sets the indicated pixel to the specified colour (rgb tuple).

## neopixels.crossfade(speed,rgb)

The pixels are crossfaded at the given speed to the target rgb tuple.

## neopixel.animate(enable)

Enables or disbles flickering

## neopixels.random()

Randomise the colours of the neopixels.

# Example program

This simple loop just changes the neopixel colours. In Rob Mile's original design GREEN signifies a HAPPY Pixelbot and RED an ANGRY Pixelbot. Do what ever you want.

```
from Colours import RED,GREEN,BLUE
import time

while True: 
  neopixels.colourCandle(RED)
  time.sleep(1)
  neopixels.colourCandle(GREEN)
  time.sleep(1)
  neopixels.colourCandle(BLUE)
  time.sleep(1)
  neopixels.random()
  time.sleep(1)


```








