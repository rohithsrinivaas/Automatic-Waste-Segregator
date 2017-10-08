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
import predict_ssh
import datetime
import move_to_bin
import constants

DISTANCE_THRESHOLD=38
#Ultrasound Distance threshold # in cm


def check_for_object():

    distance=ultrasonic_1.measure()
    print "Ultrasound check ... \n"

    while (distance>DISTANCE_THRESHOLD):
        time.sleep(1)
        distance=ultrasonic_1.measure()
        print "Ultrasound check ... \n"
        #Sleep for 1 second

def take_picture():
    print "Taking pricture ... \n"
    subprocess.call(['bash','camera.sh'])

def main():
    print "Starting AWS cycle ... \n"
    print "Starting run-timer ... \n"
    s1=time.clock()                      # Timer 1
    check_for_object()

    print "Settling camera before shot ... \n"
    time.sleep(2)
    take_picture()

    print "\n\n Starting predictor ... \n"
    score=predict_ssh.predict_ssh()
    print "Scores sucessfully got ... \n"
    print "Moving to bin \t",score," ..."
    print "Reference [glass metal organic plastic] \n"
    move_to_bin.mover(score)
                       # Timer 2

    stamp=datetime.datetime.now()
    stamp_path='./logs/'+str(stamp)
    #cleanup
    print "Cleanup and Saving Logs ... \n"
    subprocess.call(['mkdir',stamp_path])
    subprocess.call(['mv','./input/image.jpg',stamp_path])                      # Original image
    #subprocess.call(['mv','./input_masked/input_masked.jpg',stamp_path])                      # Masked image
    subprocess.call(['mv','./input_resized/resized_input.jpg',stamp_path])      #Resized logs

    subprocess.call(['mv','./ssh_output/ssh_output.txt',stamp_path])        # Vision confidence

    time.sleep(3)           #Steadying time
    print "Killing of transients ...\n"
    s2=time.clock()
    print "\n Total Run time \t", s2-s1

    print "#################################"

if __name__=='__main__':

    #Backup logs
    print "################################# \n \n"
    print "\t \t Welcome to AWS-One. \n Booting Up ... \n "

    #constants.IP_initialise()

    RPI_IP,MAC_IP=constants.read_IP()
    #### CONSTANTS #####
    PORT_LOGS='Ankivarun@'+MAC_IP+':~/Documents/Academics/IIT\ M/Projects/Smart\ DB/mac_interface/logs/'
    # Send logs via rsync
    PORT_CONSTANTS='Ankivarun@'+MAC_IP+':~/Documents/Academics/IIT\ M/Projects/Smart\ DB/mac_interface/'


    print "Syncing Logs ... \n"
    subprocess.call(['sshpass','-p','1207','rsync','-a','./logs/',PORT_LOGS])
    print "Detection Active ... \n"
    while True:
        main()
