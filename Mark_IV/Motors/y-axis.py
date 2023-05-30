# prod ready
import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches

"""
Moves both motor 3 and motor 4 of the Y axis. Currently CW || 0 moves the y axis forward
DOES NOT HAVE LIMIT SWITCH FUNCTIONALITY INCLUDED. POTENTIALLY DESTRUCTIVE 
"""

ls = limitSwitches()


def yMovement():
    # Direction pin from controller
    GPIO.setwarnings(False)
    GPIO.cleanup()
    DIR_1 = 26  # DIR+
    # DIR_2 = 25 #DIR+
    # Step pin from controller
    STEP_1 = 13  # PULL+
    # STEP_2 = 24 #PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    flag = 0

    GPIO.setmode(GPIO.BCM)
    motor1_switch = 24
    motor2_switch = 12
    GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(motor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CCW)
    # GPIO.output(DIR_2, CW)
    # CW Away from limit switch
    try:
        while 1:

            for x in range(MAX):

                # Set one coil winding to high
                GPIO.output(STEP_1, GPIO.HIGH)
                #        GPIO.output(STEP_2,GPIO.HIGH)
                # .5 == super slow
                # .00005 == breaking
                sleep(0.001)  # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(STEP_1, GPIO.LOW)
                #       GPIO.output(STEP_2,GPIO.LOW)
                sleep(0.001)  # Dictates how fast stepper motor will run

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    yMovement()


if __name__ == "__main__":
    main()
