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


def get_record_all(type = { "soil_moisture", "water_level", "air_moisture", "light", "temperature"}):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM `"+TABLE_CONVERSION[type]+"`"
    
    cursor.execute(sql)
    # cursor.execute(sql, param)
    result = cursor.fetchall()
    cursor.close()

    
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
    
    print(sql)
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
    cursor.close()

    
    result_list = []
    for row in result:
        result_dict = {
            "id": row[0],
            "value": str(row[1]),  # Convert Decimal to string
            "timestamp": row[2].strftime('%Y-%m-%d %H:%M:%S'),  # Format datetime as string
            "greenroom_id": row[3]
        }
        result_list.append(result_dict)
    
    print(result_list)
    return result_list



def get_record_date(date, type = { "soil_moisture", "water_level", "air_moisture", "light", "temperature"}):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM `"+TABLE_CONVERSION[type]+"`  WHERE timestamp = %s"
    param = (date,)
    cursor.execute(sql, param)
    result = cursor.fetchall()
    cursor.close()

    
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
    cursor.close()

    
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
    cursor.close()

    
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

def get_record_greenroom_all_actuator_threshold_one(greenroom_id, today=False):
    ACTUATOR_MODE_CONVERSION = {
        'temperature_actuator_threshold' : 'temperature_threshold',
        'light_actuator_threshold' : 'light_threshold',
        'soil_moisture_actuator_threshold' : 'moisture_threshold'
    }

    result_dict = {}
    table_name = [
        'temperature_actuator_threshold',
        'light_actuator_threshold',
        'soil_moisture_actuator_threshold',
    ]

    conn = connect_db()
    cursor = conn.cursor()

    for t in table_name:
        if t == 'light_actuator_threshold':
            brightness_level = [1, 2, 3]
            for level in brightness_level:
                sql = "SELECT threshold FROM `"+t+"` WHERE greenroom_id = %s AND level = %s ORDER BY timestamp DESC LIMIT 1"
                
                param = (greenroom_id, level,)
                cursor.execute(sql, param)
                result = cursor.fetchone()

                param_action = ACTUATOR_MODE_CONVERSION[t] + f'_{level}'

                if result != None :
                    result_dict[param_action] = result[0]
        else:
            sql = "SELECT threshold FROM `"+t+"` WHERE greenroom_id = %s ORDER BY timestamp DESC LIMIT 1"
                
            param = (greenroom_id,)
            cursor.execute(sql, param)
            result = cursor.fetchone()
            
            param_action = ACTUATOR_MODE_CONVERSION[t]

            if result != None :
                result_dict[param_action] = result[0]   
        
    return result_dict

def insert_threshold(type:str, threshold:float, greenroom_id:int, level:int = None):
    CONVERSION = {
        'temp' : "temperature_actuator_threshold",
        'light' : "light_actuator_threshold",
        'soil' : "soil_moisture_actuator_threshold"
    }

    conn = connect_db()
    cursor = conn.cursor()
    table = CONVERSION[type]

    if table == "light_actuator_threshold":
        sql = "INSERT INTO `"+table+"` (threshold,greenroom_id,level) VALUES (%s,%s,%s)"
        param = (threshold, greenroom_id, level)
    else:
        sql = "INSERT INTO `"+table+"` (threshold,greenroom_id) VALUES (%s,%s)"
        param = (threshold, greenroom_id)
        
    cursor.execute(sql, param)
    conn.commit()

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
    

def get_one_day_record(table,greenroom_id):
    table_name = ["temperature_sensor", "light_sensor", "air_moisture_sensor", "soil_moisture_sensor", "water_level_sensor"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT EXTRACT(HOUR FROM timestamp) AS hour, AVG(value) AS average_temperature FROM '+table+' WHERE greenroom_id = %s AND EXTRACT(DAY FROM timestamp) = EXTRACT(DAY FROM CURRENT_DATE) AND EXTRACT(MONTH FROM timestamp) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM timestamp) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY hour ORDER BY hour;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "value": str(row[1]),  # Convert Decimal to string
            "label": str(row[0])  # Format datetime as string
        }
        result_list.append(result_dict)
        
    return result_list


