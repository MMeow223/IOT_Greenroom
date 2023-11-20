# import serial

# PORT1 = "COM6"
# PORT2 = "COM8"

# # connect to two arduinos
# arduino_1 = serial.Serial(PORT1, 9600)
# arduino_2 = serial.Serial(PORT2, 9600)

# while True:
#     # read from arduino 1
#     while arduino_1.in_waiting > 0:
#         line = arduino_1.readline().decode('utf-8').rstrip()
#         print(line)
        
#     # read from arduino 2
#     while arduino_2.in_waiting > 0:
#         line = arduino_2.readline().decode('utf-8').rstrip()
#         print(line)
        
#     # # write to arduino 1
#     # arduino_1.write("1".encode())

#     # # write to arduino 2
#     # arduino_2.write("1".encode())

#     # # close connection
#     # arduino_1.close()
#     # arduino_2.close()



serial_data = "temp:50|hum:100|soil:100|light:999|water:0"

data_array = serial_data.split("|")

for data in data_array:
    print(data.split(":")[1])
    data_dict = {
        "temp": data.split(":")[1],
        "hum": data.split(":")[1],
        "soil": data.split(":")[1],
        "light": data.split(":")[1],
        "water": data.split(":")[1],
    }

print(data_array)

