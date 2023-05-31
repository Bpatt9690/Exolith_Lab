# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
from time import sleep
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def actuator():
    in1 = int(os.getenv("LINEAR_in1"))
    in2 = int(os.getenv("LINEAR_in2"))
    en = int(os.getenv("LINEAR_en"))
    temp1 = 1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    p = GPIO.PWM(en, 50)

    p.start(25)
    print("\n")
    print("The default speed & direction of motor is LOW & Forward.....")
    print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
    print("\n")

    while 1:
        x = input()

        if x == "r":
            print("run")
            if temp1 == 1:
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                print("forward")
                x = "z"
            else:
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                print("backward")
                x = "z"

        elif x == "s":
            print("stop")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
            x = "z"

        elif x == "f":
            print("forward")
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            temp1 = 1
            x = "z"

        elif x == "b":
            print("backward")
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            temp1 = 0
            x = "z"

        elif x == "l":
            print("low")
            p.ChangeDutyCycle(25)
            x = "z"

        elif x == "m":
            print("medium")
            p.ChangeDutyCycle(50)
            x = "z"

        elif x == "h":
            print("high")
            p.ChangeDutyCycle(75)
            x = "z"

        elif x == "e":
            GPIO.cleanup()
            print("GPIO Clean up")
            break

        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")


def main():
    actuator()


if __name__ == "__main__":
    main()