import serial
import os
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import time

load_dotenv()

AWS_CLIENT = os.getenv("AWS_CLIENT")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_PORT = os.getenv("AWS_PORT")
AWS_ROOT_CA = os.getenv("AWS_ROOT_CA")
AWS_PRIVATE_KEY = os.getenv("AWS_PRIVATE_KEY")
AWS_CERTIFICATE = os.getenv("AWS_CERTIFICATE")
PORT1 = os.getenv("PORT1")
PORT2 = os.getenv("PORT2")
BAUDRATE = os.getenv("BAUDRATE")
CREDENTIALS = os.getenv("CREDENTIALS")
FIREBASE_STORAGE = os.getenv("FIREBASE_STORAGE")

arduino_1 = None
arduino_2 = None
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
        if(arduino_1 != None):
            if(arduino_1.isOpen == False):
                arduino_1.open()
            arduino_1.write(dict[payload].encode())
    elif topic == "scheduler":
        print("Received--"+payload)
        if(arduino_1 != None):
            if(arduino_1.isOpen == False):
                arduino_1.open()
            arduino_1.write(dict[payload].encode())
            

def publish_topic():
    pass


def subscribe_topic():
    myMQTTClient.subscribe(actuator_topic, 1, on_message_received)
    myMQTTClient.subscribe(scheduler_topic, 1, on_message_received)
    print("Subscribe successful")

def arduino_connection():
    arduino_1 = serial.Serial(PORT1, BAUDRATE)
    arduino_2 = serial.Serial(PORT2, BAUDRATE)

def read_arduino_serial():
    if(arduino_1 != None):
        while arduino_1.in_waiting > 0:
            line = arduino_1.readline().decode('utf-8').rstrip()
            line = line + ";1"
            print(line)
            myMQTTClient.publish(sensor_topic, line, 1)

def schedule_read_sensor():
    def scheduler_job():
        if(arduino_1 != None):
            if(arduino_1.isOpen == False):
                arduino_1.open()
            arduino_1.write(dict["read"].encode())
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduler_job, 'interval', minutes=15)
    scheduler.start()

def main():
    aws_iot_connection()
    subscribe_topic()
#    schedule_read_sensor()
#    ardunio = arduino_connection()
    while True:
        read_arduino_serial()
        time.sleep(1)

if __name__ == "__main__":
    main()
