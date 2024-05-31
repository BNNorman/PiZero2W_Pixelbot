# Neopixels

Nornmally the bot has a 12 led neopixel ring but the length can be set in Config.sys

All commands return True on success and False otherwise. On failure a message is displayed on stdout.

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




