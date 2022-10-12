import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
switch=16
GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
x = 0


try:

	while(1):

		if GPIO.input(switch) == 0:
			x+=1
			
		else:
			x=0

		if x > 5:
			print('Pressed')

		sleep(.05)

except KeyboardInterrupt:
    print("GPIO Cleanup")
    GPIO.cleanup()