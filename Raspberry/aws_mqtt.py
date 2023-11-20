import serial
import os
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from apscheduler.schedulers.background import BackgroundScheduler
import firebase_admin
from firebase_admin import credentials, storage
import subprocess
import time
from camera import capture_image

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
    "read" : "999",
    "read_height" : "101",
}



myMQTTClient = AWSIoTMQTTClient(AWS_CLIENT)

def firebase_storage(bucket_dir, image_path):

    cred = credentials.Certificate(CREDENTIALS)
    # print("Uploading image to Firebase Storage...")
    firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE
    })

    # Path to the image you want to upload
    # image_path = "image/2023-10-08-01115008-62db-4593-827a-24c3927a0ff9.png"

    filename = os.path.basename(image_path)

    # Create a Cloud Storage client
    bucket = storage.bucket()

    # Define the destination path in Firebase Storage (optional)
    destination_blob_name = "{}/{}".format(bucket_dir, filename)

    # Upload the image
    try:
        # Open and read the image
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Create a blob and upload the image data
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(image_data, content_type="image/jpeg")

        print(
            f"Image {image_path} uploaded to Firebase Storage at {destination_blob_name}")
    except Exception as e:
        print(f"Error uploading image: {e}")

    # Clean up: Delete the temporary credentials
    firebase_admin.delete_app(firebase_admin.get_app())

    os.remove(image_path)
    
def calculate_plant_size():
    return NotImplementedError

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
            


def subscribe_topic():
    myMQTTClient.subscribe(actuator_topic, 1, on_message_received)
    myMQTTClient.subscribe(scheduler_topic, 1, on_message_received)
    print("Subscribe successful")

def arduino_connection():
    global arduino_1, arduino_2
    arduino_1 = serial.Serial(PORT1, BAUDRATE)
    arduino_2 = serial.Serial(PORT2, BAUDRATE)

def read_arduino_serial():
    # better practice will be send a proper json format and all data in one json
    if(arduino_1 != None):
        while arduino_1.in_waiting > 0:
            line = arduino_1.readline().decode('utf-8').rstrip()
            line = line + ";1"
            print(line)
            myMQTTClient.publish(sensor_topic, line, 1)
            
    if(arduino_2 != None):
        while arduino_2.in_waiting > 0:
            line = arduino_2.readline().decode('utf-8').rstrip()
            line = line + ";2"
            print(line)
            myMQTTClient.publish(sensor_topic, line, 1)

# schedule a job to call funciton in arduino 1 and 2 every 15 minutes
def schedule_read_sensor():
    def scheduler_job_one():
        # schedule to get sensor data from arduino 1
        if(arduino_1 != None):
            if(arduino_1.isOpen == False):
                arduino_1.open()
            arduino_1.write(dict["read"].encode())
    
    def scheduler_job_two():
        # schedule to get height data from arduino 2
        if(arduino_2 != None):
            if(arduino_2.isOpen == False):
                arduino_2.open()
            arduino_2.write(dict["read_height"].encode())

        # schedule to take picture
        image_path = capture_image()
        firebase_storage("plant_size_image",
                     image_path)
        
        print("Take picture")
        print("Location" + image_path)
    
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(scheduler_job_one, 'interval', minutes=1)
    scheduler1.start()
    
    scheduler2 = BackgroundScheduler()
    scheduler2.add_job(scheduler_job_two, 'interval', minutes=1)
    scheduler2.start()
    
    
def publish_topic():
    
    # to actuator
    
    message = "light_act:0"
    
    json = '{"message": "' + message + '"}'
    
    myMQTTClient.publish(actuator_topic, json, 1)
    
def main():
    arduino_connection()
    aws_iot_connection()
    subscribe_topic()
    schedule_read_sensor()
    while True:
        read_arduino_serial()
        time.sleep(1)

if __name__ == "__main__":
    main()
