import serial
import os
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import subprocess
import time

load_dotenv()

AWS_CLIENT = os.getenv("AWS_CLIENT")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_PORT = os.getenv("AWS_PORT")
AWS_ROOT_CA = os.getenv("AWS_ROOT_CA")
AWS_PRIVATE_KEY = os.getenv("AWS_PRIVATE_KEY")
AWS_CERTIFICATE = os.getenv("AWS_CERTIFICATE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
CREDENTIALS = os.getenv("CREDENTIALS")
FIREBASE_STORAGE = os.getenv("FIREBASE_STORAGE")

arduino = None
actuator_topic = "actuator"
scheduler_topic = "scheduler"
sensor_topic = "sensor"
dict = {
    "light_act:0" : "30",
    "light_act:1" : "1",
    "light_act:2" : "2",
    "light_act:3" : "3",
    "temp_act:0" : "40",
    "temp_act:1" : "4",
    "soil_act:0" : "50",
    "soil_act:1" : "5",
    "water_act:0" : "60",
    "water_act:1" : "6",
    "read" : "999"
}

DICT = {
    "1001": 1,
    "1002": 0,
}

myMQTTClient = AWSIoTMQTTClient(AWS_CLIENT)

def aws_iot_connection():

    # AWS IoT certificate based connection
    myMQTTClient.configureEndpoint(AWS_ENDPOINT, 8883)
    myMQTTClient.configureCredentials(AWS_ROOT_CA, AWS_PRIVATE_KEY, AWS_CERTIFICATE)
    # Infinite offline Publish queueing
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    # connect and publish
    myMQTTClient.connect()
    print("Connection successful")

def on_message_received(client, userdata, message):
    payload = message.payload.decode()
    topic = message.topic
    if topic == "actuator":
        print("Received--"+payload)
        if(arduino != None):
            if(arduino.isOpen == False):
                arduino.open()
            arduino.write(dict[payload].encode())
    elif topic == "scheduler":
        print("Received--"+payload)
        if(arduino != None):
            if(arduino.isOpen == False):
                arduino.open()
            arduino.write(dict[payload].encode())
            

def publish_topic():
    pass


def subscribe_topic():
    myMQTTClient.subscribe(actuator_topic, 1, on_message_received)
    myMQTTClient.subscribe(scheduler_topic, 1, on_message_received)
    print("Subscribe successful")

def arduino_connection():
    arduino = serial.Serial(PORT, BAUDRATE)
    return arduino


def main():
    aws_iot_connection()
    subscribe_topic()
#    ardunio = arduino_connection()
    while True:
        if(arduino != None):
            while arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').rstrip()
                line = line + ";1"
                print(line)
                myMQTTClient.publish(sensor_topic, line, 1)
        time.sleep(1)

if __name__ == "__main__":
    main()
