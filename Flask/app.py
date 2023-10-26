from flask import Flask, render_template, request
import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
from decimal import Decimal
from datetime import datetime
import tempfile

from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
# from firebase import firebase
import firebase_admin
from firebase_admin import credentials, storage


# Currently this connects to local db
import aws_rds_com as db

from aws_rds_com import *

CREDENTIALS = os.getenv("CREDENTIALS")
FIREBASE_STORAGE = os.getenv("FIREBASE_STORAGE")
cred = credentials.Certificate(CREDENTIALS)
firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE
    })
app = Flask(__name__)

# IP address may change each time broker is restarted
# MQTT_SERVER = "172.20.10.4"
# actuator_topic = 'actuator'
# scheduler_topic = "scheduler"
# sensor_topic = "sensor"
# port = 5000

# def on_connect(client, userdata, flags, rc):
#     client.publish(actuator_topic, "STARTING SERVER")
#     client.publish(actuator_topic, "CONNECTED")
#     client.subscribe(sensor_topic)


# def on_message(client, userdata, msg):
#     payload = str(msg.payload, encoding='utf-8')
#     print(payload)
#     splitStr = payload.split(":")
#     print(splitStr)
#     secondSplit = splitStr[1].split(";")
#     print(secondSplit)
#     match splitStr[0]:
#         case "Water":
#             db.insert_sensor_by_type("moisture", secondSplit[0], secondSplit[1])
#         case "Light Value":
#             db.insert_sensor_by_type("light", secondSplit[0], secondSplit[1])
#         case "Temperature":
#             db.insert_sensor_by_type("temperature", secondSplit[0], secondSplit[1])
#         case "level":
#             db.insert_sensor_by_type("level", secondSplit[0], secondSplit[1])
#         case "Growth Light":
#             db.insert_actuator_by_type("light", secondSplit[0], secondSplit[1])
#         case "Water Pump":
#             db.insert_actuator_by_type("water", secondSplit[0], secondSplit[1])
#         case "Fan":
#             db.insert_actuator_by_type("fan", secondSplit[0], secondSplit[1])

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
def create_greenroom():
    
    if request.method == 'POST':
        
        name = request.form.get("name")
        location = request.form.get("location")
        description = request.form.get("description")
        
        file = request.files['images']
        

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
            
            # Optionally, you can provide feedback to the user, e.g., by redirecting to a success page
            # return render_template('success.html', image_url=image_url)
    
    return render_template('create_greenroom.html')



@app.route('/greenroom-detail/<id>', methods=['GET', 'POST'])
def page_greenroom_detail(id):
    all_param = ["nutrient", "water", "light", "fan"]
    for param in all_param:
        # Get the posted value
        value = request.form.get(param)
        if value != None:
            msg = f"{param}:{value}"
            print(msg)
            db.insert_actuator_by_type(param,value,id)
            client.publish(actuator_topic, msg)

    greenroom = db.select_by_id(id)
    return render_template('greenroom-detail.html', greenroom=greenroom)


# @app.route('/manual', methods=['GET', 'POST'])
# # Template for publishing manual control messages through MQTT
# def manual_control():
#     # Defines all the name of "modules" to loop through (the name should match the "name" attr in form)
#     all_param = ["nutrient", "light"]
#     for param in all_param:
#         # Get the posted value
#         value = request.form.get(param)
#         if value != None:
#             msg = f"{param}:{value}"
#             print(msg)
#             client.publish(actuator_topic, msg)

#     return render_template('manual_control.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# def scheduler_read_sensor():
#     print("Publishing to read sensor data...")
#     client.publish(scheduler_topic, "read")

if __name__ == '__main__':
    # client = mqtt.Client()
    # #client.username_pw_set(username, password)
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect(MQTT_SERVER)
    # client.loop_start()

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(scheduler_read_sensor, 'interval', minutes=15)
    # scheduler.start()

    app.run(debug=True)

    