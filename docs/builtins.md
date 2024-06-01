# Builtins

The Python interpreter has only the following builtin function calls available for your program.

## myname()

Returns the PIXELBOT_NAME as defined in Config.py. This is useful for MQTT callbacks to ensure the Pixelbot only responds to messages sent to itself.

## distance()

Returns the current distance (mm) from the distance sensor
