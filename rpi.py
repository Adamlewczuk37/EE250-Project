import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.IN)
import time
import Adafruit_MCP3008
from Adafruit_GPIO import SPI
#import socket

HOST = '172.20.10.3'
PORT = 8901

def main():
    output = 11
    SPI_PORT   = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    GPIO.setup(output, GPIO.OUT, initial=GPIO.LOW)

    temperature = 0
    rotary = 0
    button = 0

    state = 0
    low_ac_thresh = 78
    hi_ac_thresh = 95
    low_heat_thresh = 62
    hi_heat_thresh = 45

    output2 = ""

    GPIO.output(output, 1)


    while 1: 
        rotary = mcp.read_adc(0)
        button = GPIO.input(16)
        print("rotary: ")
        print(rotary)
        print("button: ")
        print(button)

        if button:
            if (state == 3):
                state = 0
            else :
                state = state + 1

        if rotary:
            if (state == 0):
                #update_hi_heat_thresh
                print("0")
                print(hi_heat_thresh)
            elif (state == 1):
                #update_low_heat_thresh
                print("1")
                print(low_heat_thresh)
            elif (state == 2):
                #update_low_ac_thresh
                print("2")
                print(low_ac_thresh)
            else :
                #update_hi_ac_thresh
                print("3")
                print(hi_ac_thresh)
        

        
        temperature = GPIO.input(15)
        print("temperature: ")
        print(temperature)

        #output2 = str(hi_heat_thresh) + " " + str(low_heat_thresh) + " " + str(low_ac_thresh) + " " + str(hi_ac_thresh) + " " + str(temperature)
        
        #with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
         #   s.connect((HOST, PORT))

         #   inp = input(output2)
         #   arr = bytes(inp, 'utf-8')
         #   s.sendall(arr)

            #data = s.recv(1024)
            #print(f"{data!r}")
       # pass

        #output2 = ""


        time.sleep(0.5)

if __name__ == '__main__':
    main()