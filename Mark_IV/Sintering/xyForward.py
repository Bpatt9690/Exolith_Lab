import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

"""
Moves both X and Y axis. Currently CW || 0 moves both axis forward
DOES NOT HAVE LIMIT SWITCH FUNCTIONALITY INCLUDED. POTENTIALLY DESTRUCTIVE 
"""


ls = limitSwitches()


def xyForward():
    # Direction pin from controller
    GPIO.cleanup()
    xDIR = int(os.getenv("MOTOR_X_Direction"))  # DIR+
    # Step pin from controller
    xSTEP = int(os.getenv("MOTOR_X_Pulse")) # PULL+

    yDIR = int(os.getenv("MOTOR_Y_Direction"))  # DIR+
    # Step pin from controller
    ySTEP = int(os.getenv("MOTOR_Y_Pulse"))  # PULL+

    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    flag = 0

    GPIO.setmode(GPIO.BCM)
    xmotor1_switch = int(os.getenv("limitSwitchX_1"))
    xmotor2_switch = int(os.getenv("limitSwitchX_2"))
    ymotor1_switch = int(os.getenv("limitSwitchY_1"))
    ymotor2_switch = int(os.getenv("limitSwitchY_2"))
    GPIO.setup(xmotor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(xmotor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ymotor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ymotor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(xDIR, GPIO.OUT)
    GPIO.setup(xSTEP, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(xDIR, CW)

    GPIO.setup(yDIR, GPIO.OUT)
    GPIO.setup(ySTEP, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(yDIR, CW)

    # CW Away from limit switch
    try:
        # Run forever.
        while 1:

            # Run for 200 steps. This will change based on how you set you controller
            for x in range(MAX):

                # Set one coil winding to high
                GPIO.output(xSTEP, GPIO.HIGH)
                GPIO.output(ySTEP, GPIO.HIGH)
                # Allow it to get there.
                # .5 == super slow
                # .00005 == breaking
                sleep(0.005)  # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(xSTEP, GPIO.LOW)
                GPIO.output(ySTEP, GPIO.LOW)
                sleep(0.005)  # Dictates how fast stepper motor will run

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    xyForward()


if __name__ == "__main__":

    main()
