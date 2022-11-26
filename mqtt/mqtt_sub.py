from imports import threading

busy = threading.Lock()


class MQTTSubscriber():
    """ Class responsible for the subscriptions """
    def __init__(self, mqttClient):
        """ Class builder """
        busy.acquire()
        self._mqtt_subscriber_client = mqttClient
        busy.release()

    
    def subscribe(self, topic):
        print(f'SubClient thread name = {threading.current_thread().getName()}')
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")


        try:
            self._mqtt_subscriber_client.on_message = on_message
            subscription_return = self._mqtt_subscriber_client.subscribe(topic)
            print(f'Subscribed to topic: {topic}')
            return subscription_return
        except Exception as e: 
            print('MQTT ERROR: ', e.args)
        
        