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

# def select_by_id(id:int):
#     conn = connect_db()
#     cursor = conn.cursor()

#     sql = "SELECT name FROM greenroom WHERE id = %s LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()

#     gr = {
#         "id" : id,
#         "name" : result[0]
#     }

#     sql = "SELECT reading,time FROM sensor WHERE type = 'level' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     if result[0] == "0":
#         gr["nutrientLow"] = True
#     else:
#         gr["nutrientLow"] = False

#     sql = "SELECT reading,time FROM sensor WHERE type = 'light' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["light"] = result[0]

#     sql = "SELECT reading,time FROM sensor WHERE type = 'moisture' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["moisture"] = result[0]

#     sql = "SELECT reading,time FROM sensor WHERE type = 'temperature' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["temperature"] = result[0]

#     sql = "SELECT status,time FROM actuator WHERE type = 'nutrient' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["nutrientStatus"] = result[0]
#     if(result[0] == "1"):
#         gr["nutrientTime"] = result[1] + timedelta(minutes=5)
#     else:
#         gr["nutrientTime"] = result[1]
    

#     sql = "SELECT status,time FROM actuator WHERE type = 'light' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["lightStatus"] = result[0]
#     gr["lightTime"] = result[1]

#     sql = "SELECT status,time FROM actuator WHERE type = 'water' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["waterStatus"] = result[0]
#     if(result[0] == "1"):
#         gr["waterTime"] = result[1] + timedelta(minutes=4)
#     else:
#         gr["waterTime"] = result[1]

#     sql = "SELECT status,time FROM actuator WHERE type = 'fan' AND greenroom = %s ORDER BY time DESC LIMIT 1"
#     param = (id,)
#     cursor.execute(sql, param)
#     result = cursor.fetchone()
#     gr["fanStatus"] = result[0]
#     gr["fanTime"] = result[1]

#     return gr

# def init_db():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM greenroom")
#     result = cursor.fetchall()
    
#     greenroom = []
#     for r in result:
#         gr = select_by_id(r[0])
#         greenroom.append(gr)
        
#     print(greenroom)

#     return greenroom

# def insert_sensor_by_type(type:str, reading:str, id:int):
#     conn = connect_db()
#     cursor = conn.cursor()
#     sql = "INSERT INTO sensor (type,reading,greenroom) VALUES (%s,%s,%s)"
#     param = (type, reading, id,)
#     cursor.execute(sql, param)
#     conn.commit()

# def insert_actuator_by_type(type:str, status:str, id:int):
#     conn = connect_db()
#     cursor = conn.cursor()
#     sql = "INSERT INTO actuator (type,status,greenroom) VALUES (%s,%s,%s)"
#     param = (type, status, id,)
#     cursor.execute(sql, param)
#     conn.commit()
    