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

def yMove(distance=6, clockwise=True, speed_mod=1):
    if speed_mod > 1:
        print("Speed modifier above 1, y motor cannot go above max speed.")
        exit()

    # Direction pin from controller
    GPIO.cleanup()
    DIR = int(os.getenv("MOTOR_Y_Direction")) #DIR+
    STEP = int(os.getenv("MOTOR_Y_Pulse")) #PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    motor_flag = 0
    seconds = distance / (0.6157 * speed_mod)

    GPIO.setmode(GPIO.BCM)
    motor1_switch = int(os.getenv("limitSwitchY_1"))
    motor2_switch = int(os.getenv("limitSwitchY_2"))
    GPIO.setup(motor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(motor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    # Set the first direction you want it to spin
    if clockwise == True:
        GPIO.output(DIR, CW)
    else:
        GPIO.output(DIR, CCW)

    #CW Away from limit switch
    try:

        now = time.time()
        timer = 0

        # x = 0
        
        # Run forever.
        while(timer <= seconds):
            # # Run for 200 steps. This will change based on how you set you controller
            # for x in range(200):

            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            #.5 == super slow
            # .00005 == breaking
            sleep(.001 / speed_mod) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.001 / speed_mod) # Dictates how fast stepper motor will run
                
            end = time.time()
            timer = round(end - now)

            if timer <= seconds:
                break
            
            if GPIO.input(motor2_switch) == 0 or GPIO.input(motor1_switch) == 0:
                motor_flag += 1
            else:
                motor_flag = 0

            if motor_flag >= 5:
                break

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    yMove()
    GPIO.cleanup()

if __name__ == '__main__':
    main()