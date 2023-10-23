import paho.mqtt.client as mqtt #import library
import serial
 
MQTT_SERVER = "172.20.10.4" #specify the broker address, it can be IP of raspberry pi or simply localhost
actuator_topic = "actuator" #this is the name of topic, like temp
scheduler_topic = "scheduler"
sensor_topic = "sensor"
dict = {
    "light:0" : "30",
    "light:1" : "1",
    "light:2" : "2",
    "light:3" : "3",
    "fan:0" : "40",
    "fan:1" : "4",
    "water:0" : "50",
    "water:1" : "5",
    "nutrient:0" : "60",
    "nutrient:1" : "6",
    "read" : "999"
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(actuator_topic)
    client.subscribe(scheduler_topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "actuator":
        payload = str(msg.payload, 'utf-8')
        print("Received--"+payload)
        if(arduino.isOpen == False):
            arduino.open()
        arduino.write(dict[payload].encode())
    elif msg.topic == "scheduler":
        payload = str(msg.payload, 'utf-8')
        print("Received--"+payload)
        if(arduino.isOpen == False):
            arduino.open()
        arduino.write(dict[payload].encode())
        while arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').rstrip()
            splitStr = line.split(":")
            line = line + ";1"
            print(line)
            client.publish(sensor_topic, line)
              
    
def arduino_connection():
    arduino = serial.Serial('/dev/ttyUSB0',9600)
    return arduino

arduino = arduino_connection()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()
