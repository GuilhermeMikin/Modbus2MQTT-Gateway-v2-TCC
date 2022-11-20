import paho.mqtt.client as mqtt
import sys
from time import sleep


class MQTTSubscriber():
    """ Class responsible for the subscriptions """
    def __init__(self, **kw):
        """ Class builder """
        self._mqtt_broker = 'localhost' #kw['mqtt_host']
        self._port = 1883
        self.client = mqtt.Client()

    
    def subscribe(self):
        print('wii')
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        
        try:
            # self.client = mqtt.Client()
            self.client.on_message = on_message
            if self.client.connect(self._mqtt_broker, self._port, 60) !=0:
                print("\nCould not connect to MQTT Broker!")
                sys.exit(-1)
            else:
                print("\nSub Client connected...")

            topic = 'status'
            self.client.subscribe(topic)
        except Exception as e: 
            print('MQTT ERROR: ', e.args)

        # try:
        #     self.client.loop_start()
        # except:
        #     print("\nDisconnecting from broker...\n")

    # def disconnect_sub(self):
        # sleep(1)
        # self.client.loop_stop()
        # self.client.disconnect()
        # print( 'bye')