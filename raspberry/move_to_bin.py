'''
Move to respective bins.
Given one hot vector (dim=4)
'''
# outputs [glass,metal,plastic,organic] confidence

import motor_control
import math
import time
import RPi.GPIO as GPIO

# CONSTANTS

#motor_control.initialise()

DISC_F_90=0.44
DISC_B_90=0.460
DISC_F_180=0.685
DISC_B_180=0.65

BRUSH_F_90=0.1425
BRUSH_B_90=0.1425
BRUSH_F_180=0.2
BRUSH_B_180=0.235

def mover(score):
     # If any before

    DISC_Forward=27
    DISC_Backward=17
    DISC_PWM_PIN=22
    DISC_RPM=100.00
    DISC_RPM_C=(DISC_RPM/60)*2*math.pi

    BRUSH_Forward=6
    BRUSH_Backward=5
    BRUSH_PWM_PIN=13
    BRUSH_RPM=200.00*7/12
    BRUSH_RPM_C=(BRUSH_RPM/60)*2*math.pi

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
    BRUSH_PWM.start(53.5)

    if score[0]:
        # Compartment 4, glass
        motor_control.DISC_and_BRUSH_reverse_angle(90)
        time.sleep(0.5)
        motor_control.BRUSH_forward_time(BRUSH_F_90)
        time.sleep(0.5)
        motor_control.BRUSH_reverse_time(BRUSH_B_90)
        time.sleep(0.5)
        motor_control.DISC_and_BRUSH_forward_angle(90)

    elif score[1]:
        # Compartment 3 ,metal
        motor_control.DISC_and_BRUSH_forward_angle(180)
        time.sleep(0.5)
        motor_control.BRUSH_forward_time(BRUSH_F_90)
        time.sleep(0.5)
        motor_control.BRUSH_reverse_time(BRUSH_B_90)
        time.sleep(0.5)
        motor_control.DISC_and_BRUSH_reverse_angle(180)

    elif score[2]:
        # Compartment 2, organic

        motor_control.DISC_and_BRUSH_forward_angle(90)
        time.sleep(1)
        motor_control.BRUSH_forward_time(BRUSH_F_90)
        time.sleep(1)
        motor_control.BRUSH_reverse_time(BRUSH_B_90)
        time.sleep(1)
        motor_control.DISC_and_BRUSH_reverse_angle(90)

    elif score[3]:
        # Compartment 1 , plastic
        motor_control.BRUSH_forward_time(BRUSH_F_90)
        time.sleep(0.5)
        motor_control.BRUSH_reverse_time(BRUSH_B_90/1.5)

if __name__=='__main__':
    mover([0,0,1,0])
