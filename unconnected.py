import envoy
import re
import string

class scanData():
	def __init__(self):
		self.data = dict()
			
	def scan(self):
		r = envoy.run("sudo iwlist eth1 scan | egrep 'Quality|ESSID|Address'")
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

	def printData(self):
		#print self.data
		for x in self.data:
			print x+str(self.data[x])

a = scanData()
for x in range(5):
	a.scan()
a.printData()
