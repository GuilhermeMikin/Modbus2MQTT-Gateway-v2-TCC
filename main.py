from imports import *
from mb2mqtt import Modbus2MqttClient
from mqtt.mqtt_sub import MQTTSubscriber
# from login import LoginApp 
Config.set('kivy', 'exit_on_escape', '0')


class MyWidget(MDScreen):
    """
    Main interface builder
    """
    def __init__(self, **kw):
        super().__init__(**kw)
                                                    

    def connection(self): #Function to connnect to the modbus network and stablish a connection with the mqtt broker
        """ Main connection method. Responsible for updating the interface and calling the client class connection method"""
        try:
            if self.ids.bt_con.text == "  CONNECT  ": #If the application is disconnected 
                try:
                    Window.set_system_cursor("wait")  #Change the cursor to wainting mode
                    connection_params = { #Get the connection parameters from the user input
                        'modbus_Addrs' : self.ids.hostmodbus.text,
                        'modbus_Port' : int(self.ids.portmodbus.text),      
                        'mqtt_broker_Addrs' : self.ids.hostmqtt.text,       
                        'mqtt_broker_Port' : int(self.ids.portmqtt.text),
                        'mqtt_broker_user' : self.ids.hostmqttuser.text,
                        'mqtt_broker_pw' : self.ids.hostmqttpw.text,  
                        'awsiot_endpoint' : self.ids.awsendpoint.text,
                        'awsiot_port' : int(self.ids.awsport.text),
                        'awsiot_client_id' : self.ids.awsclientid.text,
                        'awsiot_path_to_certificate' : self.ids.awscert.text,
                        'awsiot_path_to_private_key' : self.ids.awsprivkey.text,
                        'awsiot_path_to_amazon_root_ca1' : self.ids.awsca1.text,
                        'tls_encryption' : (True if self.ids.check_tls.active else False)
                        }
                    self._mb2mqttClient = Modbus2MqttClient(**connection_params) #Pass the arguments to the Modbus2MQRR Client's constructor class
                    # self._mb2mqttClient.ModbusMQTTConnect() #Calls the newly created client connection function
                    ######
                    self._mb2mqttClient._connecting_thread = True
                    self._mb2mqttClient._thread_connection = threading.Thread(target=self._mb2mqttClient.ModbusMQTTConnect, name='Thred Connection')
                    self._mb2mqttClient._thread_connection.start()
                    sleep(2)
                    self.ids.bt_con.text = "DISCONNECT"   #After connected, it changes the button text to "disconnect"
                    if self._mb2mqttClient._status_conn_mqtt == True or self._mb2mqttClient._status_conn_mqtt_aws == True: #If it has successfully connected
                        Snackbar(text = "Successfully connected!", bg_color=(0,1,0,1)).open()
                    else:
                        Snackbar(text = "Modbus connected successfully, but a connection to the MQTT Broker could not be established...", bg_color=(0,0,1,1)).open()
                    self.ids.img_con.source = 'imgs/conectado.png'
                    Window.set_system_cursor("arrow")
                except Exception as e:
                    Window.set_system_cursor("arrow")
                    print(f"Error connecting to server: ",e.args)
                    Snackbar(text = f"Error connecting to server! ERROR: {e.args}", bg_color=(1,0,0,1)).open()
            elif self.ids.bt_con.text == "DISCONNECT":
                self.ids.bt_con.text = "  CONNECT  "
                self.ids.img_con.source = 'imgs/desconectado.png'
                Snackbar(text = "Client disconnected!", bg_color=(1,0,0,1)).open()
                self._mb2mqttClient.disconnect()
                # self._mb2mqttClient._thread_connection.stop()
            else:
                Snackbar(text = "Something went wrong!", bg_color=(1,0,0,1)).open()
        except Exception as e:
            print(f"Error connecting to server: ",e.args)
    
    def gateway(self):
        if self.ids.bt_con.text == "DISCONNECT":
            if self.ids.bt_readpub.text == "Start Reading/Publishing":
                self.ids.bt_readpub.text = "STOP Reading/Publishing"
                Window.set_system_cursor("wait")
                modbus_type = 3
                gate1 =(True if self.ids.checkgate1.active else False)
                gate2 =(True if self.ids.checkgate2.active else False)
                gate3 =(True if self.ids.checkgate3.active else False)
                gate4 =(True if self.ids.checkgate4.active else False)
                manual_gates = (gate1,gate2,gate3,gate4)
                json_gates = (True if self.ids.checkjson.active else False)
                json_file_path = self.ids.jsonpath.text
                modbus_read_addr1 = int(self.ids.modbusaddr1.text)
                modbus_read_length1 = int(self.ids.lengthpub1.text)
                modbus_type_display1 = self.ids.modbustd1.active
                mqtt_pub_topic1 = self.ids.topic1.text
                modbus_read_addr2 = int(self.ids.modbusaddr2.text)
                modbus_read_length2 = int(self.ids.lengthpub2.text)
                modbus_type_display2 = self.ids.modbustd2.active
                mqtt_pub_topic2 = self.ids.topic2.text
                modbus_read_addr3 = int(self.ids.modbusaddr3.text)
                modbus_read_length3 = int(self.ids.lengthpub3.text)
                modbus_type_display3 = self.ids.modbustd3.active
                mqtt_pub_topic3 = self.ids.topic3.text
                modbus_read_addr4 = int(self.ids.modbusaddr4.text)
                modbus_read_length4 = int(self.ids.lengthpub4.text)
                modbus_type_display4 = self.ids.modbustd4.active
                mqtt_pub_topic4 = self.ids.topic4.text
                try:
                    try:
                        self._mb2mqttClient._publishing_thread = True
                        self._mb2mqttClient._thread_publisher = threading.Thread(target=self._mb2mqttClient.mbs2mqttGateway, name='Thread Gateway',args=(
                            modbus_type,modbus_read_addr1,modbus_read_length1,
                            modbus_read_addr2,modbus_read_length2,
                            modbus_read_addr3,modbus_read_length3,
                            modbus_read_addr4,modbus_read_length4,
                            mqtt_pub_topic1,mqtt_pub_topic2,
                            mqtt_pub_topic3,mqtt_pub_topic4,
                            manual_gates, json_gates, json_file_path,
                            modbus_type_display1,modbus_type_display2,
                            modbus_type_display3,modbus_type_display4))
                        self._mb2mqttClient._thread_publisher.start()
                        Snackbar(text = f"Reading has started and data is being published to the specified topic...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                        Window.set_system_cursor("arrow")
                    except Exception as e: 
                        Window.set_system_cursor("arrow")
                        print('ERROR creating gateway thread: ', e.args)
                    # try:   
                    #     topic2 = f'test'
                    #     # mqtt_gw_sub_thread = MQTTSubscriber(self._mb2mqttClient._mqtt_client)
                    #     # self._mqtt_gw_sub_thread = MQTTSubscriber(self._mb2mqttClient._mqtt_client)
                    #     # self._thread_gw_subscriber = threading.Thread(target=self._mb2mqttClient.subscribe, name='Thread GW Subscriber', args=(topic2,))
                    #     # self._thread_gw_subscriber.start()
                    #     # self._mqtt_gw_sub_thread._mqtt_client.loop_start()
                    #     # print('GW-Subscriber client created AND INICIATED')
                    #     # self._mqtt_gw_sub_thread._mqtt_client.loop_start()
                    # except Exception as e: 
                    #     Window.set_system_cursor("arrow")
                    #     # self._mqtt_gw_sub_thread._mqtt_client.loop_stop()
                    #     print('ERROR creating gateway-subscriber thread: ', e.args)
                except Exception as e: 
                    Window.set_system_cursor("arrow")
                    print('ERROR: ', e.args)
                    Snackbar(text = f"Could not start gateway! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
            else:
                try:
                    self.ids.bt_readpub.text = "Start Reading/Publishing"
                    self._mb2mqttClient._publishing_thread = False
                    # mqtt_gw_sub_thread._mqtt_client.loop_stop()
                    # self._mqtt_gw_sub_thread._mqtt_client.loop_stop()
                    Snackbar(text = f"Stopping reading...", bg_color=(1,0,0,1), size_hint_y=0.05).open()
                except Exception as e:
                    print('ERROR: ', e.args)
                    Snackbar(text = f"Could not stop reading! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
        else:
            Snackbar(text = f"Could not read! Modbus Client is not connected", bg_color=(1,0,0,1)).open()

    
    def pub(self):
        if self.ids.bt_con.text == "DISCONNECT":
            Window.set_system_cursor("wait")
            mqtt_pub_msg = self.ids.msgpub.text
            mqtt_pub_topic = self.ids.topic.text
            try:
                if self._mb2mqttClient._status_conn_mqtt:
                    self._mb2mqttClient.mqttPublisher(topic=mqtt_pub_topic, msg=mqtt_pub_msg)
                    Snackbar(text = f"Message successfully published to topic {mqtt_pub_topic}...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                    Window.set_system_cursor("arrow")
                elif self._mb2mqttClient._status_conn_mqtt_aws:
                    self._mb2mqttClient.awsMqttPublisher(topic=mqtt_pub_topic, msg=mqtt_pub_msg)
                    Snackbar(text = f"Message successfully published to topic {mqtt_pub_topic}...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                    Window.set_system_cursor("arrow")
                else:
                    print('Problem with the MQTT connection...')
            except Exception as e: 
                Window.set_system_cursor("arrow")
                print('ERROR: ', e.args)
                Snackbar(text = f"Could not publish! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
        else:
            Snackbar(text = f"Could not publish! Client is not connected", bg_color=(1,0,0,1)).open()


    def sub(self):
        if self.ids.bt_con.text == "DISCONNECT":
            if self.ids.bt_subscribe.text == " Subscribe ":
                self.ids.bt_subscribe.text = "Unsubscribe"
                Window.set_system_cursor("wait")
                mqtt_sub_topic = self.ids.topic_sub.text
                try:
                    self._mb2mqttClient._subscribing_thread = True
                    self._mb2mqttClient._thread_subscriber = threading.Thread(target=self._mb2mqttClient.mqttSubscriber, args=(mqtt_sub_topic))
                    self._mb2mqttClient._thread_subscriber.start()
                    Snackbar(text = f"Subscribed to topic {mqtt_sub_topic} successfully...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                    Window.set_system_cursor("arrow")
                except Exception as e: 
                    Window.set_system_cursor("arrow")
                    print('ERROR: ', e.args)
                    Snackbar(text = f"Could not start subscription! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
            else:
                try:
                    self.ids.bt_subscribe.text = " Subscribe "
                    self._mb2mqttClient._subscribing_thread = False
                    Snackbar(text = f"Stopping subscription...", bg_color=(1,0,0,1), size_hint_y=0.05).open()
                except Exception as e:
                    print('ERROR: ', e.args)
                    Snackbar(text = f"Could not stop subscription! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
        else:
            Snackbar(text = f"Could not read! Modbus Client is not connected", bg_color=(1,0,0,1)).open()



    def write(self):
        if self.ids.bt_con.text == "DISCONNECT":
            Window.set_system_cursor("wait")
            modbus_type = 1 if self.ids.checkcoil.active == True else 2
            modbus_write_addr = int(self.ids.modbusaddrwrite.text)
            modbus_write_value = int(self.ids.modbusvaluewrite.text)
            try:
                self._mb2mqttClient.writeMbsData(modbus_type, modbus_write_addr, modbus_write_value)
                Snackbar(text = f"{modbus_write_value} written at the specified address ({modbus_write_addr})", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                Window.set_system_cursor("arrow")
            except Exception as e:
                Window.set_system_cursor("arrow")
                print('ERROR: ', e.args)
                Snackbar(text = f"Could not write! ERROR: {e.args}", bg_color=(1,0,0,1)).open()
        else:
            Snackbar(text = f"Could not write! Modbus Client is not connected", bg_color=(1,0,0,1)).open()


    def read(self):
        if self.ids.bt_con.text == "DISCONNECT":
            Window.set_system_cursor("wait")
            modbus_type = 3
            modbus_read_addr = int(self.ids.modbusaddrread.text)
            modbus_read_length = int(self.ids.length.text)
            try:    
                if self.ids.modbustdisplayF32.active:
                    modbus_reads = self._mb2mqttClient.readMbsF32Data(modbus_type, modbus_read_addr, modbus_read_length)
                else:
                    modbus_reads = self._mb2mqttClient.readMbsData(modbus_type, modbus_read_addr, modbus_read_length)
                self.ids.modbus_reads.text = f"Read: {modbus_reads}"
                Snackbar(text = f"Successfully read from address {modbus_read_addr} to {modbus_read_addr+modbus_read_length-1}", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                Window.set_system_cursor("arrow")
            except Exception as e: 
                Window.set_system_cursor("arrow")
                print('ERROR: ', e.args)
                Snackbar(text = f"Could not read! ERROR: {e.args}", bg_color=(1,0,0,1)).open()
        else:
            Snackbar(text = f"Could not read! Modbus Client is not connected", bg_color=(1,0,0,1)).open()

    
    def config(self):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text='Aqui vão algumas futuras configurações'))
        box2 = BoxLayout(orientation='horizontal', spacing = "10dp")
        button_ok = Button(text='Config', size_hint=(1, 0.6))
        button_cancel = Button(text='Cancel', size_hint=(1, 0.6))
        box2.add_widget(button_ok)
        box2.add_widget(button_cancel)
        box.add_widget(box2)
        popup = Popup(title='Settings', content=box, size_hint=(None, None), size=(300, 120))
        button_cancel.bind(on_release=popup.dismiss)
        popup.open()
        pass



class Mbs2MQTTApp(MDApp):
    """
    Classe com o aplicativo
    """
    def build(self):
        """
        Método que gera o aplicativo com o widget principal
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"
        Window.bind(on_request_close=self.on_request_close)
        return MyWidget()

    
    def on_request_close(self, *args):
        self.textpopup(title='Exit', text='Are you sure?')
        return True


    def textpopup(self, title='', text=''):
        box = BoxLayout(orientation='vertical')
        box.add_widget(Label(text=text))
        box2 = BoxLayout(orientation='horizontal', spacing = "10dp")
        button_ok = Button(text='OK', size_hint=(1, 0.6))
        button_cancel = Button(text='Cancel', size_hint=(1, 0.6))
        box2.add_widget(button_ok)
        box2.add_widget(button_cancel)
        box.add_widget(box2)
        popup = Popup(title=title, content=box, size_hint=(None, None), size=(300, 120))
        button_ok.bind(on_release= self.stop)
        button_cancel.bind(on_release=popup.dismiss)
        popup.open()


class Content(MDBoxLayout):
    manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass

if __name__ == '__main__':
    application_thread = threading.Thread(target=Mbs2MQTTApp().run(), name='Thread GUI')
    application_thread.start()
    application_thread.join()
    # Mbs2MQTTApp().run()
    # LoginApp()
    # if MyWidget.loggedin:
    #     Mbs2MQTTApp().run()
    