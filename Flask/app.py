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

import aws_rds_com as db
from dotenv import load_dotenv

load_dotenv()

AWS_CLIENT = os.getenv("AWS_CLIENT")
AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
AWS_ROOT_CA = os.getenv("AWS_ROOT_CA")
AWS_PRIVATE_KEY = os.getenv("AWS_PRIVATE_KEY")
AWS_CERTIFICATE = os.getenv("AWS_CERTIFICATE")

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
    subscribe_topic()

def subscribe_topic():
    result = myMQTTClient.subscribe(sensor_topic, 1, on_message)
    print("RESULT FOR SUBSCRIBE")
    print(result)

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
        db.insert_activity(data_type, value, greenroom_id)
    elif table_type == "sensor":
        db.insert_sensor(data_type, value, greenroom_id)
    elif table_type == "mode":
        db.update_mode(data_type, value, greenroom_id)


def prepare_sidebar():
    # Get all greenrooms
    greenrooms = db.get_greenroom_all()
    
    # get current link
    current_link = request.path
    current_link = current_link.split("/")[1]
    
    # prepare sidebar
    sidebar = []
    for gr in greenrooms:
        sidebar.append({
            "name": gr["name"],
            "link": gr["greenroom_id"],
            "active": gr["greenroom_id"] == current_link
        })
        
    return sidebar

aws_iot_connection()

