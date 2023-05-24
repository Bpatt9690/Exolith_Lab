import RPi.GPIO as GPIO
from time import sleep
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
# load_dotenv()

def zMove(distance=3, dir=True, speed_mod=1):
    # between 0 and 100, controls speed. 50 is medium speed.
    cycles = 50

    # NEEDS TESTING. num is a constant that can turn distance to seconds given the linear actuator's speed.
    num = 1

    if speed_mod > 1:
        print("Speed modifier above 1, linear actuator cannot go above max speed.")
        exit()

    GPIO.cleanup()
    # in1 = int(os.getenv("LINEAR_in1"))
    # in2 = int(os.getenv("LINEAR_in2"))
    # en = int(os.getenv("LINEAR_en"))
    in1 = 7
    in2 = 8
    en = 9
    seconds = distance / (num * speed_mod)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)

    # Sets up analog device (linear actuator)
    p = GPIO.PWM(en, 1000)

    if dir:
        # Moves forward
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    else:
        # Moves backward
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)

    try:
        # Moves at default max speed (cycles) multiplied by speed mod to get actual speed.
        p.start(cycles * speed_mod)
        sleep(seconds)
        p.stop()

    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()


def main():
    zMove()
    GPIO.cleanup()

if __name__ == "__main__":
    main()