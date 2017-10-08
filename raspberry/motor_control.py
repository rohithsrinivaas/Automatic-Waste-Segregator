'''
Configure timed pulse based motion movement

Subject to reliability of the Linux clock

Refer motor_logs.md for reported data.
'''


import sys
import time
import RPi.GPIO as GPIO
import math

mode=GPIO.getmode()
print mode
GPIO.cleanup()

sleeptime=1

## CONSTANTS
DISC_Forward=17
DISC_Backward=27
DISC_PWM_PIN=22
DISC_RPM=100.00
DISC_RPM_C=(DISC_RPM/60)*2*math.pi

BRUSH_Forward=6
BRUSH_Backward=5
BRUSH_PWM_PIN=13
BRUSH_RPM=200.00*7/12
BRUSH_RPM_C=(BRUSH_RPM/60)*2*math.pi

## SETUP
GPIO.setmode(GPIO.BCM)

GPIO.setup(DISC_Forward, GPIO.OUT)
GPIO.setup(DISC_Backward, GPIO.OUT)
GPIO.setup(DISC_PWM_PIN,GPIO.OUT)

DISC_PWM = GPIO.PWM(DISC_PWM_PIN,100)
DISC_PWM.start(40)

GPIO.setup(BRUSH_Forward, GPIO.OUT)
GPIO.setup(BRUSH_Backward, GPIO.OUT)
GPIO.setup(BRUSH_PWM_PIN,GPIO.OUT)

BRUSH_PWM = GPIO.PWM(BRUSH_PWM_PIN,100)
BRUSH_PWM.start(72)


def DISC_forward(theta):

    t=theta/DISC_RPM_C

    GPIO.output(DISC_Forward, GPIO.HIGH)
    GPIO.output(DISC_Backward, GPIO.LOW)

    print("Moving DISC Forward by theta \t",theta)
    time.sleep(t)
    GPIO.output(DISC_Forward, GPIO.LOW)

def DISC_reverse(theta):
    t=theta/DISC_RPM_C

    GPIO.output(DISC_Forward, GPIO.LOW)
    GPIO.output(DISC_Backward, GPIO.HIGH)

    print("Moving DISC Backward by theta \t",theta)
    time.sleep(t)
    GPIO.output(DISC_Backward, GPIO.LOW)

def BRUSH_forward(theta):
    t=theta/BRUSH_RPM_C

    GPIO.output(BRUSH_Forward, GPIO.HIGH)
    GPIO.output(BRUSH_Backward, GPIO.LOW)

    print("Moving BRUSH Forward by theta \t",theta)
    time.sleep(t)
    GPIO.output(BRUSH_Forward, GPIO.LOW)

def BRUSH_reverse(theta):
    t=theta/BRUSH_RPM_C

    GPIO.output(BRUSH_Forward, GPIO.LOW)
    GPIO.output(BRUSH_Backward, GPIO.HIGH)

    print("Moving BRUSH Backward by theta \t",theta)
    time.sleep(t)
    GPIO.output(BRUSH_Backward, GPIO.LOW)


#####
# Time based implementations
####

DISC_F_90=0.4720
DISC_B_90=0.3778
DISC_F_180=0.76
DISC_B_180=0.755

BRUSH_F_90=0.0795
BRUSH_B_90=0.085
BRUSH_F_180=0.165
BRUSH_B_180=0.172

def DISC_forward_time(t):

    GPIO.output(DISC_Forward, GPIO.HIGH)
    GPIO.output(DISC_Backward, GPIO.LOW)

    print("Moving DISC Forward for time \t", t)
    time.sleep(t)
    GPIO.output(DISC_Forward, GPIO.LOW)


def DISC_reverse_time(t):

    GPIO.output(DISC_Backward, GPIO.HIGH)
    GPIO.output(DISC_Forward, GPIO.LOW)

    print("Moving DISC Backward for time \t", t)
    time.sleep(t)
    GPIO.output(DISC_Backward, GPIO.LOW)


def BRUSH_forward_time(t):
    #initialise()    #Done for external calls

    GPIO.output(BRUSH_Backward, GPIO.LOW)
    GPIO.output(BRUSH_Forward, GPIO.HIGH)

    print("Moving BRUSH Forward for time \t", t)
    time.sleep(t)
    GPIO.output(BRUSH_Forward, GPIO.LOW)

    #GPIO.cleanup()

def BRUSH_reverse_time(t):
    #initialise()    #Done for external calls

    GPIO.output(BRUSH_Forward, GPIO.LOW)
    GPIO.output(BRUSH_Backward, GPIO.HIGH)

    print("Moving BRUSH Backward for time \t", t)
    time.sleep(t)
    GPIO.output(BRUSH_Backward, GPIO.LOW)

    #GPIO.cleanup()

''' Assuming Brush moves faster than Disc.'''

def DISC_and_BRUSH_forward_angle(theta):
    #initialise()    #Done for external calls
    # Theta in degrees

    if theta==90:
        GPIO.output(DISC_Forward, GPIO.HIGH)
        GPIO.output(BRUSH_Forward,GPIO.HIGH)

        print("Moving BRUSH and Disc Forward for angle 90 deg \t")

        time.sleep(BRUSH_F_90)
        GPIO.output(BRUSH_Forward, GPIO.LOW)
        time.sleep(DISC_F_90-BRUSH_F_90)
        GPIO.output(DISC_Forward, GPIO.LOW)

    elif theta==180:
        GPIO.output(DISC_Forward, GPIO.HIGH)
        GPIO.output(BRUSH_Forward,GPIO.HIGH)

        print("Moving BRUSH and Disc Forward for angle 180 deg \t")

        time.sleep(BRUSH_F_180)
        GPIO.output(BRUSH_Forward, GPIO.LOW)
        time.sleep(DISC_F_180-BRUSH_F_180)
        GPIO.output(DISC_Forward, GPIO.LOW)

    #GPIO.cleanup()

def DISC_and_BRUSH_reverse_angle(theta):
    #initialise()    #Done for external calls
    # Theta in degrees

    if theta==90:
        GPIO.output(DISC_Backward, GPIO.HIGH)
        GPIO.output(BRUSH_Backward,GPIO.HIGH)

        print("Moving BRUSH and Disc Backward for angle 90 deg \t")

        time.sleep(BRUSH_B_90)
        GPIO.output(BRUSH_Backward, GPIO.LOW)
        time.sleep(DISC_B_90-BRUSH_B_90)
        GPIO.output(DISC_Backward, GPIO.LOW)

    elif theta==180:
        GPIO.output(DISC_Backward, GPIO.HIGH)
        GPIO.output(BRUSH_Backward,GPIO.HIGH)

        print("Moving BRUSH and Disc Backward for angle 180 deg \t")

        time.sleep(BRUSH_B_180)
        GPIO.output(BRUSH_Backward, GPIO.LOW)
        time.sleep(DISC_B_180-BRUSH_B_180)
        GPIO.output(DISC_Backward, GPIO.LOW)

    #GPIO.cleanup()

if __name__=='__main__':
    count=0
    #initialise()
    while (1):

        DISC_reverse_time(0.76)
        time.sleep(2)
        BRUSH_forward_time(0.0795)
        #BRUSH_forward_time(0.165)
        #BRUSH_forward_time(0.5)
        time.sleep(1)
        count+=1
        if count==1:
            break
        #DISC_reverse(6*math.pi)

        #BRUSH_forward(math.pi)
        #BRUSH_reverse(math.pi)

    GPIO.cleanup()
