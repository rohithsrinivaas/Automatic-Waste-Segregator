'''
Distributed computing based model for low power RISC device.
'''

# SSH for prediction
import resize
import subprocess
import time
import os
import shutil
import constants
import masking

RPI_IP,MAC_IP=constants.read_IP()

PORT='Ankivarun@'+MAC_IP+':~/Documents/Academics/IIT\ M/Projects/Smart\ DB/mac_interface/ssh_input/'
PASSWORD='1207'
PORT_OP='~/Documents/Academics/IIT\ M/Projects/Smart\ DB/mac_interface/ssh_output/'

def predict_ssh(test=None,image=None):
    # outputs [glass,metal,plastic,organic] confidence

    #image must be of form ./input/foo.jpg
    if not test:
        #image_masked=masking.background_subtract()
        image_resized=resize.rpi_resize()

    #Send over image
    subprocess.call(['sshpass','-p','1207','rsync','./input_resized/resized_input.jpg',PORT])


    while True:
        if os.path.isfile('./ssh_output/ssh_output.txt'):
            time.sleep(0.1)
            break
        else:
            time.sleep(0.01)
            continue

    with open('./ssh_output/ssh_output.txt') as file:
        vision_features=file.readlines()

    for i in range(len(vision_features)):
        vision_features[i]=float(vision_features[i])

    print "Vision Features in [glass,metal,organic,plastic]", vision_features,"\n"

    # ARGMAX Procedure

    arg_max=max(vision_features)
    for i in range(len(vision_features)):
        if vision_features[i]==arg_max:
            vision_features[i]=1
        else:
            vision_features[i]=0

    return vision_features

if __name__=='__main__':
    s1=time.clock()
    predict_ssh()
    s2=time.clock()

    print s2-s1
