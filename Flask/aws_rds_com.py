import mysql.connector
from datetime import datetime, timedelta

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iot_launcher"
    )

    return connection

def select_by_id(id:int):
    conn = connect_db()
    cursor = conn.cursor()

    sql = "SELECT name FROM greenroom WHERE id = %s LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()

    gr = {
        "id" : id,
        "name" : result[0]
    }

    sql = "SELECT reading,time FROM sensor WHERE type = 'level' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    if result[0] == "0":
        gr["nutrientLow"] = True
    else:
        gr["nutrientLow"] = False

    sql = "SELECT reading,time FROM sensor WHERE type = 'light' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["light"] = result[0]

    sql = "SELECT reading,time FROM sensor WHERE type = 'moisture' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["moisture"] = result[0]

    sql = "SELECT reading,time FROM sensor WHERE type = 'temperature' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["temperature"] = result[0]

    sql = "SELECT status,time FROM actuator WHERE type = 'nutrient' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["nutrientStatus"] = result[0]
    if(result[0] == "1"):
        gr["nutrientTime"] = result[1] + timedelta(minutes=5)
    else:
        gr["nutrientTime"] = result[1]
    

    sql = "SELECT status,time FROM actuator WHERE type = 'light' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["lightStatus"] = result[0]
    gr["lightTime"] = result[1]

    sql = "SELECT status,time FROM actuator WHERE type = 'water' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["waterStatus"] = result[0]
    if(result[0] == "1"):
        gr["waterTime"] = result[1] + timedelta(minutes=4)
    else:
        gr["waterTime"] = result[1]

    sql = "SELECT status,time FROM actuator WHERE type = 'fan' AND greenroom = %s ORDER BY time DESC LIMIT 1"
    param = (id,)
    cursor.execute(sql, param)
    result = cursor.fetchone()
    gr["fanStatus"] = result[0]
    gr["fanTime"] = result[1]

    return gr

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM greenroom")
    result = cursor.fetchall()
    
    greenroom = []
    for r in result:
        gr = select_by_id(r[0])
        greenroom.append(gr)

    return greenroom

def insert_sensor_by_type(type:str, reading:str, id:int):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO sensor (type,reading,greenroom) VALUES (%s,%s,%s)"
    param = (type, reading, id,)
    cursor.execute(sql, param)
    conn.commit()

def insert_actuator_by_type(type:str, status:str, id:int):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO actuator (type,status,greenroom) VALUES (%s,%s,%s)"
    param = (type, status, id,)
    cursor.execute(sql, param)
    conn.commit()