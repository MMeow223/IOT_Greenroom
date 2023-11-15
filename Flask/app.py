from flask import Flask, render_template, request
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
from decimal import Decimal
from datetime import datetime
import tempfile

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# from firebase import firebase
import firebase_admin
from firebase_admin import credentials, storage

from aws_rds_com import *
from dotenv import load_dotenv

AWS_CLIENT = os.getenv("AWS_CLIENT")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_ROOT_CA = os.getenv("AWS_ROOT_CA")
AWS_PRIVATE_KEY = os.getenv("AWS_PRIVATE_KEY")
AWS_CERTIFICATE = os.getenv("AWS_CERTIFICATE")

load_dotenv()
CREDENTIALS = os.getenv("CREDENTIALS")
FIREBASE_STORAGE = os.getenv("FIREBASE_STORAGE")
cred = credentials.Certificate(CREDENTIALS)
firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE
    })
app = Flask(__name__)

actuator_topic = "actuator"
scheduler_topic = "scheduler"
sensor_topic = "sensor"

myMQTTClient = None
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
    subscribe_topic()

def subscribe_topic():
    myMQTTClient.subscribe(sensor_topic, 1, on_message)

# Messages from Arduino -> PI -> Cloud, expect the format of "table_type!data_type:value;greenroom_id"
def on_message(client, userdata, message):
    payload = message.payload.decode()
    splitStr = payload.split("!")
    secondSplit = splitStr[1].split(":")
    thirdSplit = secondSplit[1].split(";")

    table_type = splitStr[0]
    data_type = secondSplit[0]
    value = thirdSplit[0]
    greenroom_id = thirdSplit[1]

    if table_type == "act":
        insert_activity(data_type, value, greenroom_id)
    elif table_type == "sensor":
        insert_sensor(data_type, value, greenroom_id)
    elif table_type == "mode":
        update_mode(data_type, value, greenroom_id)


@app.route('/')
def index():
    
    greenrooms= get_greenroom_all()
    for gr in greenrooms:
        soil_chart_label = []
        light_chart_label = []
        temperature_chart_label = []
        soil_chart_data = []
        light_chart_data = []
        temperature_chart_data = []
        
        for i in get_record_greenroom(gr["greenroom_id"],True,"soil_moisture"):
            soil_chart_label.append(i["timestamp"])
            soil_chart_data.append(i["value"])
        
        for i in get_record_greenroom(gr["greenroom_id"],True,"light"):
            light_chart_label.append(i["timestamp"])
            light_chart_data.append(i["value"])
            
        for i in get_record_greenroom(gr["greenroom_id"],True,"temperature"):
            temperature_chart_label.append(i["timestamp"])
            temperature_chart_data.append(i["value"])
            
        current_water_level = get_record_greenroom(gr["greenroom_id"],True,"level")
        # get the last one
        if len(current_water_level) > 0:
            current_water_level = current_water_level[0]["value"]
            if current_water_level == "0":
                current_water_level = True
            else:
                current_water_level = False
        else:
            current_water_level = False
            
        greenrooms[greenrooms.index(gr)]["soil_chart_data"] = soil_chart_data
        greenrooms[greenrooms.index(gr)]["light_chart_data"] = light_chart_data
        greenrooms[greenrooms.index(gr)]["temperature_chart_data"] = temperature_chart_data
        
        greenrooms[greenrooms.index(gr)]["soil_chart_label"] = soil_chart_label
        greenrooms[greenrooms.index(gr)]["light_chart_label"] = light_chart_label
        greenrooms[greenrooms.index(gr)]["temperature_chart_label"] = temperature_chart_label
        
        greenrooms[greenrooms.index(gr)]["water_level"] = current_water_level
        
    data_template = {
        "greenroom": greenrooms,
        
    }

    return render_template('index.html', data=data_template)


@app.route('/create_greenroom', methods=['GET', 'POST'])
def create_greenroom_page():
    
    if request.method == 'POST':
        
        name = request.form.get("name")
        location = request.form.get("location")
        description = request.form.get("description")
        
        file = request.files['images']
        

        image_url = "default.jpg"
       # Check if a file was submitted
        if file:
            # Create a reference to the Firebase Storage location where you want to store the image
            storage_ref = storage.bucket().blob("greenroom_images/" + file.filename)
            
            # Upload the file to Firebase Storage
            storage_ref.upload_from_string(file.read(), content_type=file.content_type)
            
            # Get the URL of the uploaded image
            image_url = storage_ref.public_url
        
        # Create the greenroom in your database, including the image URL
        create_greenroom(name, location, description, image_url)
            
    
    return render_template('create_greenroom.html')



@app.route('/greenroom-detail/<id>', methods=['GET', 'POST'])
def page_greenroom_detail(id):
    all_param = ["water", "soil", "light", "temp"]
    for param in all_param:
        value = request.form.get(param)
        if value != None:
            msg = f"{param}:{value}"
            print(msg)
            insert_activity(param,value,id)
            if(param != "water"):
                update_mode(param, "manual", id)
            myMQTTClient.publish(actuator_topic, msg)

    greenroom = get_record_greenroom_all_actuator_one(id)
    for i in get_record_greenroom(id,type="soil_moisture"):
        greenroom["moisture"] = i["value"]
        
    for i in get_record_greenroom(id,type="light"):
        greenroom["light"] = i["value"]
        
    for i in get_record_greenroom(id,type="temperature"):
        greenroom["temperature"] = i["value"]
        
    current_water_level = get_record_greenroom(id,type="level")
    # get the last one
    if len(current_water_level) > 0:
        current_water_level = str(current_water_level[0]["value"])
        print(current_water_level)
        if current_water_level == "0.00":
            current_water_level = True
        else:
            current_water_level = False
    else:
        current_water_level = False

    greenroom["water_level"] = current_water_level
    
    greenroom["name"] = get_greenroom(id)[0]["name"]
    greenroom["image"] = get_greenroom(id)[0]["image"]

    greenroom.update(get_record_greenroom_all_actuator_mode_one(id))
    
    print(greenroom)

    return render_template('greenroom-detail.html', greenroom=greenroom)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# def scheduler_read_sensor():
#     print("Publishing to read sensor data...")
#     client.publish(scheduler_topic, "read")

if __name__ == '__main__':
    myMQTTClient = AWSIoTMQTTClient(AWS_CLIENT)
    aws_iot_connection()

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(scheduler_read_sensor, 'interval', minutes=15)
    # scheduler.start()

    app.run(debug=True)

    