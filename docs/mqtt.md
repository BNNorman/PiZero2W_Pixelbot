# mqtt.md

The Pixelbot code will attempt to connect to an mqtt broker specified in Config.py

Commands return True on success and False on failure - error messages will be output to stdout.

Config.py defines MQTT_TOPIC as the top level topic which all Pixelbots subscribe to.


## mqtt.add_callback(topic,cb)

Any messages received on the given topic will be passed to your callback function cb.

If the topic is specific to this Pixelbot, e.g. /pixelbot/<bot name> then messages can be published which target one particular bot. You could use this to control an individual bot from a laptop etc.

If cb is not callable the call will result in an emitted a message to the Pi stduot and return False.

The topic is subscribed to automatically.

```
def myCb(msg):
  print("Got message",msg)

mqtt.add_callback(topic,myCb)

```


## mqtt.publish(topic,msg)

Sends a string message to the specified topic.

The topic could be a path to another Pixelbot so they could exchange messages.

# Example Program

This very simplistic program allows you to send 'move' and 'rotate' commands vi MQTT to a Pixelbot on the topic "/pixelbot/motors".

If you have multiple Pixelbots you should include the Pixelbot name in the topic to listen only for commands targetting your Pixelbot. 

```
# define our callback function for controlling motors
def motorsCB(msg):
  # expecting a comma separated list cmd,p1[,p2,p3]
  params=msg.split(",")
  cmd=params[0].strip().upper()
  if cmd=="MOVE":
    if len(params)==3:
      motors.move(param[1],params[2])
    else:
      motors.move(param[1]) # default duration=0
  elif cmd=="ROTATE":
    if len(params)==3:
      motors.rotate(param[1],params[2])
    else:
      motors.rotate(param[1]) # default duration=0
  else:
      print(f"Unexpected command {cmd}")

# add the callback to listen for messages sent to
# this Pixelbot
mqtt.add_callback(f"/{myname()}/motors",motorsCB)

while True:
  # do nothing but don't use pass which will consume
  # cpu resources 
  time.sleep(0.1)

```
