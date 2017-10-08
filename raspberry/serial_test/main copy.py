'''
Main module of control:

1. Sleep module
2. Check Distance to obstacle
3. If < threshold, call predict.py
4. Call motor_control.py
5. Check if any data has to be saved.
6. Switch off everything.
'''

import subprocess
import time
import ultrasonic_1
import predict_copy
import motor_control
import tensorflow as tf

DISTANCE_THRESHOLD=20

def check_for_object():

    distance=ultrasonic_1.measure()

    while (distance<DISTANCE_THRESHOLD):
        time.sleep(1)
        #Sleep for 1 second

def take_picture():
    subprocess.call('raspistill -o ./input/image.png -t 1010')

def main():

    check_for_object()
    take_picture()
    score=predict_copy.predict()
    #motor_control.(score)

if __name__=='__main__':

    main()
