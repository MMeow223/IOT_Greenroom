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
        password="password",
        database="iot_greenroom"
    )
    return connection


def get_record_all(type = { "soil_moisture", "water_level", "air_moisture", "light", "temperature"}):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM `"+TABLE_CONVERSION[type]+"`"
    
    cursor.execute(sql)
    # cursor.execute(sql, param)
    result = cursor.fetchall()
    
    result_list = []
    for row in result:
        result_dict = {
            "id": row[0],
            "value": str(row[1]),  # Convert Decimal to string
            "timestamp": row[2].strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
            "greenroom_id": row[3]
        }
        result_list.append(result_dict)
        
    return result_list

def get_record_greenroom(greenroom_id, today=False, type = { "soil_moisture", "water_level", "air_moisture", "light", "temperature"}):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM `"+TABLE_CONVERSION[type]+"` WHERE greenroom_id = %s AND timestamp >= %s"
    
    if today:
        # equal to 0:00:00 today
        date = datetime.now() - timedelta(days=1)
        # now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        # start from year 2023
        date = datetime(2023, 1, 1)
        
    param = (greenroom_id, date,)
    cursor.execute(sql, param)
    result = cursor.fetchall()
    
    result_list = []
    for row in result:
        result_dict = {
            "id": row[0],
            "value": str(row[1]),  # Convert Decimal to string
            "timestamp": row[2].strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
            "greenroom_id": row[3]
        }
        result_list.append(result_dict)
        
    return result_list



def get_record_date(date, type = { "soil_moisture", "water_level", "air_moisture", "light", "temperature"}):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM `"+TABLE_CONVERSION[type]+"`  WHERE timestamp = %s"
    param = (date,)
    cursor.execute(sql, param)
    result = cursor.fetchall()
    
    result_list = []
    for row in result:
        result_dict = {
            "id": row[0],
            "value": str(row[1]),  # Convert Decimal to string
            "timestamp": row[2].strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
            "greenroom_id": row[3]
        }
        result_list.append(result_dict)
        
    return result_list

def get_greenroom(id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM greenroom WHERE greenroom_id = %s"
    param = (id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    
    result_list = []
    for row in result:
        result_dict = {
            "greenroom_id": row[0],
            "name": row[1],  # Convert Decimal to string
            "location": row[2],  # Format datetime as string
            "desrciption": row[3],
            "image": row[4]
        }
        result_list.append(result_dict)
        
    return result_list

def get_greenroom_all():
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM greenroom"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    result_list = []
    for row in result:
        result_dict = {
            "greenroom_id": row[0],
            "name": row[1],  # Convert Decimal to string
            "location": row[2],  # Format datetime as string
            "desrciption": row[3],
            "image": row[4]
        }
        result_list.append(result_dict)
        
    return result_list

def create_greenroom(name, location, description,image_url):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO greenroom (name, location, description, image) VALUES (%s, %s, %s, %s)"
    param = (name, location, description,image_url,)
    cursor.execute(sql, param)
    conn.commit()

def get_record_greenroom_all_actuator_one(greenroom_id, today=False):
    ACTUATOR_CONVERSION = {
        'temperature_actuator_activity' : "temperature",
        'light_actuator_activity' : "light",
        'air_moisture_actuator_activity' : "air",
        'soil_moisture_actuator_activity' : "moisture",
        'water_level_actuator_activity' : "water"
    }

    result_dict = {}
    table_name = [
        'temperature_actuator_activity',
        'light_actuator_activity',
        'air_moisture_actuator_activity',
        'soil_moisture_actuator_activity',
        'water_level_actuator_activity'
    ]

    conn = connect_db()
    cursor = conn.cursor()

    for t in table_name:
        sql = "SELECT action,timestamp FROM `"+t+"` WHERE greenroom_id = %s AND timestamp >= %s ORDER BY timestamp DESC LIMIT 1"

        if today:
            # equal to 0:00:00 today
            date = datetime.now() - timedelta(days=1)
            # now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # start from year 2023
            date = datetime(2023, 1, 1)
            
        param = (greenroom_id, date,)
        cursor.execute(sql, param)
        result = cursor.fetchone()
        
        param_action = ACTUATOR_CONVERSION[t]+"_action"
        param_timestamp = ACTUATOR_CONVERSION[t]+"_timestamp"

        if result != None :
            result_dict[param_action] = result[0]
            result_dict[param_timestamp] = result[1].strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as string        
        
    return result_dict

def get_record_greenroom_all_actuator_mode_one(greenroom_id, today=False):
    ACTUATOR_MODE_CONVERSION = {
        'temperature_actuator_mode' : 'temperature_mode',
        'light_actuator_mode' : 'light_mode',
        'soil_moisture_actuator_mode' : 'moisture_mode'
    }

    result_dict = {}
    table_name = [
        'temperature_actuator_mode',
        'light_actuator_mode',
        'soil_moisture_actuator_mode',
    ]

    conn = connect_db()
    cursor = conn.cursor()

    for t in table_name:
        sql = "SELECT mode FROM `"+t+"` WHERE greenroom_id = %s AND timestamp >= %s ORDER BY timestamp DESC LIMIT 1"

        if today:
            # equal to 0:00:00 today
            date = datetime.now() - timedelta(days=1)
            # now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # start from year 2023
            date = datetime(2023, 1, 1)
            
        param = (greenroom_id, date,)
        cursor.execute(sql, param)
        result = cursor.fetchone()
        
        param_action = ACTUATOR_MODE_CONVERSION[t]
        # param_timestamp = ACTUATOR_MODE_CONVERSION[t]+"_timestamp"

        if result != None :
            result_dict[param_action] = result[0]
            # result_dict[param_timestamp] = result[1].strftime('%Y-%m-%d %H:%M:%S')  # Format datetime as string        
        
    return result_dict

def insert_activity(type:str, action:str, greenroom_id:int):
    CONVERSION = {
        'temp' : "temperature_actuator_activity",
        'light' : "light_actuator_activity",
        'air' : "air_moisture_actuator_activity",
        'soil' : "soil_moisture_actuator_activity",
        'water' : "water_level_actuator_activity"
    }

    conn = connect_db()
    cursor = conn.cursor()
    table = CONVERSION[type]
    sql = "INSERT INTO `"+table+"` (action,greenroom_id) VALUES (%s,%s)"
    param = (action, greenroom_id)
    cursor.execute(sql, param)
    conn.commit()

def insert_sensor(type:str, value:float, greenroom_id:int):
    CONVERSION = {
        'temp' : "temperature_sensor",
        'light' : "light_sensor",
        'air' : "air_moisture_sensor",
        'soil' : "soil_moisture_sensor",
        'water' : "water_level_sensor"
    }

    conn = connect_db()
    cursor = conn.cursor()
    table = CONVERSION[type]
    sql = "INSERT INTO `"+table+"` (value,greenroom_id) VALUES (%s,%s)"
    param = (value, greenroom_id)
    cursor.execute(sql, param)
    conn.commit()

def update_mode(type:str, mode:str, greenroom_id:int):
    CONVERSION = {
        'temp' : "temperature_actuator_mode",
        'light' : "light_actuator_mode",
        'air' : "air_moisture_actuator_mode",
        'soil' : "soil_moisture_actuator_mode",
        'water' : "water_level_actuator_mode"
    }

    conn = connect_db()
    cursor = conn.cursor()
    table = CONVERSION[type]
    sql = "UPDATE `"+table+"` SET mode = %s WHERE greenroom_id = %s"
    param = (mode, greenroom_id)
    cursor.execute(sql, param)
    conn.commit()
    