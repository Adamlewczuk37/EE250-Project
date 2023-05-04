import grovepi
import time
from grove_rgb_lcd import *
import math
import threading
import socket

HOST = '172.20.10.2'
PORT = 2000

def main():
	tempsensor = 4
	potentiometer = 0
	button = 3
	buttonState = 0

	grovepi.pinMode(tempsensor,"INPUT")
	grovepi.pinMode(potentiometer,"INPUT")
	grovepi.pinMode(button, "INPUT")

	textCommand(0x01)
	lock = threading.Lock()

	time.sleep(1)

	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))

		while True:
			output = ""
			[temperature,humidity] = grovepi.dht(tempsensor,0)
			if not math.isnan(temperature) and not math.isnan(humidity):
				output = str(temperature) + " " + str(humidity)
			else:
				output = "0" + " 0"

			thresh = grovepi.analogRead(potentiometer)
			thresh = thresh / 10
			output = output + " " + str(thresh)

			if grovepi.digitalRead(button):
				output += " 1"
				buttonState = 1
			else:
				output += " 0"
			arr = bytes(output, 'utf-8')
			s.sendall(arr)

			display = "Threshold: " + str(thresh)

			if buttonState:
				break
			time.sleep(1)
			data = s.recv(1024)
			if not data:
				break
			data = str(data)
			data = data.strip('\'b')
			with lock:
				if (data == "RED"):
					setRGB(255,0,0)
				else:
					setRGB(0,0,255)
				setText_norefresh(display)
pass

if __name__ == '__main__':
    main()