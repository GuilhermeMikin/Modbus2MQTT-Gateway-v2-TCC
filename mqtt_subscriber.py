import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

aws_client_id = "Device1"
aws_iot_port = 8883
aws_endpoint = "ax7j1tokadxlb-ats.iot.us-east-2.amazonaws.com"
path_to_certificate = "D:\\AWS\\thingtest\\31d8a33563-certificate.pem.crt"
path_to_private_key = "D:\\AWS\\thingtest\\31d8a33563-private.pem.key"
path_to_amazon_root_ca1 = "D:\\AWS\\thingtest\\AmazonRootCA1.pem.txt"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(aws_client_id)
myAWSIoTMQTTClient.configureEndpoint(aws_endpoint, 8883)
myAWSIoTMQTTClient.configureCredentials(path_to_amazon_root_ca1, path_to_private_key, path_to_certificate)

print('-' * 100)
print('MQTT Subscriber'.center(100))
topic = input('\nSubscribe to topic: ')

myAWSIoTMQTTClient.connect()
print('Begin Subscription \n')


def customCallback(client, userdata, message):
    print(message.payload.decode("utf-8"))

myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
print('\nSuccessfully Subscribed! Press Enter to exit...\n')
x = input()

myAWSIoTMQTTClient.unsubscribe(topic)
print("Client unsubscribed") 

myAWSIoTMQTTClient.disconnect()
print("Client Disconnected")