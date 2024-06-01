import paho.mqtt.client as paho_client
from paho.mqtt.enums import CallbackAPIVersion
from Config import MQTT_BROKER, MQTT_USER, MQTT_PASS, MQTT_TOPIC


class MQTT_CLIENT():
    def __init__(self):
        self.mqttc = paho_client.Client(CallbackAPIVersion.VERSION1)
        self.broker_connected = False
        self.on_message_routes = {}
        
        self.connect_to_broker()

    def add_callback(self, sub_topic, cb):
        # the top level is /pixelbot/<PIXELBOT_NAME>
        if not callable(cb):
            print("MQTT add_callback cb is not callable")
            return False
        self.on_message_routes[sub_topic] = cb
        
        #self.subscribe(sub_topic)
        return True

    def del_callback(self, topic, cb):
        # if not callable burp
        try:
            del self.on_message_routes[topic]
            return True
        except:
            return False
        
    def on_connect(self, mqttc, obj, flags, rc):
        if rc == 0:
            print("MQTT on_connect")
            self.broker_connected = True
            self.mqttc.subscribe(MQTT_TOPIC)

        else:
            raise Exception(f"MQTT broker on_connect error {rc}")

    def on_disconnect(self):
        self.mqttc.loop_stop()
        self.broker_connected = False

    def on_message(self, mqttc, obj, msg):
        print(f"on_message topic={msg.topic} payload={msg.payload}")
        if self.on_message_routes[msg.topic]:
            f = self.on_message_routes[msg.topic]
            f(msg.payload.decode("utf-8"))
        else:
            print(f"No callback found for topic {msg.topic}")

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("MQTT on_subscribed")

    def publish(self, topic, msg):
        self.mqttc.publish(topic, msg.encode("utf-8"))

    def subscribe(self, topic):
        self.mqttc.subscribe(topic)

    def connect_to_broker(self):
        if self.broker_connected:
            print("Already connected to broker")
            return

        if MQTT_USER is not None:
            self.mqttc.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_subscribe = self.on_subscribe

        self.mqttc.loop_start()  # background thread
        self.mqttc.connect(MQTT_BROKER)

    def isConnected(self):
        return self.broker_connected

    def stop(self):
        self.mqttc.disconnect()


if __name__ == "__main__":
    import time

    mqtt = MQTT_CLIENT()


    def callback(msg):
        print("my added callback", msg)


    mqtt.add_callback(MQTT_TOPIC, callback)

    print("range 5", range(5))

    try:
        for m in range(5):
            mqtt.publish(MQTT_TOPIC, f"brian says hello {m}")
            time.sleep(1)

    except:
        mqtt.stop()
