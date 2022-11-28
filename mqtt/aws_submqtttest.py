import time as t
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

ENDPOINT = "a14esw6xzioxj2-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "D:\\Eng_Cont_Aut\\4 - Ini_Cientifica\\EnergyEfficiency4.0\\ESTEIRA\\aws\\esteiraic-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "D:\\Eng_Cont_Aut\\4 - Ini_Cientifica\\EnergyEfficiency4.0\\ESTEIRA\\aws\\esteiraic-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "D:\\Eng_Cont_Aut\\4 - Ini_Cientifica\\EnergyEfficiency4.0\\ESTEIRA\\aws\\AmazonRootCA1.pem"
TOPIC = "test/status"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)

myAWSIoTMQTTClient.connect()
print('Begin Subscription \n')

def customCallback(client, userdata, message):
    print(message.payload.decode("utf-8"))
myAWSIoTMQTTClient.subscribe(TOPIC, 1, customCallback)

print('Waiting for the callback. Click to conntinue...')
x = input()

myAWSIoTMQTTClient.unsubscribe(TOPIC)
print("Client unsubscribed") 


myAWSIoTMQTTClient.disconnect()
print("Client Disconnected")