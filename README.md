Team Member 1: Adam Lewczuk
Team Member 2: Michael Wasson

Hardware configuration:
Attach GrovePi shield to Raspberry Pi.
Button is attached to port D3.
Rotary Angle Sensor is attached to port A0
Temperature/Humidity sensor is attached to port D4
Fan is attached to port D5 (This part is not part of the given course kit and we had to buy it online)

Compilation/Excecution:
Before running the program, make sure to modify the HOST variable that is at the top of both main.py and rpi.py to whatever
ip address that corresponds to your server machine. 
Open a terminal on your server machine and run python3 main.py.
Open a terminal on your Raspberry Pi and run python3 rpi.py

Libraries used in client code:
grovepi
time
grove_rgb_lcd 
math
threading
socket

Libraries used in server code:
socket
math
pandas
plotly.express

Link to Video:
https://drive.google.com/file/d/1qe4SFgkK7w_Jo9f-NfF-FCd4asDb2KfI/view?usp=share_link
