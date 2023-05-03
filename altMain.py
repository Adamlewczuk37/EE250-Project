# echo-server.py
import socket
import math
import plotly.express as px
from plotly.subplots import make_subplots
HOST = "172.20.10.7"  # Standard loopback interface address (localhost)
PORT = 2000  # Port to listen on (non-privileged ports are > 1023)

incomingData = []
temperature = 0
RH = 0
threshold = 0
H_index = 0
buttonState = 0
time = 1
output = ""

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
	if HI < 80:
		HI = 0.5 * (T+61+(T-68)*0.5 + RH*0.094)
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

			print(str(temperature) + " " + str(RH) + " " + str(threshold) + " " + str(H_index))
			if buttonState:
				break
			if H_index < threshold:
				output = "RED"
			else:
				output = "BLUE"

			arr = bytes(output, 'utf-8')
			conn.sendall(arr)

# Create a figure with three subplots
fig = make_subplots(rows=1, cols=3)

# Add a line plot to the first subplot
fig.add_trace(px.line(x=time_list, y=temp_list).data[0], row=1, col=1)
fig.update_xaxes(title_text="Time (s)", row=1, col=1)
fig.update_yaxes(title_text="Temperature 1 (F)", row=1, col=1)

# Add a line plot to the second subplot
fig.add_trace(px.line(x=time_list, y=RH_list).data[0], row=1, col=2)
fig.update_xaxes(title_text="Time (s)", row=1, col=2)
fig.update_yaxes(title_text="Relative Humidity", row=1, col=2)

# Add a line plot to the second subplot
fig.add_trace(px.line(x=time_list, y=H_index_list).data[0], row=1, col=3)
fig.update_xaxes(title_text="Time (s)", row=1, col=3)
fig.update_yaxes(title_text="Heat Index", row=1, col=3)


# Update the layout to include an overall title
fig.update_layout(title_text="Metrics with respect to time", title_x=0.5)

# Save the figure as a PNG image
fig.write_image("metrics.png")



