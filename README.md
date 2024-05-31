# PiZero2W_Pixelbot

Using a Pi Zero &amp; Python to send commands to a Rob Miles pixelbot via a serial connection.

Actually, it's a lot more than that, you can upload a Python program and have the Pixelbot controlled from it.

Here's a sample program which allows the pixelbot to receive and act on messages from an mqtt broker. You could be sending it commands manually or Pixelbots could be talking to each other, or even just muttering to themselves.

```
From Colours import RED,GREEN,BLUE
import time

def mqttMotorCallback(msg):
  params=msg.split(",")
  cmd=params[0].toUpper()
  if cmd=="MF": #forward
    motors.move(int(params[1])) # distance, no duration
  elif cmd=="MA": # arc
    motors.arc(param[1],param[2])) # radius & angle, no duration

def mqttNeopixelCallback(msg):
  params=msg.split(",")
  cmd=params[0].toUpper()
  if cmd=="RANDOM":
    neopixels.random()
  else:
    neopixels.fill(param[1]) # assuming a colour name or rgb tuple

mqtt.add_callback("/pixelbot/motors", mqttMotorsCallback)
mqtt.add_callback("/pixelbot/neopixels",mqttNeopixelCallback)

while True:
  # you could send mqtt messages to yourself or to another pixelbot.
  mqtt.publish("/pixelbot/motors","MF,1000")  # motors forward 1000mm as fast as possible
  while motors.areMoving():
     time.sleep(0.1)
```

read the docs to find out what else you can do - the Pixelbot has a speaker and an ultrasonic distance sensor


  




```
