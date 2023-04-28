import grovepi
import time
import sys
import threading
from grove_rgb_lcd import *

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
ultrasonic_ranger = 4

lock = threading.Lock()

# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0

LCD = 1

grovepi.pinMode(potentiometer,"INPUT")
grovepi.pinMode(LCD, "OUTPUT")


time.sleep(1)

set_val = 0
dist = 0
string1 = ""
string2 = ""

while True:
    try:
        dist = grovepi.ultrasonicRead(ultrasonic_ranger)
        set_val = grovepi.analogRead(potentiometer)

    except Exception as e:
        print ("Error:{}".format(e))
    
    if (dist > set_val):
        with lock:
            setRGB(0,255,0)
        string1 = str(set_val) + "cm" + "\n"
        string2 = str(dist) + "cm"
        with lock:
            setText_norefresh(string1 + string2)
    else:
        with lock:
            setRGB(255,0,0)
        string1 = str(set_val) + "cm OBJ PRES" + "\n"
        string2 = str(dist) + "cm"
        with lock:
            setText_norefresh(string1 + string2)
    
    time.sleep(0.1) # don't overload the i2c bus