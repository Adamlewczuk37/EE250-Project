# echo-server.py
import socket
import math
import pandas as pd
import plotly.express as px

HOST = "172.20.10.2"  # Standard loopback interface address (localhost)
PORT = 2000  # Port to listen on (non-privileged ports are > 1023)

incomingData = []
temperature = 0
RH = 0
threshold = 0
H_index = 0
buttonState = 0
time = 1
output = ""

double_list = []
temp_list = []
RH_list=[]
H_index_list = []
time_list = []


def calc_H_Index(T, RH):
	HI = -42.379 + 2.04901523*T + 10.14333127*RH - .22475541*T*RH - .00683783*T*T - .05481717*RH*RH + .00122874*T*T*RH + .00085282*T*RH*RH - .00000199*T*T*RH*RH
	if T >= 80 and T <= 112 and RH < 13:
		adjustment = ((13-RH)/4)*math.sqrt((17-abs(T-95))/17)
		HI += adjustment
	elif RH > 85 and T >= 80 and T <= 87:
		adjustment = ((RH-85)/10) * ((87-T)/5)
		HI -= adjustment
	elif HI < 80:
		HI = 0.5 * (T+61+(T-68)*1.2 + RH*0.094)
	return HI


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print(f"Connected by {addr}")
		while True:
			data = conn.recv(1024)
			if not data:
				break
			data = str(data)
			data = data.strip("\'b")
			incomingData = data.split()

			temperature = float(incomingData[0])*9/5 + 32
			RH = float(incomingData[1])
			threshold = float(incomingData[2])
			H_index = calc_H_Index(temperature, RH)
			buttonState = float(incomingData[3])

			temp_list.append(temperature)
			RH_list.append(RH)
			H_index_list.append(H_index)
			time_list.append(time)
			time += 1

			#print(str(temperature) + " " + str(RH) + " " + str(threshold) + " " + str(H_index))
			if buttonState:
				break
			if H_index < threshold:
				output = "RED "
			else:
				output = "BLUE "
			
			output = output + str(H_index) + " "
			
			diff = H_index - threshold
			if diff > 25:
				output = output + "255"
			elif diff > 20:
				output = output + "128"
			elif diff > 15:
				output = output + "8"
			elif diff > 10:
				output = output + "5"
			elif diff > 5:
				output = output + "3"
			else:
				output = output + "0"

			arr = bytes(output, 'utf-8')
			conn.sendall(arr)

temp_list.pop(0)
RH_list.pop(0)
H_index_list.pop(0)
time_list.pop(0)
double_list.append(time_list)
double_list.append(temp_list)
double_list.append(RH_list)
double_list.append(H_index_list)

a = pd.DataFrame(double_list)
df = a.transpose()
df.columns = ['Time', 'Temperature', 'Humidity', 'Index']
vals = ['Temperature', 'Humidity', 'Index']

fig = px.line(df, x='Time', y=vals, title="Heat Index Computations")
fig.update_yaxes(title_text="Temperature in F / % Humidity")
fig.update_xaxes(title_text="Trial Number")

# Save the figure as a PNG image
fig.write_image("metrics.png")