def get_one_month_record(table,greenroom_id):
    table_name = ["temperature_sensor", "light_sensor", "air_moisture_sensor", "soil_moisture_sensor", "water_level_sensor"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT DATE(timestamp) AS day, AVG(value) AS average_temperature FROM '+table+' WHERE greenroom_id = %s AND EXTRACT(MONTH FROM timestamp) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM timestamp) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY day ORDER BY day;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "value": str(row[1]),  # Convert Decimal to string
            "label": str(row[0])  # Format datetime as string
        }
        result_list.append(result_dict)
        
    return result_list
    
    
def get_one_year_record(table,greenroom_id):
    table_name = ["temperature_sensor", "light_sensor", "air_moisture_sensor", "soil_moisture_sensor", "water_level_sensor"]
    if table not in table_name:
        return "Table not found"
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT EXTRACT(MONTH FROM timestamp) AS month,AVG(value) AS average_temperature FROM '+table+' WHERE greenroom_id = %s AND EXTRACT(YEAR FROM timestamp) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY month ORDER BY month;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "value": str(row[1]),  # Convert Decimal to string
            "label": str(row[0])  # Format datetime as string
        }
        result_list.append(result_dict)
        
    return result_list
    
    
    


def get_life_time_record(table,greenroom_id):
    table_name = ["temperature_sensor", "light_sensor", "air_moisture_sensor", "soil_moisture_sensor", "water_level_sensor"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT EXTRACT(YEAR FROM timestamp) AS year, AVG(value) AS average_temperature FROM '+table+' WHERE greenroom_id = %s GROUP BY year ORDER BY year;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "value": str(row[1]),  # Convert Decimal to string
            "label": str(row[0])  # Format datetime as string
        }
        result_list.append(result_dict)
        
    return result_list

