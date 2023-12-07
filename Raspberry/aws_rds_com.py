import mysql.connector
from datetime import datetime, timedelta

# CONSTANT
TABLE_CONVERSION = {
    'temperature': 'temperature_sensor',
    'light': 'light_sensor',
    'air_moisture': 'air_moisture_sensor',
    'soil_moisture': 'soil_moisture_sensor',
    'level': 'water_level_sensor'
}


def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot_greenroom_2"
    )
    return connection


def save_plant_image(url, greenroom_id:int):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO `plant_image`(`image_link`, `greenroom_id`) VALUES (%s, %s);"
    param = (url, greenroom_id,)
    cursor.execute(sql, param)
    cursor.close()
    