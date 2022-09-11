#Elevation axis


import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
switch=6
GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while(1):
	if GPIO.input(switch)==1:
		print('Button was pressed')
		sleep(1)
	sleep(.1)