def get_actuator_one_day_record(table,greenroom_id):
    
    table_name = ["air_moisture_actuator_activity","soil_moisture_actuator_activity","temperature_actuator_activity","light_actuator_activity","water_level_actuator_activity"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT SUM(action = 1) AS count_1, SUM(action = 0) AS count_0 FROM '+table+' WHERE greenroom_id = %s AND DATE(timestamp) = CURRENT_DATE;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "count_0": str(row[0]),  # Format datetime as string
            "count_1": str(row[1])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list

def get_actuator_one_month_record(table,greenroom_id):
    
    table_name = ["air_moisture_actuator_activity","soil_moisture_actuator_activity","temperature_actuator_activity","light_actuator_activity","water_level_actuator_activity"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT SUM(count_1) AS total_count_1, SUM(count_0) AS total_count_0 FROM (SELECT SUM(CASE WHEN action = 1 THEN 1 ELSE 0 END) AS count_1, SUM(CASE WHEN action = 0 THEN 1 ELSE 0 END) AS count_0 FROM '+table+' WHERE greenroom_id = %s AND EXTRACT(MONTH FROM timestamp) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM timestamp) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY EXTRACT(DAY FROM timestamp)) AS daily_counts;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "count_0": str(row[0]),  # Format datetime as string
            "count_1": str(row[1])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list

def get_actuator_one_year_record(table,greenroom_id):
    
    table_name = ["air_moisture_actuator_activity","soil_moisture_actuator_activity","temperature_actuator_activity","light_actuator_activity","water_level_actuator_activity"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT EXTRACT(YEAR FROM timestamp) AS year, COUNT(*) AS total_actions, SUM(action = 1) AS count_1, SUM(action = 0) AS count_0 FROM '+table+' WHERE greenroom_id = %s GROUP BY year ORDER BY year;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "count_0": str(row[1]),  # Format datetime as string
            "count_1": str(row[2])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list

def get_actuator_life_time_record(table,greenroom_id):
    
    table_name = ["air_moisture_actuator_activity","soil_moisture_actuator_activity","temperature_actuator_activity","light_actuator_activity","water_level_actuator_activity"]
    if table not in table_name:
        return "Table not found"
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT EXTRACT(YEAR FROM timestamp) AS year, COUNT(*) AS total_actions, SUM(action = 1) AS count_1, SUM(action = 0) AS count_0 FROM '+table+' WHERE greenroom_id = %s GROUP BY year ORDER BY year;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "count_0": str(row[1]),  # Format datetime as string
            "count_1": str(row[2])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list
    
def get_plant_size_and_height_one_day_record(greenroom_id):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT HOUR(timestamp) AS hour, ROUND(AVG(height), 2) AS average_height, ROUND(AVG(size), 2) AS average_size FROM plant_size_height WHERE greenroom_id = %s AND DATE(timestamp) = CURDATE() GROUP BY HOUR(timestamp) ORDER BY hour;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "timestamp": str(row[0]),  # Format datetime as string
            "height": str(row[1]),  # Format datetime as string
            "size": str(row[2])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list

def get_plant_size_and_height_one_month_record(greenroom_id):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT DAY(timestamp) AS day, ROUND(AVG(height), 2) AS average_height, ROUND(AVG(size), 2) AS average_size FROM plant_size_height WHERE greenroom_id = %s AND MONTH(timestamp) = MONTH(CURDATE()) AND YEAR(timestamp) = YEAR(CURDATE()) GROUP BY DAY(timestamp) ORDER BY DAY(timestamp);'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "timestamp": str(row[0]),  # Format datetime as string
            "height": str(row[1]),  # Format datetime as string
            "size": str(row[2])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list

def get_plant_size_and_height_one_year_record(greenroom_id):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT MONTH(timestamp) AS month, ROUND(AVG(height), 2) AS average_height, ROUND(AVG(size), 2) AS average_size FROM plant_size_height WHERE greenroom_id = %s AND YEAR(timestamp) = YEAR(CURDATE()) GROUP BY MONTH(timestamp) ORDER BY MONTH(timestamp);'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "timestamp": str(row[0]),  # Format datetime as string
            "height": str(row[1]),  # Format datetime as string
            "size": str(row[2])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list

def get_plant_size_and_height_lifetime_record(greenroom_id):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT YEAR(timestamp) AS year, ROUND(AVG(height), 2) AS average_height, ROUND(AVG(size), 2) AS average_size FROM plant_size_height WHERE greenroom_id = %s GROUP BY YEAR(timestamp) ORDER BY YEAR(timestamp);'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()

    
    result_list = []
    for row in result:
        # return in value and label
        result_dict = {
            "timestamp": str(row[0]),  # Format datetime as string
            "height": str(row[1]),  # Format datetime as string
            "size": str(row[2])  # Convert Decimal to string
        }
        result_list.append(result_dict)
        
    return result_list


def get_plant_image(greenroom_id):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = 'SELECT * FROM plant_image WHERE greenroom_id = %s ORDER BY timestamp DESC;'
    param = (greenroom_id,)
    cursor.execute(sql,param)
    result = cursor.fetchall()
    cursor.close()
    
    result_list = []
    for row in result:
        # return in value and label
        # result_dict = {
        #     "timestamp": str(row[1]),  # Format datetime as string
        #     "image_link": str(row[2]),  # Format datetime as string
        # }
        result_list.append(str(row[2]))
            
    return result_list

def get_latest_sensor_data(table, greenroom_id:int):
    
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM `"+table+"` WHERE greenroom_id = %s ORDER BY timestamp desc LIMIT 1;"
    param = (greenroom_id,)
    cursor.execute(sql, param)
    result = cursor.fetchall()
    cursor.close()
    
    return result[0][0]
    