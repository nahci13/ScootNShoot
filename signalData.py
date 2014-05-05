import serial
import time
import envoy

class signalData:
	def __init__(self,size1,size2): # i.e signalData(20,90)
		self.size1 = size1
		self.size2 = size2
		self.data=[[0 for x in xrange(size1)] for x in xrange(size2)]
		self.average=[0 for x in xrange(size2)]        
		self.movedAverage=[0 for x in xrange(size2)]
		self.movingWindowSize = 5  #keep this odd!

	def getData(self,location):
		for i in range(0,self.size1):
			self.data[location][i] = getSignal()

	def averager(self):
		for i in range(0,self.size2):
			total = 0
			for j in range(0,self.size1):
				total+=self.data[i][j]
			self.average[i] = total/self.size1

	def printAverages(self):
		print self.average

	def findBest(self): #returns the servo location where the average signal was the best
		bestSignal = 1000 #impossibly bad signal strength
		location = 0
		for i in xrange(0,self.size2):
			if (self.average[i] < bestSignal):
				bestSignal = self.average[i]
				location = i
		return location	

	def findBestMoved(self): #returns the servo location where the average signal was the best
		bestSignal = 1000 #impossibly bad signal strength
		location = 0
		bestArray = []
		bests = []
		for i in xrange(0,self.size2):
			if (self.movedAverage[i] < bestSignal):
				bestSignal = self.movedAverage[i]
				bestArray = [] #reset the array of bestsignals because a better was found
			        bests = []
				bests.append(i)
			elif (self.movedAverage[i] > bestSignal):
				if len(bests) > 0:
					bestArray+=[bests]
					bests = []	
			elif (self.movedAverage[i] == bestSignal):	
				bests.append(i)
		largestLength = 0
		bestArrayArray = [] 
		print "BestArray:"
		print bestArray
		for array in bestArray:
			if len(array) > largestLength:
				largestLength = len(array)
				bestArrayArray = array
		return bestArrayArray[largestLength/2]

	def movingAverage(self):
		a = []
		b = []
		c = []
		d = []
		for x in range(self.size2-(self.movingWindowSize/2),self.size2):
			a+=[x]
		for x in range(0,self.size2):
			b+=[x]
		for x in range(0,self.size2+(self.movingWindowSize/2)):
			c+=[x]
		d = a+b+c
		index = 0
		for i in range(0,self.size2):
			total = 0
			for j in range(0,self.movingWindowSize):
				total+=self.average[d[j+index]]
			self.movedAverage[i] = total/self.movingWindowSize
			index +=1


def getSignal():
	r = envoy.run("iwconfig wlan2 | grep -Eo '(-[0-9]{1,3})'")
	newstring = r.std_out.replace("-","")
	try:
		i = int(newstring)
	except:
		print newstring
		return 100 #fix this value. maybe try recalling getSignal
	return i



