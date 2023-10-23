from flask import Flask, render_template, request, redirect, url_for, flash, session
import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json

# Currently this connects to local db
import aws_rds_com as db

app = Flask(__name__)

# IP address may change each time broker is restarted
MQTT_SERVER = "172.20.10.4"
actuator_topic = 'actuator'
scheduler_topic = "scheduler"
sensor_topic = "sensor"
port = 5000

def on_connect(client, userdata, flags, rc):
    client.publish(actuator_topic, "STARTING SERVER")
    client.publish(actuator_topic, "CONNECTED")
    client.subscribe(sensor_topic)


def on_message(client, userdata, msg):
    payload = str(msg.payload, encoding='utf-8')
    print(payload)
    splitStr = payload.split(":")
    print(splitStr)
    secondSplit = splitStr[1].split(";")
    print(secondSplit)
    match splitStr[0]:
        case "Water":
            db.insert_sensor_by_type("moisture", secondSplit[0], secondSplit[1])
        case "Light Value":
            db.insert_sensor_by_type("light", secondSplit[0], secondSplit[1])
        case "Temperature":
            db.insert_sensor_by_type("temperature", secondSplit[0], secondSplit[1])
        case "level":
            db.insert_sensor_by_type("level", secondSplit[0], secondSplit[1])
        case "Growth Light":
            db.insert_actuator_by_type("light", secondSplit[0], secondSplit[1])
        case "Water Pump":
            db.insert_actuator_by_type("water", secondSplit[0], secondSplit[1])
        case "Fan":
            db.insert_actuator_by_type("fan", secondSplit[0], secondSplit[1])


@app.route('/', methods=['GET', 'POST'])
def index():
    greenroom = db.init_db()
    return render_template('index.html', greenroom=greenroom)

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

@app.route('/manual', methods=['GET', 'POST'])
# Template for publishing manual control messages through MQTT
def manual_control():
    # Defines all the name of "modules" to loop through (the name should match the "name" attr in form)
    all_param = ["nutrient", "light"]
    for param in all_param:
        # Get the posted value
        value = request.form.get(param)
        if value != None:
            msg = f"{param}:{value}"
            print(msg)
            client.publish(actuator_topic, msg)

    return render_template('manual_control.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

def scheduler_read_sensor():
    print("Publishing to read sensor data...")
    client.publish(scheduler_topic, "read")

if __name__ == '__main__':
    client = mqtt.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER)
    client.loop_start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduler_read_sensor, 'interval', minutes=15)
    scheduler.start()

    app.run(host='0.0.0.0', port=port)

    