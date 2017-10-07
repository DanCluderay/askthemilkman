
import paho.mqtt.client as mqtt

def make_mqtt_call(topic, payload):
    if topic=="":
        topic="cluderay"
    else:
        topic = "cluderay/" + topic
    print("MQTT TOPIC - " + str(topic))
    client = mqtt.Client("dancluderay111174")
    client.connect("test.mosquitto.org")
    client.publish(topic, str(payload))
    return str(payload)