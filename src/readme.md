# Python Sources #

## PICO_Pixelbot

The PICO pixelbot needs to use Serial1 not Serial for this to work. Also uncomment #define DIAGNOSTICS_ACTIVE  in commands.h

## Wiring

The Pico TX/RX should then be wired TX-RX, RX-TX as usual, plus a common ground.

## Pi Zero

The Pi Zero needs to have shell messages disabled on the serial connection. Raspi-config will let you do that with the latest raspbian.

You also need to install paho-mqtt, pyserial (if not already installed)

## Running

The main program is HttpServer which presents an editor web page at localhost:8080. Of course, from a remote desktop etc, you should use the IP address acquired by the Pi Zero.

With the Pi Zero connected to a monitor/keyboard you can launch HttPServer.py manually and watch any messages which appear on screen. Alternatively, you could use VNC to remotely do that.

To get the Pi running automatically you need to invest some time in setting up a systemd service. I haven't done that yet.

