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
        database="iot_greenroom_2"
    )
    return connection

def seed_temperature_sensor(id):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime(2019,1,1)
    for _ in range(1825):  # Adjust the number of records you want to create
        value = random.uniform(20.0, 30.0)  # Example temperature range
        greenroom_id = id
        
        timestamp = timestamp + timedelta(days=1)

        sql = "INSERT INTO `temperature_sensor`(`value`, `timestamp`, `greenroom_id`) VALUES (%s, %s, %s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()

def seed_soil_sensor(id):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime(2019,1,1)
    for _ in range(1825):  # Adjust the number of records you want to create
        value = random.uniform(0,100)  # Example temperature range
        greenroom_id = id
        
        timestamp = timestamp + timedelta(days=1)
            
        sql = "INSERT INTO `soil_moisture_sensor`(`value`, `timestamp`, `greenroom_id`) VALUES (%s, %s, %s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()

def seed_light_sensor(id):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime(2019,1,1)
    for _ in range(1825):  # Adjust the number of records you want to create
        value = random.uniform(100,1000)  # Example temperature range
        greenroom_id = id
        
        timestamp = timestamp + timedelta(days=1)
      
        sql = "INSERT INTO `light_sensor`(`value`, `timestamp`, `greenroom_id`) VALUES (%s, %s, %s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()

def seed_plant_height_size(id):
    
    size = 1
    height = 1
    timestamp = datetime(2019,1,1)

    conn = connect_db()
    cursor = conn.cursor()
    for i in range(1825):  # Adjust the number of records you want to create
        greenroom_id = id
        
        if(random.randint(0,10) < 3):
            size = size + round(random.uniform(0,1),2) 
            height = height + round(random.uniform(0,1),2) 
            
        timestamp = timestamp + timedelta(days=1)

        sql = "INSERT INTO `plant_size_height`(`size`, `height`, `timestamp`, `greenroom_id`) VALUES (%s,%s,%s,%s)"
        param = (size, height, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()
    
def seed_actuator_temp(id):
    # tiemstamp is the start of this month
    timestamp = datetime(2019,1,1)
    
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(1825):  # Adjust the number of records you want to create
        greenroom_id = id

        value = random.randint(0,1)
        timestamp = timestamp + timedelta(days=1)
        
        sql = "INSERT INTO `temperature_actuator_activity`(`action`, `timestamp`, `greenroom_id`) VALUES (%s,%s,%s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()
    
def seed_actuator_light(id):
    # tiemstamp is the start of this month
    timestamp = datetime(2019,1,1)
    
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(1825):  # Adjust the number of records you want to create
        greenroom_id = id

        value = random.randint(0,1)
        timestamp = timestamp + timedelta(days=1)
        
        sql = "INSERT INTO `light_actuator_activity`(`action`, `timestamp`, `greenroom_id`) VALUES (%s,%s,%s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()
# Repeat the pattern for other sensor tables (air_moisture_sensor, soil_moisture_sensor, water_level_sensor)


def seed_actuator_soil(id):
    # tiemstamp is the start of this month
    timestamp = datetime(2019,1,1)
    
    conn = connect_db()
    cursor = conn.cursor()
    for i in range(1825):  # Adjust the number of records you want to create
        greenroom_id = id

        value = random.randint(0,1)
        timestamp = timestamp + timedelta(days=1)
        
        sql = "INSERT INTO `soil_moisture_actuator_activity`(`action`, `timestamp`, `greenroom_id`) VALUES (%s,%s,%s)"
        param = (value, timestamp, greenroom_id)
        cursor.execute(sql, param)
    conn.commit()
    
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


# seed_temperature_sensor(1)
# seed_temperature_sensor(2)

# seed_soil_sensor(1)
# seed_soil_sensor(2)

# seed_light_sensor(1)
# seed_light_sensor(2)

seed_plant_height_size(1)
seed_plant_height_size(2)

# seed_actuator_temp(1)
# seed_actuator_temp(2)

# seed_actuator_light(1)
# seed_actuator_light(2)

# seed_actuator_soil(1)
# seed_actuator_soil(2)




# Example usage:
# seed_temperature_sensor()
# seed_actuator_temp()
# Call other seed functions for different sensor tables
# seed_greenroom()
# Call seed functions for other tables
