'''
Main module of control:

1. Sleep module
2. Check Distance to obstacle
3. If < threshold, call predict.py
4. Call motor_control.py
5. Check if any data has to be saved.
6. Switch off everything.
'''
import picamera
import subprocess
import time
import ultrasonic_1
import predict
#import motor_control

DISTANCE_THRESHOLD=12
CAMERA = picamera.PiCamera()

def check_for_object():

    distance=ultrasonic_1.measure()

    while (distance>DISTANCE_THRESHOLD):
        time.sleep(1)
        distance=ultrasonic_1.measure()
        #Sleep for 1 second

def take_picture():

    CAMERA.capture('./input/image.jpg')

def main():
    s1=time.clock()
    check_for_object()
    take_picture()
    score=predict.predict()
    s2=time.clock()
    print s2-s1
    #motor_control.(score)

if __name__=='__main__':
    main()
