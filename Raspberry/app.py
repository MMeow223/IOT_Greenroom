# This module runs on the Raspberry Pi
# to communicate with between Arduino and AWS IoT Core

# Arduino sends data to Raspberry Pi via serial communication
# Raspberry Pi sends data to AWS IoT Core via MQTT
# import serial
import os
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# from firebase import firebase
import firebase_admin
from firebase_admin import credentials, storage
import serial
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

DICT = {
    "1001": 1,
    "1002": 0,
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


def arduino_connection():
    arduino_1 = serial.Serial(PORT1, BAUDRATE)
    arduino_2 = serial.Serial(PORT2, BAUDRATE)


def aws_iot_connection():

    # AWS IoT certificate based connection
    myMQTTClient.configureEndpoint(AWS_ENDPOINT, AWS_PORT)
    myMQTTClient.configureCredentials(
        AWS_ROOT_CA, AWS_PRIVATE_KEY, AWS_CERTIFICATE)
    # Infinite offline Publish queueing
    myMQTTClient.configureOfflinePublishQueueing(-1)
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    # connect and publish
    myMQTTClient.connect()


def decode(data):
    data_array = data.split("|")
    data_dic = {
        "light": (int)(data_array[0].split(":")[1]),
        "soil": (float)(data_array[1].split(":")[1]),
        "temp": (int)(data_array[2].split(":")[1]),
        "water_level": (int)(data_array[3].split(":")[1]),
    }
    
    pass


def encode(data):
    pass


def publish_topic():
    pass


def subscribe_topic():
    myMQTTClient.subscribe(topic_name, 1, subscription_callback)
    pass


def main():
    image_path = capture_image()
    firebase_storage("plant_size_image",
                     image_path)
    # while True:
    #     data = arduino.readline()
    #     print(data)


if __name__ == "__main__":
    main()
