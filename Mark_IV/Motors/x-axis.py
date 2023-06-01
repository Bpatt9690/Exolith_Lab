import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches

"""
Moves both motor 1 and motor 2 of the X axis. Currently CW || 0 moves the x axis forward
DOES NOT HAVE LIMIT SWITCH FUNCTIONALITY INCLUDED. POTENTIALLY DESTRUCTIVE 
"""
# CW Away from limit switch

ls = limitSwitches()


def xMovement():
    GPIO.setwarnings(False)
    GPIO.cleanup()

    DIR_1 = 19  # DIR+
    STEP_1 = 20  # PULL+

    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1

    MAX = 10000

    GPIO.setmode(GPIO.BCM)
    motor1_switch = 4
    motor2_switch = 27

    GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(motor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    # Set the first direction
    GPIO.output(DIR_1, CW)

    # !!!Not Calling LimitSwitches Class!!!#

    try:
        while 1:

            for x in range(MAX):

                GPIO.output(STEP_1, GPIO.HIGH)
                # .5 == super slow
                # .00005 == breaking
                sleep(0.001)  # Dictates how fast stepper motor will run
                GPIO.output(STEP_1, GPIO.LOW)
                sleep(0.001)

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    xMovement()


if __name__ == "__main__":
    main()
