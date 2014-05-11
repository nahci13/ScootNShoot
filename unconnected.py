import envoy
import re
import string
import sys

class scanData():
	def __init__(self,interface):
		self.data = dict()
		self.averages = dict()
		self.pairs = dict()
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


	def averagedData(self): #averages the signal strength of each AP depending on how many scans were performed
		total = 0
		for x in self.data:
			print self.data[x]
			#print self.data[x][1]
			for y in self.data[x][1]:
				total += y
			total += (100*(self.scanNumber-len(self.data[x][1]))) #add in bad data for every scan that a signal was not found so that the average isn't artificially inflated
			self.averages[x] = [self.data[x][0], total/self.scanNumber]
			total = 0

	def sortConnections(self): #sorts all found access points by average signal strength
		APs = []
		count = 0
		for x in self.data:
			APs+=[[x,self.averages[x][0][0],self.averages[x][1]]]
			count += 1
		self.sortedAccessPoints = sorted(APs,key=getKey)
		print "sorted access points:"
		for x in self.sortedAccessPoints:
			print x
	
	def getDuplicates(self): #groups access points with the same SSID
		findPairs = dict()
		for x in self.averages:
			#print self.averages[x][0][0]
			ssid = self.averages[x][0][0]
			if ssid in findPairs:
				#print "x already here" + str(x)
				#print findPairs[ssid]
				findPairs[ssid][0].append(str(x))
				findPairs[ssid][1].append(self.averages[x][1])
			else:
				findPairs[self.averages[x][0][0]]=[[x],[self.averages[x][1]]]
				
		for x in findPairs:
			print str(x) + " " +str(findPairs[x])
			if len(findPairs[x][0])>1:
				self.pairs[x]=findPairs[x]

		print "pairs"
		for x in self.pairs:
			print str(x) + " " + str(self.pairs[x])

	#def getBestPair(self):
		#for x in self.pairs

	def bestUD(self): #returns an array with the mac addresses of the two UD access points with with the best signal
		result = []
		value1=100
		value2=100
		best1=0
		best2=0
		a=[]
		if ("UDel" in self.pairs):
			a = self.pairs["UDel"]
			print "yes, its there"	
			db = a[1]
			index = 0
			for x in db:
				if x < value1:
					best2=best1 #pass previous best down
					value2=value1
					value1=x
				        best1=index
				elif x<value2:
					value2=x
					best2=index
				index+=1	
			result.append(a[0][best1])
			result.append(a[0][best2])
		return result

def getKey(item):  #needed for the sorting function 
	return item[2]

#antenna should probably be either 1 or 2
def connect(interface,BSSID,antenna):
	call("nmcli "+"c "+"up "+"iface " +interface+" id "+"UDel\ "+antenna+" "+"ap "+BSSID,shell = True)
	return

def main():
	a = scanData(sys.argv[1])
	for x in range(5):
		a.scan()
	a.printData()
	print "number of scans performed "+str(a.scanNumber)
	a.averagedData()
	a.printAverages()
	a.sortConnections()
	#print "duplicates"
	#print a.pairs
	a.getDuplicates()
	macs= a.bestUD()
	print macs

if __name__ == '__main__':
	main()
