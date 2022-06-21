import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
#DIR_1 = 17
AZ_DIR = 25
# Step pin from controller

AZ_STEP = 24
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

# Establish Pins in software
GPIO.setup(AZ_DIR, GPIO.OUT)
GPIO.setup(AZ_STEP, GPIO.OUT)

# Set the first direction you want it to spin
GPIO.output(AZ_DIR, CW)
try:
	# Run forever.
	#while True:

	sleep(1.0)
	# Esablish the direction you want to go
	GPIO.output(AZ_DIR,CW)

	GPIO.output(AZ_STEP,GPIO.HIGH)

	# Allow it to get there.
	sleep(.0001) # Dictates how fast stepper motor will run
	# Set coil winding to low
	GPIO.output(AZ_STEP,GPIO.LOW)
	
	sleep(.5)



	GPIO.output(AZ_DIR, CCW)
	GPIO.output(AZ_STEP,GPIO.HIGH)

	# Allow it to get there.
	sleep(.00001) # Dictates how fast stepper motor will run
	# Set coil winding to low
	GPIO.output(AZ_STEP,GPIO.LOW)
	 # Dictates how fast stepper motor will run
	GPIO.cleanup()

	#	"""Change Direction: Changing direction requires time to switch. The
	#	time is dictated by the stepper motor and controller. """
	#	sleep(1.0)
	#	GPIO.output(DIR,CCW)
	#	for x in range(200):
	#		GPIO.output(STEP,GPIO.HIGH)
	#		sleep(.005)
	#		GPIO.output(STEP,GPIO.LOW)
	#		sleep(.005)

# Once finished clean everything up
except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()