''' Socket to indicate change in motion in IR'''

import RPi.GPIO as GPIO
import time

def indicate():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(14, GPIO.IN)         #Read output from PIR motion sensor
    while True:
        i=GPIO.input(14)
        if i==0:                 #When output from motion sensor is LOW
            print "No intruders",i
            time.sleep(0.1)
        elif i==1:               #When output from motion sensor is HIGH
            print "Intruder detected",i
            time.sleep(0.1)

if __name__=='__main__':
    indicate()
