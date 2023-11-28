from faker import Faker
import mysql.connector
from datetime import datetime, timedelta
import random


fake = Faker()

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot_greenroom"
    )
    return connection


def seed_temperature_sensor():
    conn = connect_db()
    cursor = conn.cursor()
    for _ in range(100):  # Adjust the number of records you want to create
        value = random.uniform(20.0, 30.0)  # Example temperature range
        greenroom_id = 1
        # timestamp today across a range of 24 hours and the end date is the end of today
        # timestamp = fake.date_time_between(start_date='today', end_date='today 23:59:59', tzinfo=None)
        timestamp = fake.date_time_between(start_date='-1d', end_date='+1d', tzinfo=None)
        
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        sql = "INSERT INTO `temperature_sensor`(`value`, `timestamp`, `greenroom_id`) VALUES (%s, %s, %s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()

def seed_soil_sensor():
    conn = connect_db()
    cursor = conn.cursor()
    for _ in range(100):  # Adjust the number of records you want to create
        value = random.uniform(0,100)  # Example temperature range
        greenroom_id = 1
        # timestamp today across a range of 24 hours and the end date is the end of today
        # timestamp = fake.date_time_between(start_date='today', end_date='today 23:59:59', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-1d', end_date='+1d', tzinfo=None)
        timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        sql = "INSERT INTO `soil_moisture_sensor`(`value`, `timestamp`, `greenroom_id`) VALUES (%s, %s, %s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()

def seed_light_sensor():
    conn = connect_db()
    cursor = conn.cursor()
    for _ in range(100):  # Adjust the number of records you want to create
        value = random.uniform(100,1000)  # Example temperature range
        greenroom_id = 1
        # timestamp today across a range of 24 hours and the end date is the end of today
        # timestamp = fake.date_time_between(start_date='today', end_date='today 23:59:59', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-1d', end_date='+1d', tzinfo=None)
        timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        sql = "INSERT INTO `light_sensor`(`value`, `timestamp`, `greenroom_id`) VALUES (%s, %s, %s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()

def seed_plant_height_size():
    
    size = 20
    height = 20
    # tiemstamp is the start of this month
    now = datetime.now()
    timestamp = datetime(now.year, 1, 1)
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(30):  # Adjust the number of records you want to create

        size = size + round(random.uniform(0,10),2) 
        height = height + round(random.uniform(0,10),2) 
        
        # add one day to this month
        timestamp = timestamp + timedelta(days=30)
        # timestamp =  datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        print(height, timestamp)

        greenroom_id = 1
        # timestamp = fake.date_time_between(start_date='today', end_date='today 23:59:59', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-1d', end_date='+1d', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        sql = "INSERT INTO `plant_size_height`(`size`, `height`, `timestamp`, `greenroom_id`) VALUES (%s,%s,%s,%s)"
        param = (size, height, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()
    
def seed_actuator_temp():
    # tiemstamp is the start of this month
    now = datetime.now()
    timestamp = datetime(now.year, now.month, 1)
    # timestamp = datetime(now.year, 1, 1)
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(30):  # Adjust the number of records you want to create

        value = random.randint(0,1)
        # add one day to this month
        timestamp = timestamp + timedelta(days=30)
        # timestamp =  datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        greenroom_id = 1
        # timestamp = fake.date_time_between(start_date='today', end_date='today 23:59:59', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-1d', end_date='+1d', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        # timestamp = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None)
        sql = "INSERT INTO `light_actuator_activity`(`action`, `timestamp`, `greenroom_id`) VALUES (%s,%s,%s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()
    
# Repeat the pattern for other sensor tables (air_moisture_sensor, soil_moisture_sensor, water_level_sensor)

def seed_greenroom():
    conn = connect_db()
    cursor = conn.cursor()
    for _ in range(5):  # Adjust the number of records you want to create
        name = fake.word()
        location = fake.city()
        description = fake.text()
        image_url = fake.image_url()
        sql = "INSERT INTO greenroom (name, location, description, image) VALUES (%s, %s, %s, %s)"
        param = (name, location, description, image_url)
        cursor.execute(sql, param)
    conn.commit()
    


# Create seed functions for other tables (e.g., temperature_actuator_activity, light_actuator_activity, etc.)

# Example usage:
# seed_temperature_sensor()
seed_actuator_temp()
# Call other seed functions for different sensor tables
# seed_greenroom()
# Call seed functions for other tables
