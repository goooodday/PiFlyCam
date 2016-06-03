# 
# Raspberry Pi Cameara CAM on the Multi-Copter
# Writer : goooodday(hkshin2@gmail.com)
# Last Update : 2015. 03. 01
# ************************************************

import picamera
import RPi.GPIO as GPIO
from time import sleep

camera = picamera.PiCamera()

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN)  # GPIO Button SW
GPIO.setup(24, GPIO.OUT) # GPIO LED

RecIDX = 0
lastCMD = 0
isCMDOK = 0
SW_On = 0

print 'Start FlyRecord~~~~~~~~~'

# Loop program 
while True:
	
	# Check Button ON	
	#------------------------------------
	if GPIO.input(23) == 0:
		SW_On += 1
	else:
		SW_On = 0


	# Switch Command
	#-------------------------------------

	# CMD Exit Program
	if SW_On >= 15000:
		break;
        
        # CMD Run & Stop
	if SW_On == 1: 		
		if lastCMD == 0:
			isCMDOK = 1
			lastCMD = 1
		else:
			isCMDOK = 1
			lastCMD = 0

	# Execute Command
	#-------------------------------------
	
	# Start Video Recording
	if lastCMD == 1 and isCMDOK == 1:
		RecIDX += 1
		GPIO.output(24, True)
		camera.start_recording(('flyvideo_%d.h264' % RecIDX))
		print ('Start Video Recording %d' % RecIDX)
		isCMDOK = 0

	elif lastCMD == 0 and isCMDOK == 1:
		GPIO.output(24, False)
		camera.stop_recording()
		print ('Stop Vide Recording %d' % RecIDX)
		isCMDOK = 0


print 'FlyRecord Stop~~~~~~~'
print ('  --- Total Video : %d' % RecIDX)
