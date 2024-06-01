PIXELBOT_NAME="brian" # whatever you want yours to be known as

NETWORK="MAKERSPACE" # or "HOME"

######### Wifi ###########################
if NETWORK=="HOME":
	WIFI_SSID = "ssid"
	WIFI_PASS = "password"
elif NETWORK=="MAKERSPACE":
	WIFI_SSID = "ssid"
	WIFI_PASS = "password"
else:
	raise Exception(f"Unknown NETWORK {NETWORK}")

######## Webserver ########################
#
# make the Editor.html appear on localhost:8080
#
WEBSERVER_PORT=8080
WEBSERVER_PAGES="Web Pages"

####### MQTT ###########
#
# I use a laptop away from home and a wifi router
# programmed on 192.168.2.1. The laptop runs an open mosquitto
# MQTT broker
#
if NETWORK=="HOME":
	MQTT_BROKER="192.168.1.xxx"
	MQTT_USER="user"
	MQTT_PASS="pass"
elif NETWORK=="MAKERSPACE":
	MQTT_BROKER="192.168.2.xxx"
	MQTT_USER=None
	MQTT_PASS=None
else:
	raise Exception(f"Unknown NETWORK {NETWORK}")

# PiBots listen on their own sub-topc
# e.g. pixelbot/PIXELBOT_NAME
# this topic is automatically subscribed to
# but you will need to add a callback to get messages
# delivered OR you can add callbacks to your own topics

MQTT_TOPIC=f"/pixelbot/{PIXELBOT_NAME}"

####### Interpreter ########
#
# program loops are followed by a test to terminate
# thisd is the level of indenting required
PYTHON_INDENT=" "*4