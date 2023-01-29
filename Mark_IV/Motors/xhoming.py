# prod ready
import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches


"""
Moves both motor 1 and motor 2 of the X axis. Currently CWW || 1 moves the x axis toward home (limitswitches)
"""

ls = limitSwitches()


def xHoming():
    # Direction pin from controller
    GPIO.cleanup()
    DIR_1 = 6  # DIR+
    STEP_1 = 5  # PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1

    MAX = 10000

    motor1_flag = 0
    motor2_flag = 0

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

    # Set the first direction
    GPIO.output(DIR_1, CCW)
    try:
        while 1:

            for x in range(MAX):

                GPIO.output(STEP_1, GPIO.HIGH)
                # .5 == super slow
                # .00005 == breaking
                sleep(0.005)  # Dictates how fast stepper motor will run

                GPIO.output(STEP_1, GPIO.LOW)

                sleep(0.005)

                if GPIO.input(motor2_switch) == 0:
                    motor2_flag += 1
                elif GPIO.input(motor1_switch) == 0:
                    motor1_flag += 1
                else:
                    motor2_flag = 0
                    motor1_flag = 0

                if motor2_flag >= 5:
                    print("X Homed")
                    sleep(1)
                    return

                elif motor1_flag >= 5:
                    print("X Homed")
                    sleep(1)
                    return

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    xHoming()


if __name__ == "__main__":
    main()
