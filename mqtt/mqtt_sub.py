import paho.mqtt.client as mqtt
import sys
from time import sleep


class MQTTSubscriber():
    """ Class responsible for the subscriptions """
    def __init__(self, **kw):
        """ Class builder """
        self._mqtt_broker = 'localhost' #kw['mqtt_host']
        self._port = 1883

    
    def subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client = mqtt.Client()
        client.on_message = on_message
        if client.connect(self._mqtt_broker, self._port, 60) !=0:
            print("\nCould not connect to MQTT Broker!")
            sys.exit(-1)
        else:
            print("\nSub Client connected...")

        topic = 'status'
        client.subscribe(topic)

        try:
            # print("\nSuccessfully Subscribed! Press CTRL+C to exit...\n")
            client.loop_forever()
        except:
            print("\nDisconnecting from broker...\n")

        client.disconnect()