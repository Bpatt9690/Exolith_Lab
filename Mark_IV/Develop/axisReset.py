from Logging import logger
import RPi.GPIO as GPIO
import time
from time import sleep
from datetime import date, datetime
import serial
from Limit_Switches import limitSwitches

class axis_reset:

    def __init__(self):
        pass

    #Responsible for resetting the elevation axis.
	#Retracts elevation boom until limit switch is triggered
    def elevation_reset(self):

    	logger.logInfo(self.timeStamp(),'Resetting Elevation')

	    #setup limit switch
	    GPIO.setmode(GPIO.BCM)
	    switch=17
	    GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

	    # Direction pin from controller
	    AZ_DIR = 25
	    # Step pin from controller
	    AZ_STEP = 24

	    # 0/1 used to signify clockwise or counterclockwise.
	    CW = 0
	    CCW = 1

	    # Setup pin layout on RPI
	    GPIO.setmode(GPIO.BCM)
	    GPIO.setup(AZ_DIR, GPIO.OUT)
	    GPIO.setup(AZ_STEP, GPIO.OUT)
	    GPIO.output(AZ_DIR, CW)

	    while(1):

	        for x in range(200):
	            GPIO.output(AZ_STEP,GPIO.HIGH)
	            # Dictates how fast stepper motor will run
	            sleep(.05)
	            GPIO.output(AZ_STEP,GPIO.LOW)

	            if GPIO.input(switch) == 0:
	                print('Elevation Reset')
	                GPIO.cleanup()
	                sleep(1)
	                return True

    	sleep(.5)


    def x_axis_reset():

    	ls = limitSwitches()

	    GPIO.cleanup()

	    DIR_1 = 6 #DIR+
	    STEP_1 = 5 #PULL+

	    # 0/1 used to signify clockwise or counterclockwise.
	    CW = 0
	    CCW = 1

	    MAX = 10000

	    motor1_flag = 0
	    motor2_flag = 0

	    GPIO.setmode(GPIO.BCM)
	    motor1_switch=27
	    motor2_switch=21

	    GPIO.setup(motor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
	    GPIO.setup(motor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

	    # Establish Pins in software
	    GPIO.setup(DIR_1, GPIO.OUT)
	    GPIO.setup(STEP_1, GPIO.OUT)

	    # Set the first direction
	    GPIO.output(DIR_1, CCW)

	    try:
	        while(1):

	            for x in range(MAX):

	                GPIO.output(STEP_1,GPIO.HIGH)
	                #.5 == super slow
	                # .00005 == breaking
	                sleep(.005) # Dictates how fast stepper motor will run
	                GPIO.output(STEP_1,GPIO.LOW)
	                sleep(.005)
	       
	                if GPIO.input(motor2_switch) == 0:
	                    motor2_flag += 1
	                elif GPIO.input(motor1_switch) == 0:
	                    motor1_flag +=1
	                else:
	                    motor2_flag = 0
	                    motor1_flag = 0

	                if motor2_flag >= 5:
	                    print('X Homing Complete')
	                    sleep(1)
	                    return True

	                elif motor1_flag >= 5:
	                    print('X Homing Complete')
	                    sleep(1)
	                    return True
	                                  
	    # Once finished clean everything up
	    except Exception as e:
	        print("cleanup")
	        GPIO.cleanup()
	    	return False


    def y_axis_reset():

    	ls = limitSwitches()

    	GPIO.cleanup()

	    DIR_1 = 19 #DIR+
	    STEP_1 = 20 #PULL+

	    # 0/1 used to signify clockwise or counterclockwise.
	    CW = 0
	    CCW = 1

	    MAX = 10000

	    motor1_flag = 0
	    motor2_flag = 0

	    GPIO.setmode(GPIO.BCM)
	    motor1_switch=18
	    motor2_switch=12
	    GPIO.setup(motor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
	    GPIO.setup(motor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)


	    # Establish Pins in software
	    GPIO.setup(DIR_1, GPIO.OUT)
	    GPIO.setup(STEP_1, GPIO.OUT)

	    # Set the first direction
	    GPIO.output(DIR_1, CCW)

	    try:

	        while(1):

	            for x in range(MAX):

	                GPIO.output(STEP_1,GPIO.HIGH)
	                # Allow it to get there.
	                #.5 == super slow
	                sleep(.005) # Dictates how fast stepper motor will run
	                GPIO.output(STEP_1,GPIO.LOW)

	                sleep(.005) 

	                if GPIO.input(motor2_switch) == 0:
	                    motor2_flag += 1
	                elif GPIO.input(motor1_switch) == 0:
	                    motor1_flag +=1
	                else:
	                    motor2_flag = 0
	                    motor1_flag = 0

	                if motor2_flag >= 5:
	                    print('Y Homing Complete')
	                    sleep(1)
	                    return True

	                elif motor1_flag >= 5:
	                    print('Y Homing Complete')
	                    sleep(1)
	                    return True
	                        
	    # Once finished clean everything up
	    except Exception as e:
	        print("cleanup")
	        GPIO.cleanup()
	    	return False


    #Current timeStamps in EST; Configurable
	def timeStamp():
	    tz_NY = pytz.timezone('America/New_York') 
	    datetime_NY = datetime.now(tz_NY)
	    return str(datetime_NY.strftime("%H:%M:%S"))
