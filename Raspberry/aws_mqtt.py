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
import math
from roboflow import Roboflow

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

actuator_topic = "actuator"
scheduler_topic = "scheduler"
sensor_topic = "sensor"
image_path = "image.jpg"

# Define the dictionary for commands
commands = {
    "light:0": "30",
    "light:1": "1",
    "light:2": "2",
    "light:3": "3",
    "temp:0": "40",
    "temp:1": "4",
    "soil:0": "50",
    "soil:1": "5",
    "water:0": "60",
    "water:1": "6",
    "read": "999",
    "read_height": "101",
}

myMQTTClient = AWSIoTMQTTClient(AWS_CLIENT)

def firebase_storage(bucket_dir, image_path):
    cred = credentials.Certificate(CREDENTIALS)
    firebase_admin.initialize_app(cred, {'storageBucket': FIREBASE_STORAGE})

    filename = os.path.basename(image_path)
    bucket = storage.bucket()
    destination_blob_name = f"{bucket_dir}/{filename}"

    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(image_data, content_type="image/jpeg")

        print(f"Image {image_path} uploaded to Firebase Storage at {destination_blob_name}")
    except Exception as e:
        print(f"Error uploading image: {e}")

    firebase_admin.delete_app(firebase_admin.get_app())

    

def plant_width(plant_width_camera, plant_height, distance_to_soil):

    """
    plant_width_camera: [Pixels]
    focal_length: (= 2495.6) Camera Specific (calculated for our camera)
    distance_to_soil: Distance between the camera and the plant soil [mm]
    plant_height: Distance between soil and top of plant [mm]
    """

    focal_length = 2495.6
    result = abs(2 * math.tan(2 * math.atan(plant_width_camera / (2 * focal_length))) * (distance_to_soil - plant_height)) 
    return result

def save_image_to_db(image_path):
    return NotImplementedError

def get_plant_size_from_model(image_path):
    rf = Roboflow(api_key="DZakyhtiyjUvgQ96ykBS")
    project = rf.workspace().project("plant_size")
    model = project.version(1).model
    
    result = model.predict(image_path, confidence=40, overlap=30).json()
    
    print(result)
    print(result["predictions"][0]["width"])
    print(result["predictions"][0]["height"])

    return 300    
    
    # print((result.predictions[0].width + result.predictions[0].height)/2)
    
    # return (result.predictions[0].width + result.predictions[0].height)/2
    # return result
   

def aws_iot_connection():
    myMQTTClient.configureEndpoint(AWS_ENDPOINT, 8883)
    myMQTTClient.configureCredentials(AWS_ROOT_CA, AWS_PRIVATE_KEY, AWS_CERTIFICATE)
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)
    myMQTTClient.configureConnectDisconnectTimeout(10)
    myMQTTClient.configureMQTTOperationTimeout(5)
    myMQTTClient.connect()
    print("Connection successful")

def on_message_received(client, userdata, message):
    
    
    print("Received a new message: ")
    payload = message.payload.decode()
    topic = message.topic

    if topic == actuator_topic or topic == scheduler_topic:
        print(f"Received--{payload}")
        arduino_write(payload)

def subscribe_topic():
    result1 = myMQTTClient.subscribe(actuator_topic, 1, on_message_received)
    result2 = myMQTTClient.subscribe(scheduler_topic, 1, on_message_received)
    
    print(result1)
    print(result2)

    print("Subscribe successful")

def arduino_connection():
    global arduino_1, arduino_2
    arduino_1 = serial.Serial(PORT1, BAUDRATE)
    arduino_2 = serial.Serial(PORT2, BAUDRATE)

def arduino_write(arduino, command):
    if arduino is not None:
        if arduino.isOpen == False:
            arduino.open()
        arduino.write(commands[command].encode())

def read_arduino_serial():
    read_arduino(arduino_1)
    read_arduino(arduino_2)

def read_arduino(arduino):
    global image_path
    
    if arduino is not None:
        while arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            line = line + ";1"
            print(line)
            myMQTTClient.publish(sensor_topic, line, 1)
            
            sensor_type = (line.split("!")[1]).split(":")[0]
            plant_height = ((line.split("!")[1]).split(":")[1]).split(";")[0]
            if sensor_type == "height":
                plant_size = 300
                image_path = "C:/Users/Asus/Pictures/Camera Roll/WIN_20231121_12_02_51_Pro.jpg"
                plant_size = get_plant_size_from_model(image_path)
                actual_plant_size = plant_width(plant_size,(int)(plant_height),8)
                os.remove(image_path)
                print("actual_plant_size = ", actual_plant_size)

def schedule_read_sensor():
    scheduler1 = BackgroundScheduler()
    scheduler1.add_job(scheduler_job, 'interval', minutes=1)
    scheduler1.start()

def scheduler_job():
    global arduino_1, arduino_2, image_path
    arduino_write(arduino_1, "read")
    arduino_write(arduino_2, "read_height")

    image_path = capture_image()
    firebase_storage("plant_size_image", image_path)
    save_image_to_db(image_path)
    
    print("Take picture")
    print("Location" + image_path)

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
