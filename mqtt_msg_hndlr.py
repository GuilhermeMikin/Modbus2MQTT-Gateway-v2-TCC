from imports import threading

busy = threading.Lock()


class MSGHandler():
    """ Class responsible for deciding the mqtt msg destination """
    def __init__(self, modbus_client):
        """ Class builder """
        busy.acquire()
        self._mqtt2mbsClient = modbus_client
        busy.release()

    def readMessage(self, msg):
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
