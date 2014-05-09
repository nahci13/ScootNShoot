import envoy
import re
import string
import sys

class scanData():
	def __init__(self,interface):
		self.data = dict()
		self.averages = dict()
		self.scanNumber = 0 #keeps track of how many scans have been logged
		self.sortedAccessPoints = []
		self.interface = interface
			
	def scan(self):
		first = "sudo iwlist "
		last = " scan | egrep 'Quality|ESSID|Address'"
		r = envoy.run(first+self.interface+last)
		newstring = r.std_out
		b = string.split(r.std_out,'Cell')
		mac = ""
		ESSID = ""
		signal = ""
		success = True
		for x in b:
			success = True
			n = str(x)
			try:
				mac = re.search(r"([\dA-F]{2}(?:[-:][\dA-F]{2}){5})",n).group()
			except:	
				success = False
			try: 
				a = re.search(r'\".+?\"',n).group()
				ESSID = a.replace("\"","")
			except:
				success = False
			try:
				signal = re.search(r'[0-9]{1,3} dBm',n).group()
				signal = signal.replace("dBm","")
				signal = signal.replace(" ", "")
				signal = int(signal)
			except:
				success = False
			if (success): #adds info to the dictionary if a mac address, ESSID, and signal were successfully found
				if mac in self.data:
					self.data[mac][1].append(signal)
				else:
					self.data[mac] = []
					self.data[mac].append([ESSID])
					self.data[mac].append([signal])
					#print "here"+str(self.data[mac])
		self.scanNumber += 1

	def printData(self):
		#print self.data
		for x in self.data:
			print x+str(self.data[x])

	def printAverages(self):
		for x in self.averages:
			print x+str(self.averages[x])


	def averagedData(self):
		total = 0
		for x in self.data:
			#print self.data[x]
			print self.data[x][1]
			for y in self.data[x][1]:
				total += y
			total += (100*(self.scanNumber-len(self.data[x][1]))) #add in bad data for every scan that a signal was not found so that the average isn't artificially inflated
			self.averages[x] = [self.data[x][0], total/self.scanNumber]
			total = 0

	def sortConnections(self):
		APs = []
		count = 0
		for x in self.data:
			APs+=[[x,self.averages[x][0][0],self.averages[x][1]]]
			count += 1
		self.sortedAccessPoints = sorted(APs,key=getKey)
		print "sorted access points:"
		for x in self.sortedAccessPoints:
			print x
	

def getKey(item):  #needed for the sorting function 
	return item[2]

def main():
	a = scanData()
	for x in range(10):
		a.scan()
	a.printData()
	print "number of scans performed "+str(a.scanNumber)
	a.averagedData()
	a.printAverages()

if __name__ == '__main__':
	main()
