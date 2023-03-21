import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches
# from dotenv import load_dotenv
# import os

"""
Moves both motor 1 and motor 2 of the X axis. Currently CW || 0 moves the x axis forward
DOES NOT HAVE LIMIT SWITCH FUNCTIONALITY INCLUDED. POTENTIALLY DESTRUCTIVE 
"""
# CW Away from limit switch

ls = limitSwitches()


def xMovement():
    GPIO.cleanup()
    DIR_1 = 27  # DIR+
    STEP_1 = 4  # PULL+
    EB = 21
    # DIR_1 = os.getenv("MOTOR_EL_DIR")
    # STEP_1 = os.getenv("MOTOR_EL_PULSE")
    CW = 0
    CCW = 1
    counter = 0
    steps = 1000000

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)
    
    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)
    GPIO.setup(EB, GPIO.IN)

    # Set the first direction you want it to spin
<<<<<<< Updated upstream
    GPIO.output(DIR_1, CCW)

    try:
        while 1:

            for x in range(1000):

                # Set one coil winding to high
                GPIO.output(STEP_1, GPIO.HIGH)
                # Set coil winding to low
            #  GPIO.output(STEP_1,GPIO.LOW)
            print("running")
            GPIO.output(STEP_1, GPIO.LOW)
            sleep(0.0001)
=======
    GPIO.output(DIR_1, CW)

    try:
        while steps > 0:
            # Set one coil winding to high
            GPIO.output(STEP_1, GPIO.HIGH)
            GPIO.output(STEP_1, GPIO.LOW)

            # counter += GPIO.input(EB)
            # print(counter)
            
            steps -= 1
>>>>>>> Stashed changes

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()

    GPIO.cleanup()

def main():
    xMovement()


if __name__ == "__main__":
    main()
