import paho.mqtt.client as mqtt

import random

import json
import time

IOT_CORE_URL="a2phmx8h09d4mm-ats.iot.eu-central-1.amazonaws.com"
MQTT_TOPIC="test-device/temperature"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$aws/things/test-device/shadow/update")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("test_device")
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("ca.cert.pem", "certificate.pem.crt", "private.pem.key")
client.connect(IOT_CORE_URL, 8883, 60)

def get_message():
    temperature = random.randint(0, 30)

    print("Randomized {}".format(temperature))

    return {
        "temperature" : temperature,
        "ts" : int(time.time()),
        "sensorId" : "test-device"
    }

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

while True:
    time.sleep(10)

    client.publish(MQTT_TOPIC, json.dumps(get_message()))

