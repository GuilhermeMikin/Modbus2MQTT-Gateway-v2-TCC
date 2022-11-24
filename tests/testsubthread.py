from mqtt.mqtt_sub import MQTTSubscriber
import threading
from time import sleep


subscribing_thread = True
mqtt_sub_thread = MQTTSubscriber()

def subscribe():
    mqtt_sub_thread.subscribe()

# def disconnect():
#     mqtt_sub_thread.disconnect_sub()

    

if __name__ == '__main__':
    sub_thread = threading.Thread(target=subscribe())
    sub_thread.start()
    mqtt_sub_thread.client.loop_start()
    sleep(5)
    mqtt_sub_thread.client.loop_stop()
    print('alow')
    
    
