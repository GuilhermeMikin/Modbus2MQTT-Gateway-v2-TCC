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

    
    def subscribe(self, topic):
        """ Method responsible for the mqtt subscription """
        print(f'SubClient thread name = {threading.current_thread().getName()}')
        def on_message(client, userdata, msg): 
            self.readMessage(msg)

        try:
            self._mqtt_subscriber_client.on_message = on_message
            subscription_return = self._mqtt_subscriber_client.subscribe(topic)
            print(f'Subscribed to topic: {topic}')
            return subscription_return
        except Exception as e: 
            print('MQTT ERROR: ', e.args)


    def tlsSubscribe(self, topic):
        """ Method responsible for the mqtt subscription with TLS Encryption """
        print(f'TLSSubClient thread name = {threading.current_thread().getName()}')
        def customCallback(client, userdata, msg): 
            self.readMessage(msg)

        try:
            subscription_return = self._mqtt_subscriber_client.subscribe(topic, 1, customCallback)
            print(f'Subscribed to topic: {topic}')
            return subscription_return
        except Exception as e: 
            print('MQTT ERROR: ', e.args)

    
    def readMessage(self, msg):
        """ Read the msg payload and decides what to do """
        try:
            msg_str = msg.payload.decode()
            msg_itens = msg_str.split(' ')
            if msg_itens[0] == 'modbus':
                modbus_write_addr = int(msg_itens[2])
                modbus_write_value = int(msg_itens[4])
                try:
                    self._mqtt2mbsClient.write_single_register(modbus_write_addr -1, modbus_write_value)
                    print(f'Modbus message "{modbus_write_value}" successfully written in address {modbus_write_addr}')
                except Exception as e: 
                    print('Mbs ERROR: ', e.args)
            else:
                print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        except Exception as e: 
            print('ERROR handling message: ', e.args)
        
    