#!/usr/bin/env python

import serial
import time
import envoy
import sys
from signalData import *
from unconnected import *
import serialController

serialString = ""
interface =""
exit = True
serFound = True
try:
	ser = serial.Serial(sys.argv[1],9600,timeout=1)
except:
	print "failed to aquire serial!"
	serFound = False

def main():
	#First parse arugments
	interface=""
	exit = True
	if (len(sys.argv)==3):
		serial = str(sys.argv[1])
		interface = str(sys.argv[2])
		exit = False
	elif (len(sys.argv)==2):
		if sys.argv[1] == str(1):
			serial = "/dev/ttyACM0"
			interface = "wlan2"
			exit = False
		elif sys.argv[1] == str(2):
			serial = "/dev/ttyACM1"
			interface = "wlan4"
			exit = False
		else:
			print "Improper arguments. Try again"
			return
	else:
		print "Wrong number of args. Try again."
		return
	print serial
	print interface
	return serial,interface,exit

def main2():
	print "in main2"
	print serial
	print interface
	unconnectedSignal = scanData(interface)
	serialController.unconnectedScan(unconnectedSignal)
	unconnectedSignal.averagedData()
	unconnectedSignal.printAverages()
	unconnectedSignal.sortConnections()
	
	signal = signalData(5,90,interface)
	serialController.scan(signal)
	#serialController.pause()
	signal.averager()
	print "regular averages:"
	print signal.average
	signal.movingAverage()
	print "signal.movedAverage:"
	print signal.movedAverage
	o = signal.findBestMoved()
	print "o (location) best serialController.moved:"
	print o
	if (o < 45):
		serialController.move(1,20)
		time.sleep(2)
		serialController.move(2,4*o)
	else:
		serialController.move(1,180)
		time.sleep(2)
		serialController.move(2,180-(4*(o-45)))

	#time.sleep(1)

	#o = signal.findBest()
	#print "o orignal version"
	#print o
	#if (o < 45):
	#	serialController.move(1,20)
	#	time.sleep(2)
	#	serialController.move(2,4*o)
	#else:
	#	serialController.move(1,180)
	#	time.sleep(2)
	#	serialController.move(2,180-(4*(o-45)))
	print "done"
		    
if __name__  == '__main__':
	data = main()
	exit = data[2]
	if (exit==False):
		serialString = data[0]
		interface = data[1] 
		print "after main"
		print serialString
		print interface
		main2()
	    
		

