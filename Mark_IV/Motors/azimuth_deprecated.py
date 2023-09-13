import RPi.GPIO as GPIO
from time import sleep
import time
from Logging import logger
from datetime import date, datetime
import serial
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def track(direction, steps, uvMax, uvUpper, uvLower):
    GPIO.setwarnings(False)
    GPIO.cleanup()

    DIR_1 = os.getenv("AZIMUTH_Direction")  # DIR+
    STEP_1 = os.getenv("AZIMUTH_Pulse")  # PULL+

    # 0/1 used to signify clockwise or counterclockwise.
    CW = direction

    if direction is 1:
        CCW = 0
    else:
        CCW = 1

    MAX = 100

    GPIO.setmode(GPIO.BCM)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CW)

    uv_current = uv_sensor()
    print("Stationary UV value: ", uv_current)

    uv_high = uv_current
    uv_low = uv_current

    try:

        for x in range(steps):
            print("Adjusting....")

            GPIO.output(STEP_1, GPIO.HIGH)
            # .5 == super slow
            # .00005 == breaking
            sleep(0.05)
            GPIO.output(STEP_1, GPIO.LOW)
            sleep(0.05)

            uv = uv_sensor()

            print("current uv:", uv)
            print("uvLower", uvLower)
            print("uvUpper", uvUpper)
            print()

            if uvLower <= uv < uvMax:
                print("Stopping here")
                stepMovement(0, 1)
                break

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    os.remove("uvsensor.txt")
    stepMovement(1, 25)
    uvMax = maxValue()
    solarPositioning(uvMax)


if __name__ == "__main__":
    main()
