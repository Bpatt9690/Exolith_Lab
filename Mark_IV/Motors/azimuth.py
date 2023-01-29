import RPi.GPIO as GPIO
from time import sleep
import time
import SI1145.SI1145 as SI1145
from Logging import logger
from datetime import date, datetime
import serial
import pytz
import os


sensor = SI1145.SI1145()


def stepMovement(direction, steps):
    GPIO.setwarnings(False)
    GPIO.cleanup()

    DIR_1 = 13  # DIR+
    STEP_1 = 26  # PULL+

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

        print(steps)
        for x in range(steps):
            print("Adjusting....")

            GPIO.output(STEP_1, GPIO.HIGH)
            # .5 == super slow
            # .00005 == breaking
            sleep(0.05)
            GPIO.output(STEP_1, GPIO.LOW)
            sleep(0.05)

            uv = uv_sensor()

            if uv > uv_high:
                uv_low = uv_high
                uv_high = uv

            print("UV High: ", uv_high)
            print("UV Low: ", uv_low)
            logger.logInfo(timeStamp(), uv_high)

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def track(direction, steps, uvMax, uvUpper, uvLower):
    GPIO.setwarnings(False)
    GPIO.cleanup()

    DIR_1 = 13  # DIR+
    STEP_1 = 26  # PULL+

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


def uv_sensor():
    global sensor
    uvAverage = 0
    for i in range(10):
        UV = sensor.readUV()
        uvIndex = UV
        uvAverage += uvIndex
        time.sleep(0.1)
    return uvAverage / 10


def maxValue():
    inputFile = open("uvsensor.txt", "r")
    num_list = [float(num) for num in inputFile.read().split()]
    # OR, num_list = map(float, inputFile.read().split())

    counter = len(num_list)
    total = sum(num_list)

    # Your desired values
    max_val = max(num_list)
    min_val = min(num_list)

    print("Max val is: ", +max_val)
    return max_val


# Current timeStamps in EST; Configurable
def timeStamp():
    tz_NY = pytz.timezone("America/New_York")
    datetime_NY = datetime.now(tz_NY)
    return str(datetime_NY.strftime("%H:%M:%S"))


def solarPositioning(uvMax):

    # uv_current = uv_sensor()

    uvUpper = uvMax + uvMax * (0.5)
    uvLower = uvMax - (uvMax * (0.5))

    print(uvMax)
    print(uvUpper)
    print(uvLower)

    # just for testing, returing to where we came from
    stepMovement(0, 25)

    track(1, 25, uvMax, uvUpper, uvLower)


def main():
    os.remove("uvsensor.txt")
    stepMovement(1, 25)
    uvMax = maxValue()
    solarPositioning(uvMax)


if __name__ == "__main__":
    main()
