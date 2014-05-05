#!/usr/bin/env python

import serial
import time
import envoy
from signalData import *
import serialController

def main():
	signal = signalData(5,90)
	serialController.scan(signal)
	serialController.pause()
	signal.averager()
	print "regular averages:"
	print signal.average
	signal.movingAverage()
	print "signal.serialController.movedAverage:"
	print signal.serialController.movedAverage
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

	time.sleep(1)
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
	main()		
	    
		
	    

