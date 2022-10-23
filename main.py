from imports import *
from mb2mqtt import ClienteMODBUS2MQTT
Config.set('kivy', 'exit_on_escape', '0')


class MyWidget(MDScreen):
    """
    Construtor
    """
    def __init__(self, **kw):
        super().__init__(**kw)


    def connection(self): #Function to connnect to the modbus network and stablish a connection with the mqtt broker
        try:
            if self.ids.bt_con.text == "  CONNECT  ": #If the application is desconnected 
                try:
                    Window.set_system_cursor("wait")                        #Change the cursor to wainting mode
                    self._modbus_Addrs = self.ids.hostmodbus.text           #Get the modbus network IP address from the user input
                    self._modbus_Port = int(self.ids.portmodbus.text)       #Get the modbus network port (default 502)
                    self._mqtt_broker_Addrs = self.ids.hostmqtt.text        #Get the MQTT Broker address
                    self._mqtt_broker_Port = int(self.ids.portmqtt.text)    #Get the MQTT Broker port
                    self._mqtt_broker_user = self.ids.hostmqttuser.text     #Get the MQTT Broker username
                    self._mqtt_broker_pw = self.ids.hostmqttpw.text         #Get the MQTT Broker password
                    self._awsiot_endpoint = self.ids.awsendpoint.text
                    self._awsiot_port = int(self.ids.awsport.text)
                    self._awsiot_client_id = self.ids.awsclientid.text
                    self._awsiot_path_to_certificate = self.ids.awscert.text 
                    self._awsiot_path_to_private_key = self.ids.awsprivkey.text 
                    self._awsiot_path_to_amazon_root_ca1 = self.ids.awsca1.text 
                    self._awsiot_state = (True if self.ids.checkaws.active else False)
                    self._c = ClienteMODBUS2MQTT(self._modbus_Addrs,self._modbus_Port,
                                                 self._mqtt_broker_Addrs,self._mqtt_broker_Port,
                                                 self._awsiot_endpoint,self._awsiot_port,self._awsiot_client_id,
                                                 self._awsiot_path_to_certificate,self._awsiot_path_to_private_key,
                                                 self._awsiot_path_to_amazon_root_ca1,self._awsiot_state)
                    self._c.connect_on()
                    self.ids.bt_con.text = "DISCONNECT"   #Connect and change the button text to "disconnect"
                    if self._c._status_conn_mqtt == True or self._c._status_conn_mqtt_aws == True:
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
                self._c.disconnect()
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
                    self._c._publishing_thread = True
                    self._c._thread_publisher = Thread(target=self._c.mbs2mqttGateway, args=(
                        modbus_type,modbus_read_addr1,modbus_read_length1,
                        modbus_read_addr2,modbus_read_length2,
                        modbus_read_addr3,modbus_read_length3,
                        modbus_read_addr4,modbus_read_length4,
                        mqtt_pub_topic1,mqtt_pub_topic2,
                        mqtt_pub_topic3,mqtt_pub_topic4,
                        manual_gates, json_gates, json_file_path,
                        modbus_type_display1,modbus_type_display2,
                        modbus_type_display3,modbus_type_display4))
                    self._c._thread_publisher.start()
                    Snackbar(text = f"Reading has started and data is being published to the specified topic...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                    Window.set_system_cursor("arrow")
                except Exception as e: 
                    Window.set_system_cursor("arrow")
                    print('ERROR: ', e.args)
                    Snackbar(text = f"Could not start reading! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
            else:
                try:
                    self.ids.bt_readpub.text = "Start Reading/Publishing"
                    self._c._publishing_thread = False
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
                if self._c._status_conn_mqtt:
                    self._c.mqttPublisher(topic=mqtt_pub_topic, msg=mqtt_pub_msg)
                    Snackbar(text = f"Message successfully published to topic {mqtt_pub_topic}...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                    Window.set_system_cursor("arrow")
                elif self._c._status_conn_mqtt_aws:
                    self._c.awsMqttPublisher(topic=mqtt_pub_topic, msg=mqtt_pub_msg)
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
                    self._c._subscribing_thread = True
                    self._c._thread_subscriber = Thread(target=self._c.mqttSubscriber, args=(mqtt_sub_topic))
                    self._c._thread_subscriber.start()
                    Snackbar(text = f"Subscribed to topic {mqtt_sub_topic} successfully...", bg_color=(0,1,0,1), size_hint_y=0.05).open()
                    Window.set_system_cursor("arrow")
                except Exception as e: 
                    Window.set_system_cursor("arrow")
                    print('ERROR: ', e.args)
                    Snackbar(text = f"Could not start subscription! ERROR: {e.args}...", bg_color=(1,0,0,1)).open()
            else:
                try:
                    self.ids.bt_subscribe.text = " Subscribe "
                    self._c._subscribing_thread = False
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
                self._c.writeMbsData(modbus_type, modbus_write_addr, modbus_write_value)
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
                    modbus_reads = self._c.readMbsF32Data(modbus_type, modbus_read_addr, modbus_read_length)
                else:
                    modbus_reads = self._c.readMbsData(modbus_type, modbus_read_addr, modbus_read_length)
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
    Mbs2MQTTApp().run()

