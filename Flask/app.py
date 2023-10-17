from flask import Flask, render_template, request, redirect, url_for, flash, session
import paho.mqtt.client as mqtt
import os
import json

app = Flask(__name__)

# IP address may change each time broker is restarted
MQTT_SERVER = "192.168.0.16"
topic = 'test_channel'
port = 5000

def on_connect(client, userdata, flags, rc):
    client.publish(topic, "STARTING SERVER")
    client.publish(topic, "CONNECTED")


def on_message(client, userdata, msg):
    client.publish(topic, "MESSAGE")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greenroom-detail')
def page_greenroom_detail():
    return render_template('greenroom-detail.html')

@app.route('/manual', methods=['GET', 'POST'])
# Template for publishing manual control messages through MQTT
def manual_control():
    # Defines all the name of "modules" to loop through (the name should match the "name" attr in form)
    all_param = ["nutrient", "light"]
    for param in all_param:
        # Get the posted value
        value = request.form.get(param)
        if value != "None":
            msg = f"{param}:{value}"
            client.publish(topic, msg)

    return render_template('manual_control.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

if __name__ == '__main__':
    client = mqtt.Client()
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER)
    client.loop_start()

    app.run(host='0.0.0.0', port=port)