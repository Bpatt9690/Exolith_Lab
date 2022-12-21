from i2clibraries import i2c_hmc5883l
from time import sleep
 
class Compassdata:

	def __init__(self):
		pass

	def getGPSData():

		hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)

		while(1):
		 
			hmc5883l.setContinuousMode()
			hmc5883l.setDeclination(-10, 4)
				 
			print(hmc5883l.getHeadingString())

			sleep(.5)