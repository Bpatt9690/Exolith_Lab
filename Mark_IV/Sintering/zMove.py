import RPi.GPIO as GPIO
from time import sleep
import time
import board
# import adafruit_vl53l0x
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()
# i2c = board.I2C()
# dSensor = adafruit_vl53l0x.VL53L0X(i2c)

def zMove(distance=0.3, dir=False, speed_mod=1):
    # Between 0 and 100, controls speed. 50 is medium speed.
    # Need to find speed that matches default speeds for x and y
    cycles = 20

    if speed_mod > 2:
        print("Speed modifier above 2, linear actuator cannot go above max speed.")
        exit()

    if speed_mod < 0.001:
        return

    GPIO.cleanup()
    in1 = int(os.getenv("LINEAR_in1"))
    in2 = int(os.getenv("LINEAR_in2"))
    en = int(os.getenv("LINEAR_en"))
    # NEEDS TESTING. num is a constant that can turn distance to seconds given the linear actuator's speed.
    num = 0.6715
    if dir:
        num = 0.3275
    print(num)
    seconds = distance / (num * speed_mod)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)

    # Sets up analog device (linear actuator)
    p = GPIO.PWM(en, 50)

    if dir:
    #     # Moves forward
    #     height_f = dSensor.range + distance
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    else:
    #     # Moves backward
    #     height_f = dSensor.range - distance
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)

    try:
        # Moves at default max speed (cycles) multiplied by speed mod to get actual speed.
        p.start(cycles * speed_mod)
        # while True:
        #     height_cur = dSensor.range
        #     if (dir and height_cur >= height_f) or (not dir and height_cur <= height_f):
        #         break
        sleep(seconds)
        p.stop()

    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


def main():
    num_args = len(sys.argv)
    if num_args == 2:
        num = float(sys.argv[1])
        if num < 0:
            zMove(abs(num), dir=False)
        else:
            zMove(abs(num), dir=True)
    else:
        zMove()
    GPIO.cleanup()


if __name__ == "__main__":
    main()