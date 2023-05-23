import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches
import time
from dotenv import load_dotenv
from xMove import xMove
from yMove import yMove
from axisReset import axis_reset
import os

# Load environment variables from .env file
load_dotenv()

'''
Moves both motor 1 and motor 2 of the X axis. Currently CW || 0 moves the x axis forward
DOES NOT HAVE LIMIT SWITCH FUNCTIONALITY INCLUDED. POTENTIALLY DESTRUCTIVE 
'''

ls = limitSwitches()

def trace_box(x_dist=14, y_dist=9):
    ar = axis_reset()
    ar.x_axis_reset()
    ar.y_axis_reset()

    # Direction pin from controller
    y_increment = 3
    num_lines = int(y_dist / y_increment)

    clockwise = True
    #CW Away from limit switch
    try:
        # Make box with given number of lines.
        for _ in range(num_lines):
            xMove(x_dist, clockwise)
            yMove(y_increment, True)
            clockwise = not(clockwise)


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    trace_box()

if __name__ == '__main__':
    main()