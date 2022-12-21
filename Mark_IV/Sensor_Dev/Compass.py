from i2clibraries import i2c_hmc5883l
from time import sleep
 
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)

while(1):
 
	hmc5883l.setContinuousMode()
	hmc5883l.setDeclination(-10, 24)
	compassReading = hmc5883l.getHeadingString()
	#newReading = (int(compassReading[0:3])+25)
	#print("Raw Reading: ",compassReading[0:3])	 
	print(hmc5883l.getHeadingString())
	#print("Adjusted Reading: ",newReading)

	sleep(.5)