@app.route('/')
def index():
    
    greenrooms= db.get_greenroom_all()
    for gr in greenrooms:
        soil_chart_label = []
        light_chart_label = []
        temperature_chart_label = []
        soil_chart_data = []
        light_chart_data = []
        temperature_chart_data = []
        
        for i in db.get_record_greenroom(gr["greenroom_id"],True,"soil_moisture"):
            soil_chart_label.append(i["timestamp"])
            soil_chart_data.append(i["value"])
        
        for i in db.get_record_greenroom(gr["greenroom_id"],True,"light"):
            light_chart_label.append(i["timestamp"])
            light_chart_data.append(i["value"])
            
        for i in db.get_record_greenroom(gr["greenroom_id"],True,"temperature"):
            temperature_chart_label.append(i["timestamp"])
            temperature_chart_data.append(i["value"])
            
        current_water_level = db.get_record_greenroom(gr["greenroom_id"],True,"level")
        # get the last one
        if len(current_water_level) > 0:
            current_water_level = current_water_level[0]["value"]
            if current_water_level == "0":
                current_water_level = True
            else:
                current_water_level = False
        else:
            current_water_level = False
     
        greenrooms[greenrooms.index(gr)]["temperature"] = db.get_one_month_record("temperature_sensor",gr["greenroom_id"])
        greenrooms[greenrooms.index(gr)]["light"] = db.get_one_month_record("light_sensor",gr["greenroom_id"])
        greenrooms[greenrooms.index(gr)]["soil"] = db.get_one_month_record("soil_moisture_sensor",gr["greenroom_id"])
        greenrooms[greenrooms.index(gr)]["current_temp_value"] = db.get_latest_sensor_data("temperature_sensor",gr["greenroom_id"])
        greenrooms[greenrooms.index(gr)]["current_light_value"] = db.get_latest_sensor_data("light_sensor",gr["greenroom_id"])
        greenrooms[greenrooms.index(gr)]["current_soil_value"] = db.get_latest_sensor_data("soil_moisture_sensor",gr["greenroom_id"])
        greenrooms[greenrooms.index(gr)]["water_level"] = current_water_level
        
    data_template = {
        "greenroom": greenrooms,
        "sidebar": prepare_sidebar()
        
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
            image_url = file.filename
        
        # Create the greenroom in your database, including the image URL
        db.create_greenroom(name, location, description, image_url)
            
    data_template = {
    # "greenroom": greenrooms,
    "sidebar": prepare_sidebar()
        
    }

    return render_template('index.html', data=data_template)



@app.route('/greenroom-detail/<id>', methods=['GET', 'POST'])
def page_greenroom_detail(id):
    all_param = ["water", "soil", "light", "temp"]
    thres_param = ["soil_threshold", "light_threshold_1", "light_threshold_2", "light_threshold_3", "temp_threshold"]

    reset = request.form.get("reset_auto")
    if reset != None:
        for param in all_param:
            if(param != "water"):
                db.update_mode(param, "auto", id)
        result = myMQTTClient.publish(actuator_topic, reset, 1)
        print("RESULT FOR PUBLISH")
        print(result)

    threshold = request.form.get("threshold_update")
    if threshold != None:
        for param in thres_param:
            value = request.form.get(param)
            msg = f"{param}:{value}"
            db.insert_threshold(param, value, id)
            result = myMQTTClient.publish(actuator_topic, msg, 1)
            print("RESULT FOR PUBLISH")
            print(result)

    for param in all_param:
        value = request.form.get(param)
        if value != None:
            msg = f"{param}:{value}"
            print(msg)
            db.insert_activity(param,value,id)
            if(param != "water"):
                db.update_mode(param, "manual", id)
            myMQTTClient.publish(actuator_topic, msg, 1)

    greenroom = db.get_record_greenroom_all_actuator_one(id)
    for i in db.get_record_greenroom(id,type="soil_moisture"):
        greenroom["moisture"] = i["value"]
        
    for i in db.get_record_greenroom(id,type="light"):
        greenroom["light"] = i["value"]
        
    for i in db.get_record_greenroom(id,type="temperature"):
        greenroom["temperature"] = i["value"]
        
    current_water_level = db.get_record_greenroom(id,type="level")
    # get the last one
    if len(current_water_level) > 0:
        current_water_level = str(current_water_level[0]["value"])
        if current_water_level == "0.00":
            current_water_level = True
        else:
            current_water_level = False
    else:
        current_water_level = False

    greenroom["water_level"] = current_water_level
    
    greenroom["name"] = db.get_greenroom(id)[0]["name"]
    greenroom["image"] = db.get_greenroom(id)[0]["image"]
    greenroom["id"] = id

    greenroom.update(db.get_record_greenroom_all_actuator_mode_one(id))

    greenroom.update(db.get_record_greenroom_all_actuator_threshold_one(id))
    
    print(greenroom)
    
    data_template = {
        "greenroom": greenroom,
        "sidebar": prepare_sidebar()
    }

    return render_template('greenroom-detail.html', data=data_template)


@app.route('/report-test/<id>', methods=['GET', 'POST'])
def report_test(id):
    greenroom_id = id
    greenrooms= db.get_greenroom(greenroom_id)
    
    one_day_temp = db.get_one_day_record("temperature_sensor",greenroom_id)
    one_day_light = db.get_one_day_record("light_sensor",greenroom_id)
    one_day_soil = db.get_one_day_record("soil_moisture_sensor",greenroom_id)
    
    one_month_temp = db.get_one_month_record("temperature_sensor",greenroom_id)
    one_month_light = db.get_one_month_record("light_sensor",greenroom_id)
    one_month_soil = db.get_one_month_record("soil_moisture_sensor",greenroom_id)
    
    one_year_temp = db.get_one_year_record("temperature_sensor",greenroom_id)
    one_year_light = db.get_one_year_record("light_sensor",greenroom_id)
    one_year_soil = db.get_one_year_record("soil_moisture_sensor",greenroom_id)
    
    life_temp = db.get_life_time_record("temperature_sensor",greenroom_id)
    life_light = db.get_life_time_record("light_sensor",greenroom_id)
    life_soil = db.get_life_time_record("soil_moisture_sensor",greenroom_id) 
    
    one_day_act_temp = db.get_actuator_one_day_record("temperature_actuator_activity",greenroom_id)
    one_day_act_light = db.get_actuator_one_day_record("light_actuator_activity",greenroom_id)
    one_day_act_soil = db.get_actuator_one_day_record("soil_moisture_actuator_activity",greenroom_id)
    
    one_month_act_temp = db.get_actuator_one_month_record("temperature_actuator_activity",greenroom_id)
    one_month_act_light = db.get_actuator_one_month_record("light_actuator_activity",greenroom_id)
    one_month_act_soil = db.get_actuator_one_month_record("soil_moisture_actuator_activity",greenroom_id)
    
    one_year_act_temp = db.get_actuator_one_year_record("temperature_actuator_activity",greenroom_id)
    one_year_act_light = db.get_actuator_one_year_record("light_actuator_activity",greenroom_id)
    one_year_act_soil = db.get_actuator_one_year_record("soil_moisture_actuator_activity",greenroom_id) 
    
    life_act_temp = db.get_actuator_life_time_record("temperature_actuator_activity",greenroom_id)
    life_act_light = db.get_actuator_life_time_record("light_actuator_activity",greenroom_id)
    life_act_soil = db.get_actuator_life_time_record("soil_moisture_actuator_activity",greenroom_id)
    
    one_day_size_height = db.get_plant_size_and_height_one_day_record(greenroom_id)
    one_month_size_height = db.get_plant_size_and_height_one_month_record(greenroom_id)
    one_year_size_height = db.get_plant_size_and_height_one_year_record(greenroom_id)
    life_size_height = db.get_plant_size_and_height_lifetime_record(greenroom_id)
    
    plant_image = db.get_plant_image(greenroom_id)
    # plant_image string to json
    data_template = {
        "one_day_temp": one_day_temp,
        "one_day_light": one_day_light,
        "one_day_soil": one_day_soil,
        "one_month_temp": one_month_temp,
        "one_month_light": one_month_light,
        "one_month_soil": one_month_soil,
        "one_year_temp": one_year_temp,
        "one_year_light": one_year_light,
        "one_year_soil": one_year_soil,
        "life_temp": life_temp,
        "life_light": life_light,
        "life_soil": life_soil,
        "one_day_act_temp": one_day_act_temp,
        "one_day_act_light": one_day_act_light,
        "one_day_act_soil": one_day_act_soil,
        "one_month_act_temp": one_month_act_temp,
        "one_month_act_light": one_month_act_light,
        "one_month_act_soil": one_month_act_soil,
        "one_year_act_temp": one_year_act_temp,
        "one_year_act_light": one_year_act_light,
        "one_year_act_soil": one_year_act_soil,
        "life_act_temp": life_act_temp,
        "life_act_light": life_act_light,
        "life_act_soil": life_act_soil,
        "one_day_size_height": one_day_size_height,
        "one_month_size_height": one_month_size_height,
        "one_year_size_height": one_year_size_height,
        "life_size_height": life_size_height,
        "plant_image": plant_image,
        "greenrooms": greenrooms[0],
        "sidebar": prepare_sidebar()
        
    }

    return render_template('report-generate-test.html', data=data_template)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == '__main__':
    aws_iot_connection()
    app.run(debug=True)
    