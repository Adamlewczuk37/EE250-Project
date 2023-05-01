import grovepi
import time
from grove_rgb_lcd import *
import math
import threading
import socket

HOST = '172.20.10.2'
PORT = 2000

def main():
    # set I2C to use the hardware bus
    grovepi.set_bus("RPI_1")

    tempsensor = 4
    LCD = 1
    potentiometer = 0
    #fan = 1

    lock = threading.Lock()

    grovepi.pinMode(tempsensor,"INPUT")
    grovepi.pinMode(potentiometer,"INPUT")
    grovepi.pinMode(LCD,"OUTPUT")
    #grovepi.pinMode(fan,"OUTPUT")

    time.sleep(1)

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            output = ""
            [temperature,humidity] = grovepi.dht(tempsensor,0)  
            if math.isnan(temperature) == False and math.isnan(humidity) == False:
                output = str(temperature) + " " + str(humidity)
            else:
                output = "0" + " 0"
            
            
            thresh = grovepi.analogRead(potentiometer)
            while thresh > 1023:
                thresh = grovepi.analogRead(potentiometer)

            thresh = thresh / 10
            output = output + " " + str(thresh)
            arr = bytes(output, 'utf-8')

            s.sendall(arr) 

            data = s.recv(1024)
            y = data.split()
            state = int(y[0])
            #power = float(y[1])

            display = "Threshold: " + str(thresh)
            with lock:
                if state == 0:
                    setRGB(255,0,0)
                elif state == 1:
                    setRGB(0,0,255)
                setText_norefresh(display)
            
            #with lock: 
          
            time.sleep(1)
    pass

if __name__ == '__main__':
    main()