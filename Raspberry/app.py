# This module runs on the Raspberry Pi
# to communicate with between Arduino and AWS IoT Core

# Arduino sends data to Raspberry Pi via serial communication
# Raspberry Pi sends data to AWS IoT Core via MQTT
import serial
import os
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

load_dotenv()

AWS_CLIENT = os.getenv("AWS_CLIENT")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_PORT = os.getenv("AWS_PORT")
AWS_ROOT_CA = os.getenv("AWS_ROOT_CA")
AWS_PRIVATE_KEY = os.getenv("AWS_PRIVATE_KEY")
AWS_CERTIFICATE = os.getenv("AWS_CERTIFICATE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")

DICT = {
    "1001": 1, 
    "1002": 0, 
    }

myMQTTClient = AWSIoTMQTTClient(AWS_CLIENT)



def arduino_connection():
    arduino = serial.Serial(PORT, BAUDRATE)
    

def aws_iot_connection():

    # AWS IoT certificate based connection
    myMQTTClient.configureEndpoint(AWS_ENDPOINT, AWS_PORT)
    myMQTTClient.configureCredentials(AWS_ROOT_CA, AWS_PRIVATE_KEY, AWS_CERTIFICATE)
    # Infinite offline Publish queueing
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    # connect and publish
    myMQTTClient.connect()
    

def decode(data):
    pass


def encode(data):
    pass

def publish_topic():
    pass

def subscribe_topic():
    myMQTTClient.subscribe(topic_name, 1, subscription_callback)
    pass

def main():
    while True:
        data = arduino.readline()
        print(data)


if "__name__" == "__main__":
    main()
