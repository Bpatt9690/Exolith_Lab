import RPi.GPIO as GPIO
from time import sleep

# Direction pin from controller
DIR_1 = 17
DIR_2 = 23
# Step pin from controller
STEP_1 = 18
STEP_2 = 22
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Setup pin layout on PI
GPIO.setmode(GPIO.BCM)

# Establish Pins in software
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)
GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)

# Set the first direction you want it to spin
GPIO.output(DIR_1, CW)
GPIO.output(DIR_2, CW)
try:
	# Run forever.
	while True:

		"""Change Direction: Changing direction requires time to switch. The
		time is dictated by the stepper motor and controller. """
		sleep(1.0)
		# Esablish the direction you want to go
		GPIO.output(DIR_1,CW)
		GPIO.output(DIR_2,CW)

		# Run for 200 steps. This will change based on how you set you controller
		for x in range(200):

			# Set one coil winding to high
			GPIO.output(STEP_1,GPIO.HIGH)
			GPIO.output(STEP_2,GPIO.HIGH)
			# Allow it to get there.
			sleep(.005) # Dictates how fast stepper motor will run
			# Set coil winding to low
			GPIO.output(STEP_1,GPIO.LOW)
			GPIO.output(STEP_2,GPIO.LOW)
			sleep(.005) # Dictates how fast stepper motor will run

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