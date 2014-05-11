#!/usr/bin/env python

import serial
import time
import io
import envoy
import sys
from signalData import *
from unconnected import *
import subprocess

serFound = False
f1 = open("antennaData1","w")
f2 = open("antennaData2","w")

def main():

	print serial
	print interface
	unconnectedSignal = scanData("eth1")
	#unconnectedScan(unconnectedSignal)
	for x in range(30):
		unconnectedSignal.scan()
	print "Data before being averaged"
	unconnectedSignal.averagedData()
	unconnectedSignal.sortConnections()
	unconnectedSignal.getDuplicates()
	bssids = unconnectedSignal.bestSignals("UDel")
	if len(bssids) == 2:
		subprocess.call("nmcli "+"c "+"up "+"iface " +"wlan2"+" id "+"UDel\ 2 "+"ap "+bssids[0],shell = True)
		subprocess.call("nmcli "+"c "+"up "+"iface " +"wlan4"+" id "+"UDel\ 1 "+"ap "+bssids[1],shell = True)
		f1.write("UDel "+bssids[0])
		f2.write("UDel "+bssids[1])
	else:	
		print "finding best UD signals failed"
	time.sleep(3)  #definitely can probably adjust this
		    
#used to be in serialController:


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
		for xpos in range(0,90,2):
			move(1,xpos)
			time.sleep(.1)
			newSignal.getData(xpos/2)
		time.sleep(1)
	else:
		for xpos in range(178,88,-2):
			move(1,xpos)
			time.sleep(.1)
			newSignal.getData((178-xpos)/2)
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
			serial2 = "/dev/ttyACM1"
			interface2 = "wlan4"
		elif sys.argv[1] == str(2):
			serialString = "/dev/ttyACM1"
			interface = "wlan4"
			serial2 = "/dev/ttyACM0"
			interface2 = "wlan2"
		elif sys.argv[1] == str(3):
			serialString = "/dev/ttyACM0"
			interface = "wlan4"
			serial2 = "/dev/ttyACM1"
			interface2 = "wlan2"
		elif sys.argv[1] == str(4):
			serialString = "/dev/ttyACM1"
			interface = "wlan2"
			serial2 = "/dev/ttyACM0"
			interface2 = "wlan4"
		elif sys.argv[1] == str(9): #debug case
			serialString = "/dev/ttyACM0"
			interface = "eth1"
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
                ser.close()
                subprocess.call(['gnome-terminal', '-x', 'python', 'redirect.py',serialString,interface,'1'])
                subprocess.call(['gnome-terminal', '-x', 'python', 'redirect.py',serial2,interface2,'2'])

#       filename = 'test1.log'
#       with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
#           process = subprocess.Popen(["python", 'sweep.py',serialString,interface], stdout=writer)
#           while process.poll() is None:
#               f1.write(reader.read())
#               time.sleep(0.5)
#           # Read the remaining
#           f1.write(reader.read())
#
#       filename2 = 'test2.log'
#       with io.open(filename2, 'wb') as writer, io.open(filename2, 'rb', 1) as reader:
#           process = subprocess.Popen(["python", 'sweep.py',serial2,interface2], stdout=writer)
#           while process.poll() is None:
#               f2.write(reader.read())
#               time.sleep(0.5)
#           # Read the remaining
#           f2.write(reader.read())
	
