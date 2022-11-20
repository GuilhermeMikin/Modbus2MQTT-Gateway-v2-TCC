from imports import *

class Modbus2MqttClient():
    """ Main class responsible for the gateway """
    def __init__(self, **kw):
        """ Class builder """
        self._app = True
        self._atendimento = None
        self._mbs_client = ModbusClient(host=kw['modbus_Addrs'], port=kw['modbus_Port'], unit_id=1)
 
        #Mosquitto Broker and Paho-MQTT
        self._broker_addrs = kw['mqtt_broker_Addrs']
        self._broker_port = kw['mqtt_broker_Port']
        self._status_conn_mqtt = False

        #AWS IoT Core SDK
        self._aws_client_id = kw['awsiot_client_id']
        self._aws_endpoint = kw['awsiot_endpoint']
        self._aws_port = kw['awsiot_port']
        self._aws_certificate = kw['awsiot_path_to_certificate']
        self._aws_privatekey = kw['awsiot_path_to_private_key']
        self._aws_rootca1 = kw['awsiot_path_to_amazon_root_ca1']
        self._tls_encryption = kw['tls_encryption']
        self._status_conn_mqtt_aws = False

        if self._tls_encryption:
            self._mqtt_client = awsmqtt.AWSIoTMQTTClient(self._aws_client_id)
        else:
            self._mqtt_client = mqtt.Client() 

        #Aux variables to the thread responsible for the connection
        self._thread_connection = None
        self._connected_thread = False

        #Aux variables to the thread responsible for the subscription
        self._thread_subscriber = None
        self._subscribed_thread = False

        #Aux variables to the thread responsible for the publishing
        self._thread_publisher = None
        self._publishing_thread = False

        self.locker = threading.Lock()


    def ModbusMQTTConnect(self):
        """ Method actually responsible for connecting to Modbus and MQTT servers """
        try:
            self._mbs_client.open()
            print('\nModbus TCP  --> OK')
        except Exception as e: 
            print('Modbus Connection ERROR: ', e.args)

        try:
            if self._tls_encryption == True: #If it is a connection with TLS certificates
                self._mqtt_client.configureEndpoint(self._aws_endpoint, 8883)
                self._mqtt_client.configureCredentials(self._aws_rootca1, self._aws_privatekey, self._aws_certificate)
                if self._mqtt_client.connect():
                    msgstatus = dict()
                    msgstatus['Timestamp'] = str(dt.now())
                    msgstatus['Message'] = "Client connected!"
                    msg_json = json.dumps(msgstatus)
                    self._mqtt_client.publish(topic="connection/status", payload=msg_json, QoS= 1)
                    
                    #Creates the thread responsible for the main subscription
                    self._subscribed_thread = True
                    # self._thread_subscriber = threading.Thread(target=self.subscribe, args="status")
                    # self._thread_subscriber.start()
                    print('Subscribed to topic status...')
                    # self._thread_subscriber.join()
                    
                    print('MQTT ---------> OK')
                    self._status_conn_mqtt_aws = True
                else:
                    print("Unable to establish connection with the MQTT Broker!")
            else:
                if self._mqtt_client.connect(self._broker_addrs, self._broker_port, 60) != 0:
                    print("Unable to establish connection with MQTT Broker!")
                    sys.exit(-1)
                else:
                    msgstatus = dict()
                    msgstatus['Timestamp'] = str(dt.now())
                    msgstatus['Message'] = "Client connected!"
                    msg_json = json.dumps(msgstatus)
                    self.mqttPublisher(topic="connection/status", msg=msg_json)

                    #Creates the thread responsible for the main subscription
                    try:
                        self._subscribed_thread = True
                        self._thread_subscriber = threading.Thread(target=self.subscribe)
                        self._thread_subscriber.start()
                        # self._thread_subscriber.join()
                        print('Successfully subscribed to topic status...')
                    except Exception as e: 
                        print('Subscription ERROR: ', e.args)

                    print('MQTT ---------> OK')
                    self._status_conn_mqtt = True
        except Exception as e: 
            print('MQTT ERROR: ', e.args)
            print("\nUnable to establish connection with MQTT Broker!\nCheck if the IP Address is OK and try again...")
            print('Following without connection with MQTT Broker..')


    def disconnect(self):
        try:
            msgstatus = dict()
            msgstatus['Timestamp'] = str(dt.now())
            msgstatus['Message'] = "Client disconnected!"
            msg_json = json.dumps(msgstatus)
            if self._status_conn_mqtt:
                self.mqttPublisher(topic="connection/status", msg=msg_json)
            elif self._status_conn_mqtt_aws:
                self.awsMqttPublisher(topic="connection/status", msg=msg_json)
            else:
                pass
            self._connecting_thread = False
            self._publishing_thread = False
            self._subscribing_thread = False
            self._mqtt_client.disconnect()
            self._atendimento = False
            self._app = False
            self._status_conn_mqtt = False
            self._status_conn_mqtt_aws = False
            print("\nThe client is now disconnected...")
        except Exception as e:
            print('ERROR disconnecting: ', e.args)


    def readMbsData(self, tipo, addr, leng=1):
        """
        Método para leitura MODBUS
        """
        try:
            if tipo == 1:
                co = self._mbs_client.read_coils(addr - 1, leng)
                return co
            elif tipo == 2:
                di = self._mbs_client.read_discrete_inputs(addr - 1, leng)
                return di
            elif tipo == 3:
                hr = self._mbs_client.read_holding_registers(addr - 1, leng)
                return hr
            elif tipo == 4:
                ir = self._mbs_client.read_input_registers(addr - 1, leng)
                return ir
            else:
                print('Not Found...')
        except Exception as e:
            print('ERROR reading Mbs Data: ', e.args)

    def readMbsF32Data(self, tipo, addr, leng=1):
        """
        Método para conversão FLOAT MODBUS
        """
        try:
            i = 0
            g = 0
            e1 = []
            listfloat = []
            while i < leng:
                if tipo == 3:
                    modbusvalues = self._mbs_client.read_holding_registers(addr - 1 + g, 2)
                elif tipo == 4:
                    modbusvalues = self._mbs_client.read_input_registers(addr - 1 + g, 2)
                else:
                    print('Data type do not supports F32')
                for value in modbusvalues:
                    binvalue = bin(value).lstrip("0b")
                    e1.insert(0 + g, binvalue)
                i += 1
                g += 2
            e = 0
            while e <= leng:
                e2 = ''
                for binvalue in e1:
                    e2 = str(f'{e2}{binvalue.rjust(16, "0")} ')
                e += 1
            b2 = str(f'{e2}')
            e3 = b2.split()
            y = 0
            while y < len(e3):
                ieee = f'{e3[0+y]}{e3[1+y]}'
                sign = int(ieee[0])
                expo = str(ieee[1:9])
                expodec = 0
                expopot = 7
                for i in range(8):
                    expodec = expodec + (int(expo[i]) * (2**expopot))
                    expopot -= 1
                mant = str(ieee[9:])
                mantdec = 0
                mantpot = -1
                for i in range(23):
                    mantdec = mantdec + (int(mant[i]) * (2 ** mantpot))
                    mantpot -= 1
                value = ((-1)**sign)*(1+mantdec)*2**(expodec-127)
                listfloat.append(round(value, 3))
                y += 2
        except Exception as e:
            print('ERROR converting FLOAT32: ', e.args, f'listfloat var {listfloat} >> {modbusvalues} addr {addr}')
            if tipo == 1:
                co = self._mbs_client.read_coils(addr - 1, leng)
                return co
            elif tipo == 2:
                di = self._mbs_client.read_discrete_inputs(addr - 1, leng)
                return di
            elif tipo == 3:
                hr = self._mbs_client.read_holding_registers(addr - 1, leng)
                return hr
            elif tipo == 4:
                ir = self._mbs_client.read_input_registers(addr - 1, leng)
                return ir
            else:
                print('Not Found...')


    def writeMbsData(self, tipo, addr, valor):
        """
        Método para escrita MODBUS
        """
        try:
            if tipo == 1:
                return self._mbs_client.write_single_coil(addr - 1, valor)
            elif tipo == 2:
                return self._mbs_client.write_single_register(addr - 1, valor)
            else:
                print('Invalid writing type..\n')
        except Exception as e:
            print('ERROR writing mbs message: ', e.args)


    def mbs2mqttGateway(self,modbus_type,
                        modbus_read_addr1,modbus_read_length1,
                        modbus_read_addr2,modbus_read_length2,
                        modbus_read_addr3,modbus_read_length3,
                        modbus_read_addr4,modbus_read_length4,
                        mqtt_pub_topic1,mqtt_pub_topic2,
                        mqtt_pub_topic3,mqtt_pub_topic4,
                        manual_gates, json_gates, json_file_path,
                        type_display1,type_display2,
                        type_display3,type_display4):
        """
        Método para leitura modbus e publicação mqtt
        """
        try:
            try:
                with open(json_file_path) as file:
                    data = json.load(file)
                if self._status_conn_mqtt:
                    self.mqttPublisher(topic=data["System Description"]['Topic'], msg=json.dumps(data["System Description"]))
                elif self._status_conn_mqtt_aws:
                    self.awsMqttPublisher(topic=data["System Description"]['Topic'], msg=json.dumps(data["System Description"]))
                else:
                    print('Problem with the MQTT connection...')
                    sleep(1)
            except Exception as e:
                print('ERROR reading Json: ', e.args, end='')
            while self._publishing_thread:
                if manual_gates[0]:
                    if type_display1:
                        modbusValues1 = self.readMbsF32Data(int(modbus_type),int(modbus_read_addr1),modbus_read_length1)
                    else:
                        modbusValues1 = self.readMbsData(int(modbus_type),int(modbus_read_addr1),modbus_read_length1)
                    msg_dict = dict()
                    msg_dict['Timestamp'] = str(dt.now())
                    msg_dict['Value'] = self.cleanMessage(modbusValues1)
                    msg_dict['Unity'] = '-'
                    msg_dict['Modbus Address'] = modbus_read_addr1
                    msg_dict['Modbus Length'] = modbus_read_length1
                    msg_dict['Modbus Function Code'] = modbus_type
                    msg_dict['Modbus Data Display'] = ('F32' if type_display1 else 'UINT16')
                    msg_dict['MQTT Topic'] = mqtt_pub_topic1
                    msg_json = json.dumps(msg_dict)
                    if self._status_conn_mqtt:
                            self.mqttPublisher(topic=mqtt_pub_topic1, msg=msg_json)
                    elif self._status_conn_mqtt_aws:
                        self.awsMqttPublisher(topic=mqtt_pub_topic1, msg=msg_json)
                    else:
                        print('Problem with the MQTT connection...')
                        sleep(1)
                if manual_gates[1]:
                    if type_display2:
                        modbusValues2 = self.readMbsF32Data(int(modbus_type),int(modbus_read_addr2),modbus_read_length2)
                    else:
                        modbusValues2 = self.readMbsData(int(modbus_type),int(modbus_read_addr2),modbus_read_length2)
                    msg_dict = dict()
                    msg_dict['Timestamp'] = str(dt.now())
                    msg_dict['Value'] = self.cleanMessage(modbusValues2)
                    msg_dict['Unity'] = '-'
                    msg_dict['Modbus Address'] = modbus_read_addr2
                    msg_dict['Modbus Length'] = modbus_read_length2
                    msg_dict['Modbus Function Code'] = modbus_type
                    msg_dict['Modbus Data Display'] = ('F32' if type_display2 else 'UINT16')
                    msg_dict['MQTT Topic'] = mqtt_pub_topic2
                    msg_json = json.dumps(msg_dict)
                    if self._status_conn_mqtt:
                        self.mqttPublisher(topic=mqtt_pub_topic2, msg=msg_json)
                    elif self._status_conn_mqtt_aws:
                        self.awsMqttPublisher(topic=mqtt_pub_topic2, msg=msg_json)
                    else:
                        print('Problem with the MQTT connection...')
                        sleep(1)
                if manual_gates[2]:
                    if type_display3:
                        modbusValues3 = self.readMbsF32Data(int(modbus_type),int(modbus_read_addr3),modbus_read_length3)
                    else:
                        modbusValues3 = self.readMbsData(int(modbus_type),int(modbus_read_addr3),modbus_read_length3)
                    msg_dict = dict()
                    msg_dict['Timestamp'] = str(dt.now())
                    msg_dict['Value'] = self.cleanMessage(modbusValues3)
                    msg_dict['Unity'] = '-'
                    msg_dict['Modbus Address'] = modbus_read_addr3
                    msg_dict['Modbus Length'] = modbus_read_length3
                    msg_dict['Modbus Function Code'] = modbus_type
                    msg_dict['Modbus Data Display'] = ('F32' if type_display3 else 'UINT16')
                    msg_dict['MQTT Topic'] = mqtt_pub_topic3
                    msg_json = json.dumps(msg_dict)
                    if self._status_conn_mqtt:
                        self.mqttPublisher(topic=mqtt_pub_topic3, msg=msg_json)
                    elif self._status_conn_mqtt_aws:
                        self.awsMqttPublisher(topic=mqtt_pub_topic3, msg=msg_json)
                    else:
                        print('Problem with the MQTT connection...')
                        sleep(1)
                if manual_gates[3]:
                    if type_display4:
                        modbusValues4 = self.readMbsF32Data(int(modbus_type),int(modbus_read_addr4),modbus_read_length4)
                    else:
                        modbusValues4 = self.readMbsData(int(modbus_type),int(modbus_read_addr4),modbus_read_length4)
                    msg_dict = dict()
                    msg_dict['Timestamp'] = str(dt.now())
                    msg_dict['Value'] = self.cleanMessage(modbusValues4)
                    msg_dict['Unity'] = '-'
                    msg_dict['Modbus Address'] = modbus_read_addr4
                    msg_dict['Modbus Length'] = modbus_read_length4
                    msg_dict['Modbus Function Code'] = modbus_type
                    msg_dict['Modbus Data Display'] = ('F32' if type_display4 else 'UINT16')
                    msg_dict['MQTT Topic'] = mqtt_pub_topic4
                    msg_json = json.dumps(msg_dict)
                    if self._status_conn_mqtt:
                        self.mqttPublisher(topic=mqtt_pub_topic4, msg=msg_json)
                    elif self._status_conn_mqtt_aws:
                        self.awsMqttPublisher(topic=mqtt_pub_topic4, msg=msg_json)
                    else:
                        print('Problem with the MQTT connection...')
                        sleep(1)
                if json_gates:
                    try:
                        for var in data:
                            if var == 'System Description':
                                pass
                            else:
                                if str(data[var]['Type']) == 'F32':
                                    modbusValues = self.readMbsF32Data(int(modbus_type),int(data[var]['Address']),data[var]['Length'])
                                else:
                                    modbusValues = self.readMbsData(int(modbus_type),int(data[var]['Address']),data[var]['Length'])
                                msg_dict = dict()
                                msg_dict['Timestamp'] = str(dt.now())
                                msg_dict['Physical Quantity'] = var
                                msg_dict['Value'] = self.cleanMessage(modbusValues)
                                msg_dict['Unity'] = data[var]['Unity']
                                msg_dict['Modbus Address'] = int(data[var]['Address'])
                                msg_dict['Modbus Length'] = data[var]['Length']
                                msg_dict['Modbus Function Code'] = modbus_type
                                msg_dict['Modbus Data Display'] = data[var]['Type']
                                msg_dict['MQTT Topic'] = data[var]['Topic']
                                msg_json = json.dumps(msg_dict)
                                if self._status_conn_mqtt:
                                    self.mqttPublisher(topic=data[var]['Topic'], msg=msg_json)
                                elif self._status_conn_mqtt_aws:
                                    self.awsMqttPublisher(topic=data[var]['Topic'], msg=msg_json)
                                else:
                                    print('Problem with the MQTT connection...')
                                    sleep(1)
                    except Exception as e:
                        print(f'ERROR json {msg_json}: ', e.args, end='')
        except Exception as e:
            print('ERROR: ', e.args, end='')
            print('Error when trying to publish to broker, please check IP address and port...')


    def cleanMessage(self, message_from_modbus):
        """
        Takes off the brackets from the message
        """
        try:
            message = str(message_from_modbus)[1:-1]
        except Exception as e:
            print(f'ERROR when cleaning the mdbs message: ', e.args, end='')
        return message


    def mqttPublisher(self, topic, msg):
        """
        Método para publicação MQTT
        """
        try:
            if self._mqtt_client.connect(self._broker_addrs, self._broker_port, 60) != 0:
                print("Unable to establish connection with MQTT Broker!")
                sys.exit(-1)
            self._mqtt_client.publish(topic, msg)
        except Exception as e:
            print('ERROR: ', e.args, end='')
            print('Error when trying to publish to broker, please check IP address and port...')
            self._status_conn_mqtt = False


    def awsMqttPublisher(self, topic, msg):
        """
        Método para publicação MQTT via IoT Core
        """
        try:
            self._mqtt_client.publish(topic, msg, 1)
            print('.')
        except Exception as e:
            print('ERROR: ', e.args, end='')
            print('Error when trying to publish to AWS IoT, please check the configs...')
            self._status_conn_mqtt_aws = False


    def subscribe(self):
        def on_message(client, userdata, msg):
            self.locker.acquire()
            self.mqttPublisher("test/subscription","Payload received...")
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.locker.release()

        self._mqtt_client.subscribe("status")
        self._mqtt_client.on_message = on_message




        
