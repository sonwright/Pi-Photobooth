#Written by Mari DeGrazia 
#arizona4n6@gmail.com
#This script will monitor a button on GPIO 13
#When pressed it will kill the photobooth python script

import RPi.GPIO as GPIO
import time
import subprocess
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
while True:
    input_state = GPIO.input(13)
    if input_state == False:
       time.sleep(0.3) 
       cmd = "sudo pkill -f photobooth.py"
       k = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       message =  k.communicate(input)
       print message[0]
       
       
       cmd = "sudo pkill -f photobooth_wii.py"
       k = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
       message =  k.communicate(input)
       print message[0]

