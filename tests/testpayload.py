from mqtt_msg_hndlr import MSGHandler


msg = "modbus addr 1227 value 111"

msghndr = MSGHandler()
msghndr.readMessage(msg)

