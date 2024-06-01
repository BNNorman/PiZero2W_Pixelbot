# Python Sources #

## PICO_Pixelbot

The PICO pixelbot needs to use Serial1 not Serial for this to work. Also uncomment #define DIAGNOSTICS_ACTIVE  in commands.h

## Wiring

The Pico TX/RX should then be wired TX-RX, RX-TX as usual, plus a common ground.

## Pi Zero

The Pi Zero needs to have shell messages disabled on the serial connection. Raspi-config will let you do that with the latest raspbian.

You also need to install paho-mqtt and pyserial (if not already installed)

## Running

The main program is HttpServer which presents an editor web page at localhost:8080. Of course, from a remote desktop etc, you should use the IP address acquired by the Pi Zero.

With the Pi Zero connected to a monitor/keyboard you can launch HttPServer.py manually using Thonny and watch any 
messages which appear on screen. Alternatively, you could use VNC to remotely do that.

To get the Pi running automatically you need to invest some time in setting up a systemd service. I haven't done that yet.

# Files

## Colours.py

Defines colours as RGB tuples.

## Config.py

Enter configuration data here.

## HttpServer.py

This module exposes an Editor webpage on localhost:8080 by default. Button presses are routed to the interpreter.py 
module to run the uploaded code (if it can)

## Interpreter

Provides an interface between your uploaded program and the HullOS.py module to allow you to read distance sensors, 
control the speaker sounds, neopixels and motors.

Your uploaded program is actually executed by the Python exec() function. If that fails (Exceptions) your program 
will exit. You should be able to restart it using the Run button on the editor web page.

## MicroPyServer.py

Provides an HTTP server used by the HttpServer module

## mqtt.py

Subscribes to an MQTT broker to allow passing messages between bots and/or a controller.

## SerialHandler.py

Sends HullOS commands to the Pixelbot and reads any responses. The Pixelbot needs to be compiled with 
DIAGNOSTICS_ACTIVE in /lib/commands/src/Commands.h. 

This module first checks that it can talk to a Pixelbot. 

## StoredScript.py

This is your last uploaded script. It will be run when you start the HttpServer module

## URLlib.py

Some basic url helpers - used to unquote uploaded programs before saving to StoredScript.py







