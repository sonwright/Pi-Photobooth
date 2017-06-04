#Written by Mari DeGrazia 
#arizona4n6@gmail.com
#This script will synch with the Wii remote and monitor the buttons
#Once a button is pressed, it will write out to a specified GPIO pin
#The photobooth script monitors the corresponding GPIO pins and once the GPIO state changes acts accordingly

import cwiid
import time
import pygame
import RPi.GPIO as GPIO

#these will be the GPIO pins that the photobooth will monitor for changes
GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT) #right, next overlay
GPIO.setup(9, GPIO.OUT) #1 button, print picture
GPIO.setup(21, GPIO.OUT) #left, previous overlay
GPIO.setup(20, GPIO.OUT) #2 button, new picture
GPIO.setup(16, GPIO.OUT) #A button, remove overlays
pygame.mixer.init()

pygame.mixer.music.load("/home/pi/Pi-Photobooth/audio/mk64_luigi03.wav")
pygame.mixer.music.play()

print 'Press button 1 + 2 on your Wii Remote...'
time.sleep(1)

wm = None
while not wm:
	try:
		wm=cwiid.Wiimote()
	except:
		print "Still looking for Wii remote..."
		pass

print 'Wii Remote connected...'
pygame.mixer.music.load("/home/pi/Pi-Photobooth/audio/mk64_mario09.wav")
pygame.mixer.music.play()
wm.rumble=True
time.sleep(1)
wm.rumble= False

Rumble = False
wm.rpt_mode = cwiid.RPT_BTN

while True:
	print  wm.state['buttons']
	direction = wm.state['buttons']
	
	# 1 button pressed
	if direction == 1:
		print "picture"
		GPIO.output(9, GPIO.LOW)
		time.sleep(.3)
		GPIO.output(9, GPIO.HIGH)

	# 2 button 
	if direction == 2:
		print "new picture"
		GPIO.output(20, GPIO.LOW)
		time.sleep(.3)
		GPIO.output(20, GPIO.HIGH)

    # A button 
	if direction == 8:
		print "remove overlays"
		GPIO.output(16, GPIO.LOW)
		time.sleep(.3)
		GPIO.output(16, GPIO.HIGH)
		
	#to make it turn, make one wheel move slower then the other	
	if direction == 1024:
		print "next overlay"
		GPIO.output(17, GPIO.LOW)
		time.sleep(.3)
		GPIO.output(17, GPIO.HIGH)

	if direction == 2048:
		print "previous overlay"
		GPIO.output(21, GPIO.LOW)
		time.sleep(.3)
		GPIO.output(21, GPIO.HIGH)