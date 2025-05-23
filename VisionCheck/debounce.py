import time
from time import sleep
import Jetson.GPIO as GPIO
import threading



GPIO.setmode(GPIO.BOARD) 
GPIO.setup(7,GPIO.IN)
# inState = False

try:
    while True:
        IO = GPIO.input(7)
        if IO == True:     
            print(f"state is {IO}")
            sleep(0.5)
        else:
            print(f"state is {IO}")
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

        
