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

