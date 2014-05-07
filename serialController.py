import serial
import envoy
import time
import pythonServoController
from signalData import *
from unconnected import *

usbport = '/dev/ttyACM0'
#usbport = '/dev/ttyACM1'
serFound = True
    
        
# Set up serial baud rate
try:
	ser = serial.Serial(usbport, 9600, timeout=1)
except:
	print "Serial not Connected. Continuing Anyway"
	serFound = False

def move(servo, angle):
	if (serFound):
		'''Moves the specified servo to the supplied angle.

		Arguments:
		servo
		the servo number to command, an integer from 1-4
		angle
		the desired servo angle, an integer from 0 to 180

		(e.g.) >>> servo.move(2, 90)
		... # "move servo #2 to 90 degrees"'''

		if (0 <= angle <= 180):
			ser.write(chr(255))
			ser.write(chr(servo))
			ser.write(chr(angle))
		else:
			print("Servo angle must be an integer between 0 and 180.\n")
	else:
		print "not working.."

def pause(): #sends arbitrary data for the arduino to read to make it reset
	move(6,50)

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
        move(1,xpos)
        move(2,ypos)
	time.sleep(1)
	move(1,xpos)
	time.sleep(1)
	for ypos in xrange(0,180,90):
		move(2,ypos)
		time.sleep(.1)
		scandata.scan()
	move(1,180)
	time.sleep(1)
	for ypos in xrange(180,0,-90):
		move(2,ypos)
		time.sleep(.1)
		scandata.scan()	
	time.sleep(1)
