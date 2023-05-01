import socket
import math
import pandas as pd
import plotly.express as px
import time

HOST = "172.20.10.2"
PORT = 2000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    temperature_arr = []
    humidity_arr = []
    index_arr = []
    time_arr = []
    temperature = 0
    humidity = 0
    index = 0
    thresh = 0

    temp = 0

    sendback = ""
    for i in range(1,51):
        time_arr.append(i)
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            x = data.split()
            temperature = float(x[0])
            temperature = (temperature*9)/5 + 32

            humidity = float(x[1])
            thresh = float(x[2])
            
            if temperature <= 40:
                index = temperature
            elif temperature < 79:
                index = (temperature*1.1) + (humidity*0.047) - 10.3
            else:
                tsq = temperature * temperature
                hsq = humidity * humidity
                b = (2.049*temperature) + (10.143*humidity) - (0.225*temperature*humidity) - (6.838*0.001*tsq) - (5.482*0.01*hsq) + (1.229*0.001*tsq*humidity) + (8.5282*0.0001*temperature*hsq) - (1.99*tsq*hsq*0.000001) - 42.379
                if (humidity < 13) and (temperature <= 112):
                    index = b - ((13-humidity)/4)*math.sqrt((17-(temperature-95))/17)
                elif (humidity > 85) and (temperature <= 87):
                    index = b + 0.02*(humidity-85)*(87-temperature)
                else :
                    index = b

            if temperature != 32.0:
                length = len(temperature_arr)
                if length < 51:
                    temperature_arr.append(temperature)
                    humidity_arr.append(humidity)
                    index_arr.append(index)
                elif (length == 51) and (temp == 0):
                    temperature_arr.pop(0)
                    humidity_arr.pop(0)
                    index_arr.pop(0)
                    double_arr = []
                    double_arr.append(time_arr)
                    double_arr.append(temperature_arr)
                    double_arr.append(humidity_arr)
                    double_arr.append(index_arr)

                    a = pd.DataFrame(double_arr)
                    df = a.transpose()
                    df.columns = ['Time', 'Temperature', 'Humidity', 'Index']
                    vals = ['Temperature', 'Humidity', 'Index']

                    fig = px.line(df, x='Time', y=vals, title="Heat Index Computations")
                    fig.update_yaxes(title_text="Temperature in F / % Humidity")
                    fig.update_xaxes(title_text="Trial Number")
                    fig.write_image("output.png")

                    temp = 1

                if index >= thresh:
                    sendback = "1"
                else :
                    sendback = "0"
                #send back value for fan speed eventually...
                send = bytes(sendback, 'utf-8')
                conn.sendall(send)

                time.sleep(2)

            if not data:
                break
