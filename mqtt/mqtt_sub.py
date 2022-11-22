from imports import mqtt, sys, awsmqtt, threading

locker = threading.Lock()


class MQTTSubscriber():
    """ Class responsible for the subscriptions """
    def __init__(self):
        """ Class builder """
        locker.acquire()
 
        #Mosquitto Broker and Paho-MQTT
        self._broker_addrs = '127.0.0.1'
        self._broker_port = 1883
        self._status_conn_mqtt = False

        #AWS IoT Core SDK
        self._aws_client_id = 'Device1'
        self._aws_endpoint = 'a13zffjlim5dan-ats.iot.us-east-1.amazonaws.com'
        self._aws_port = '8883'
        self._aws_certificate = 'D:\\AWS\\mbs2mqtt_certs\\modbus2mqtt-certificate.pem.crt'
        self._aws_privatekey = 'D:\\AWS\\mbs2mqtt_certs\\modbus2mqtt-private.pem.key'
        self._aws_rootca1 = 'D:\\AWS\\mbs2mqtt_certs\\AmazonRootCA1.pem'
        self._tls_encryption = False
        self._status_conn_mqtt_aws = False

        if self._tls_encryption:
            self._mqtt_client = awsmqtt.AWSIoTMQTTClient(self._aws_client_id)
        else:
            self._mqtt_client = mqtt.Client()
            
        locker.release()


    # def __init__(self, **kw):
    #     """ Class builder """
    #     self._mqtt_broker = 'localhost' #kw['mqtt_host']
    #     self._port = 1883
    #     self.client = mqtt.Client()

    
    def subscribe(self):
        print('wii')
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        
        try:
            
            self._mqtt_client.on_message = on_message
            if self._tls_encryption == True: #If it is a connection with TLS certificates
                self._mqtt_client.configureEndpoint(self._aws_endpoint, 8883)
                self._mqtt_client.configureCredentials(self._aws_rootca1, self._aws_privatekey, self._aws_certificate)
                if self._mqtt_client.connect():
                    print("\nSub Client connected...")
                    self._status_conn_mqtt_aws = True
                else:
                    print("Unable to establish connection with the MQTT Broker!")
            else:
                if self._mqtt_client.connect(self._broker_addrs, self._broker_port, 60) !=0:
                    print("\nCould not connect to MQTT Broker!")
                    sys.exit(-1)
                else:
                    print("\nSub Client connected...")

            topic = 'status'
            self._mqtt_client.subscribe(topic)
        except Exception as e: 
            print('MQTT ERROR: ', e.args)
        
        
        
        # try:
        #     # self.client = mqtt.Client()
        #     self._mqtt_client.on_message = on_message
            
        #     if self._mqtt_client.connect(self._mqtt_broker, self._port, 60) !=0:
        #         print("\nCould not connect to MQTT Broker!")
        #         sys.exit(-1)
        #     else:
        #         print("\nSub Client connected...")

        #     topic = 'status'
        #     self._mqtt_client.subscribe(topic)
        # except Exception as e: 
        #     print('MQTT ERROR: ', e.args)