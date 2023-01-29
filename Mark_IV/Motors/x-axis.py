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
    # Direction pin from controller
    GPIO.cleanup()
    DIR_1 = 6  # DIR+
    # Step pin from controller
    STEP_1 = 5  # PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    flag = 0

    GPIO.setmode(GPIO.BCM)
    motor1_switch = 27
    motor2_switch = 21
    GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(motor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CW)

    try:
        while 1:

            for x in range(MAX):

                # Set one coil winding to high
                GPIO.output(STEP_1, GPIO.HIGH)
                # .5 == super slow
                # .00005 == breaking
                sleep(0.005)
                # Set coil winding to low
                GPIO.output(STEP_1, GPIO.LOW)
                sleep(0.005)

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    xMovement()


if __name__ == "__main__":
    main()
