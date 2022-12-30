import os 
import time
from datetime import date, datetime
import pytz

class logger:

	def __init__(self):
		pass

	def logUV(self,data):
		timestamp = self.timestamp()
		print(timestamp +" INFO: "+str(data))
		print()
		f = open("uvsensor.txt","a")
		f.write(str(data)+"\n")
		f.close()

	def logInfo(self,data):
		timestamp = self.timestamp()
		print(timestamp+" INFO: "+str(data))
		print()
		f = open(str(timestamp)+".txt","a")
		f.write(str(data)+"\n")
		f.close()

	def timeStamp():
	    tz_NY = pytz.timezone('America/New_York') 
	    datetime_NY = datetime.now(tz_NY)
	    return str(datetime_NY.strftime("%H:%M:%S"))