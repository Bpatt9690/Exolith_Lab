import RPi.GPIO as GPIO
from time import sleep
import time
import SI1145.SI1145 as SI1145
from Logging import logger
from datetime import date, datetime
import serial
import pytz
import os

azVal = None
uvUpper = None
uvLower = None

class azimuth_tracker:

	def __init__(self):
		self.sensor = SI1145.SI1145()
		self.logger = logger()


	def stepMovement(self,direction,steps):
	    GPIO.setwarnings(False) 
	    GPIO.cleanup()

	    DIR_1 = 13 #DIR+
	    STEP_1 = 26 #PULL+

	    # 0/1 used to signify clockwise or counterclockwise.
	    CW = direction

	    if direction is 1:
	        CCW = 0
	    else:
	        CCW = 1

	    MAX = 100

	    # Setup pin layout on PI
	    GPIO.setmode(GPIO.BCM)

	    # Establish Pins in software
	    GPIO.setup(DIR_1, GPIO.OUT)
	    GPIO.setup(STEP_1, GPIO.OUT)

	    # Set the first direction you want it to spin
	    GPIO.output(DIR_1, CW)

	    uv_current = self.uv_sensor()
	    self.logger.logInfo('Stationary UV value: '+str(uv_current))

	    uv_high = uv_current
	    uv_low = uv_current 

	    try:

	        for x in range(steps):
	            self.logger.logInfo('Adjusting....')
	 
	            GPIO.output(STEP_1,GPIO.HIGH)
	            #.5 == super slow
	            # .00005 == breaking
	            sleep(.05) 
	            GPIO.output(STEP_1,GPIO.LOW)
	            sleep(.05)

	            uv = self.uv_sensor()

	            if uv > uv_high:
	                uv_low = uv_high
	                uv_high = uv

	            self.logger.logUV(uv_high)
	            self.logger.logInfo('Current UV High: '+str(uv_high))

	    # Once finished clean everything up
	    except Exception as e:
	        self.logger.logInfo("Step Movement Exception: "+str(e))
	        GPIO.cleanup()


	def maxValue(self):
	    inputFile = open("uvsensor.txt","r")
	    num_list = [float(num) for num in inputFile.read().split()]

	    counter = len(num_list)
	    total = sum(num_list)

	    # Your desired values
	    max_val = max(num_list)
	    min_val = min(num_list)

	    self.logger.logInfo("Max UV Value: "+str(max_val))
	    return max_val


	def uv_sensor(self):
	    uvAverage = 0
	    for i in range(10):
	            UV = self.sensor.readUV()
	            uvIndex = UV
	            uvAverage += uvIndex
	            time.sleep(.1)
	    return (uvAverage/10)


	def azimuthPositioning(self,uvMax):

		global uvLower
		global uvUpper

	    uvUpper = uvMax + uvMax*(.10)
	    uvLower = uvMax - (uvMax*(.10))

	    self.logger.logInfo('UV Max: '+str(uvMax))
	    self.logger.logInfo('UV Upper: '+str(uvUpper))
	    self.logger.logInfo('UV Lower: '+str(uvLower))

	    self.azimuthMaxPosition(1,25,uvMax,uvUpper,uvLower)


	def azimuthMaxPosition(self,direction,steps,uvMax,uvUpper,uvLower):
	    GPIO.setwarnings(False) 
	    GPIO.cleanup()

	    DIR_1 = 13 #DIR+
	    STEP_1 = 26 #PULL+

	    # 0/1 used to signify clockwise or counterclockwise.
	    CW = direction

	    if direction is 1:
	        CCW = 0
	    else:
	        CCW = 1

	    MAX = 100

	    # Setup pin layout on PI
	    GPIO.setmode(GPIO.BCM)

	    # Establish Pins in software
	    GPIO.setup(DIR_1, GPIO.OUT)
	    GPIO.setup(STEP_1, GPIO.OUT)

	    # Set the first direction you want it to spin
	    GPIO.output(DIR_1, CW)

	    uv_current = self.uv_sensor()
	    self.logger.logInfo('Stationary UV value: '+str(uv_current))

	    self.logger.logInfo('uvLower'+str(uvLower))
	    self.logger.logInfo('uvUpper'+str(uvUpper))

	    try:

	        for x in range(steps):
	            self.logger.logInfo('Azimuth Adjustment...')
	 
	            GPIO.output(STEP_1,GPIO.HIGH)
	            #.5 == super slow
	            # .00005 == breaking
	            sleep(.05) 
	            GPIO.output(STEP_1,GPIO.LOW)
	            sleep(.05)

	            uv = self.uv_sensor()

	            self.logger.logInfo('Current UV Value:'+str(uv))
	           
	            if uvLower <= uv <= uvMax:
	            	global uvVal
	            	uvVal = uv
	                self.logger.logInfo('Stopping here')
	                self.stepMovement(0,1) #used as a brake
	                return True

            return False

	    # Once finished clean everything up
	    except Exception as e:
	        self.logger.logInfo("Exception in track: "+str(e))
	        GPIO.cleanup()


#simple tracking solution that relies on UV values being close
   	def tracking(self):
   		global uvVal
   		global uvLower
   		global uvUpper

   		uvVal = self.uv_sensor()

   		print(uvVal,uvLower,uvUpper)

   		if uvLower <= uvVal <= uvMax:
   			logger.logInfo('Azimuth adjustment reached...')
   			return True

   		else:

   			logger.logInfo('Azimuth adjustment required...')

			GPIO.setwarnings(False) 
			GPIO.cleanup()

			DIR_1 = 13 #DIR+
			STEP_1 = 26 #PULL+

			# 0/1 used to signify clockwise or counterclockwise.
			CW = 1
			CCW = 0
			steps = 10 #small increment of search
	
			# Setup pin layout on PI
			GPIO.setmode(GPIO.BCM)

			# Establish Pins in software
			GPIO.setup(DIR_1, GPIO.OUT)
			GPIO.setup(STEP_1, GPIO.OUT)

			# Set the first direction you want it to spin
			GPIO.output(DIR_1, CW)

			try:

				for x in range(steps):
					self.logger.logInfo('Adjusting....')

					GPIO.output(STEP_1,GPIO.HIGH)
					#.5 == super slow
					# .00005 == breaking
					sleep(.05) 
					GPIO.output(STEP_1,GPIO.LOW)
					sleep(.05)

					uvVal = self.uv_sensor()

					if uvLower <= uvVal <= uvUpper:
						uvUpper = uvVal + uvVal*(.10)
						uvLower = uvVal - (uvVal*(.10))
						logger.logInfo('Azimuth Adjusted')
						return True
		
				return False

			# Once finished clean everything up
			except Exception as e:
				self.logger.logInfo("Tracking Exception: "+str(e))
				GPIO.cleanup()