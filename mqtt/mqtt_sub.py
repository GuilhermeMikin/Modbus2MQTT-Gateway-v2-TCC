from imports import threading

busy = threading.Lock()


class MQTTSubscriber():
    """ Class responsible for the subscriptions """
    def __init__(self, mqttClient, modbus_client):
        """ Class builder """
        busy.acquire()
        self._mqtt_subscriber_client = mqttClient
        self._mqtt2mbsClient = modbus_client
        busy.release()

    
    def subscribe(self, topic, modbus_client):
        print(f'SubClient thread name = {threading.current_thread().getName()}')
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
            write_modbus = True
            modbus_write_addr = 1225
            modbus_write_value = 4545
            if write_modbus:
                try:
                    self._mqtt2mbsClient.write_single_register(modbus_write_addr -1, modbus_write_value)
                    print('Modbus message written')
                except Exception as e: 
                    print('Mbs ERROR: ', e.args)

        try:
            self._mqtt_subscriber_client.on_message = on_message
            subscription_return = self._mqtt_subscriber_client.subscribe(topic)
            print(f'Subscribed to topic: {topic}')
            return subscription_return
        except Exception as e: 
            print('MQTT ERROR: ', e.args)
        
        