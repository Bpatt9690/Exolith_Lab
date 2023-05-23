import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

'''
Moves both motor 1 and motor 2 of the X axis. Currently CW || 0 moves the x axis forward
DOES NOT HAVE LIMIT SWITCH FUNCTIONALITY INCLUDED. POTENTIALLY DESTRUCTIVE 
'''

ls = limitSwitches()

def xMove(distance):
    # Direction pin from controller
    GPIO.cleanup()
    DIR = int(os.getenv("MOTOR_X_Direction")) #DIR+
    STEP = int(os.getenv("MOTOR_X_Pulse")) #PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    flag = 0
    # distance = int(input()) #must be in cm!
    seconds = distance/0.6157

    GPIO.setmode(GPIO.BCM)
    motor1_switch = int(os.getenv("limitSwitchX_1"))
    motor2_switch = int(os.getenv("limitSwitchX_2"))
    GPIO.setup(motor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(motor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR, CW)

    #CW Away from limit switch
    try:

        now = time.time()
        timer = 0

        # x = 0
        
        # Run forever.
        while(timer <= seconds):

            # Run for 200 steps. This will change based on how you set you controller
            for x in range(200):

                # Set one coil winding to high
                GPIO.output(STEP,GPIO.HIGH)
                # Allow it to get there.
                #.5 == super slow
                # .00005 == breaking
                sleep(.001) # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(STEP,GPIO.LOW)
                sleep(.001) # Dictates how fast stepper motor will run
                
                end = time.time()
                timer = round(end - now) 

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    xMove()

if __name__ == '__main__':
    main()