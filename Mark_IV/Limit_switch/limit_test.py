import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
switch=2
GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while(1):
	if GPIO.input(switch)==0:
		print('Button was pressed')
		sleep(.1)
	sleep(.1)