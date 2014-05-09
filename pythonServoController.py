#!/usr/bin/env python

import serial
import time
import envoy
import sys
from signalData import *
from unconnected import *


serFound = False

def main():

	print serial
	print interface
	unconnectedSignal = scanData("eth1")
	#unconnectedScan(unconnectedSignal)
	for x in range(30):
		unconnectedSignal.scan()
	unconnectedSignal.averagedData()
	unconnectedSignal.printAverages()
	unconnectedSignal.sortConnections()
	
	signal = signalData(5,90,interface)
	scan(signal)
	#serialController.pause()
	signal.averager()
	print "regular x averages:"
	print signal.average
	signal.movingAverage()
	print "signal.movedAverage:"
	print signal.movedAverage
	o = signal.findBestMoved()
	print "o (location) best serialController.moved:"
	print o
	if (o < 45):
		move(1,20)
		time.sleep(2)
		move(2,4*o)
	else:
		move(1,180)
		time.sleep(2)
		move(2,180-(4*(o-45)))

	print "Now scanning in the y direction"
	time.sleep(1)
	#Now start scanning in the Y direction
	signalY = signalData(5,90,interface)
        yscan(signalY,o)
	signalY.averager()
	print "regular y averages:"
	print signalY.average
	signalY.movingAverage()
	print "signalY.movedAverage:"
	print signalY.movedAverage
	value = signalY.findBestMoved()
	print "value (location) best serialController.moved:"
	print value
	
        move(1,value)

	print "done"
		    




#used to be in serialCotroller:


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

#scan the y direction after x has been found
def yscan(newSignal, o): #the way it scans depends on the orientation of the servo
	time.sleep(1)
	if o<45:
		for xpos in xrange(0,90,1):
			move(1,xpos)
			time.sleep(.1)
			newSignal.getData(xpos)
		time.sleep(1)
	else:
		for xpos in xrange(89,-1,-1):
			move(1,xpos)
			time.sleep(.1)
			newSignal.getData(89-xpos)
		time.sleep(1)

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

if __name__  == '__main__':
	interface =""
	serFound = False
	#First parse arugments
	if (len(sys.argv)==3):
		serialString = str(sys.argv[1])
		interface = str(sys.argv[2])
		
	elif (len(sys.argv)==2):
		if sys.argv[1] == str(1):
			serialString = "/dev/ttyACM0"
			interface = "wlan2"
		elif sys.argv[1] == str(2):
			serialString = "/dev/ttyACM1"
			interface = "wlan4"
		elif sys.argv[1] == str(3):
			serialString = "/dev/ttyACM0"
			interface = "wlan4"
		elif sys.argv[1] == str(4):
			serialString = "/dev/ttyACM1"
			interface = "wlan2"
		else:
			print "Improper arguments. Try again"
	else:
		print "Wrong number of args. Try again."

	print "serialString is "+serialString
	try:
		ser = serial.Serial(serialString,9600,timeout=1)
		serFound = True
	except:
		print "failed to aquire serial!"
	if (serFound):
		main()
