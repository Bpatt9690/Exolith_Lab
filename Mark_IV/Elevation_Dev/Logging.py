class logger:


	def __init__(self):
		pass


	def logInfo(str,timestamp):
		print(timestamp+" INFO: "+str)
		print()
		f = open("gpsData.txt","a")
		f.write(str+"\n")
		f.close()