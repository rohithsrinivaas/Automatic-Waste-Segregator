#!/bin/bash

# Configured to run for Logitech C270
# prevent usb not found error by repeated re-loading
##configure here
#type your username for the variable USER if you run with sudo, otherwise bash will use root.
USER=pi
#put the path to this bash script here

bs=`lsusb | grep Logitech | cut -c5-7`
dve=`lsusb | grep Logitech | cut -c16-18`


cam() {

fswebcam  ./input/image.jpg --no-banner -D 1

}

cam

sudo /home/$USER/usbreset /dev/bus/usb/$bs/$dve
