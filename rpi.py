import grovepi
import time
from grove_rgb_lcd import *
import math

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")
sensor = 1  # The Sensor goes on digital port 4.

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.

while True:
	try:
		# This example uses the blue colored sensor. 
		# The first parameter is the port, the second parameter is the type of sensor.
		[temp,humidity] = grovepi.dht(sensor,blue)  
		if math.isnan(temp) == False and math.isnan(humidity) == False:
			print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))

	except IOError:
		print ("Error")
