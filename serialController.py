import serial
import envoy
import time
import pythonServoController
import sys
from signalData import *
from unconnected import *

#usbport = '/dev/ttyACM1'
#serFound = True
    
        
# Set up serial baud rate
#try:
#	print "In try statement"
#	print pythonServoController.serial
#	print "out try statement"
#	ser = serial.Serial(pythonServoController.serial, 9600, timeout=1)
#except:
#	print "Serial not Connected. Continuing Anyway"
#	print "pythonServoController serial is:"
#	print pythonServoController.serial
#	serFound = False

def move(servo, angle):
	if (pythonServoController.serFound):
		'''Moves the specified servo to the supplied angle.

		Arguments:
		servo
		the servo number to command, an integer from 1-4
		angle
		the desired servo angle, an integer from 0 to 180

		(e.g.) >>> servo.move(2, 90)
		... # "move servo #2 to 90 degrees"'''

		if (0 <= angle <= 180):
			pythonServoController.ser.write(chr(255))
			pythonServoController.ser.write(chr(servo))
			pythonServoController.ser.write(chr(angle))
		else:
			print("Servo angle must be an integer between 0 and 180.\n")
	else:
		print "not working.."

#takes in signalData class for input
def scan(newSignal): #scan to be used to find ideal location after being connected to the network
    running = True
    while (running): #get rid of this useless while loop?
	xpos =20 
	ypos = 0
	time.sleep(1)
	move(1,xpos)
	move(2,ypos)
	time.sleep(1)
	move(1,xpos)
	time.sleep(1)
	for ypos in xrange(0,180,4):
	    
	    move(2,ypos)
	    time.sleep(.1)
	    newSignal.getData(ypos/4)
	move(1,180)
	time.sleep(1)
	for ypos in xrange(180,0,-4):
	
	    move(2,ypos)
	    time.sleep(0.1)
	    newSignal.getData(newSignal.size2- (ypos/4))
	time.sleep(1)
	running = False

def unconnectedScan(scandata):
	xpos = 20
	ypos = 0
	time.sleep(1)
	move(1,xpos)
	move(2,ypos)
	time.sleep(1)
	move(1,xpos)
	time.sleep(1)
	for ypos in xrange(0,180,90):
		move(2,ypos)
		time.sleep(.1)
		scandata.scan()
		print "scandone"
	move(1,180)
	time.sleep(.5)
	move(0,0)
	time.sleep(.5)
	print "donemoving"
	scandata.scan()
	print "scandone"
	move(2,0)
	time.sleep(.5)
	scandata.scan()
	print "scandone"
	time.sleep(1)
#	for ypos in xrange(180,0,-90):
#		move(2,ypos)
#		time.sleep(.1)
#		scandata.scan()	
#		print "scandone"
#		time.sleep(1)
#	time.sleep(1)
