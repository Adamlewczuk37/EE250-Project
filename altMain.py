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

def calc_H_Index(temperature, relative_humidity):
	# Constants in the formula
	c1 = -42.379
	c2 = 2.04901523
	c3 = 10.14333127
	c4 = -0.22475541
	c5 = -0.00683783
	c6 = -0.05481717
	c7 = 0.00122874
	c8 = 0.00085282
	c9 = -0.00000199

	hi = c1 + c2*temperature + c3*relative_humidity + c4*temperature*relative_humidity + c5*temperature**2 + c6*relative_humidity**2 + c7*temperature**2*relative_humidity + c8*temperature*relative_humidity**2 + c9*temperature**2*relative_humidity**2

	if temperature >= 80 and temperature <= 112 and relative_humidity < 13:
		adjustment = ((13 - relative_humidity)/4) * math.sqrt((17 - abs(temperature - 95))/17)
		hi += adjustment
	elif relative_humidity > 85 and temperature >= 80 and temperature <= 87:
		adjustment = ((relative_humidity - 85)/10) * ((87 - temperature)/5)
		hi -= adjustment

	# Apply a final adjustment if the HI is less than 80
	if hi < 80:
		hi = 0.5 * (temperature + 61 + (temperature - 68)*0.5 + relative_humidity*0.094)

	return hi

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



