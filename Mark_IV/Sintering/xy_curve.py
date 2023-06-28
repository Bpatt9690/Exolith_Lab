import RPi.GPIO as GPIO
from math import cos, sin, atan2, sqrt
import math
import os
import sys
import multiprocessing as mp
from Limit_Switches import limitSwitches
from xMove import xMove
from yMove import yMove

ls = limitSwitches()

def xyCurve(x_dist=0, y_dist=0, x_circle=0, y_circle=3, rotation=True):
    # Initialize variables
    speed_mod = 1

    # Tracks the total previous x and y movement
    x_prev = 0
    y_prev = 0

    # Tracks the current distance to move for x and y
    x = 0
    y = 0

    # Used to stop when limit switch activated
    motor_flag = 0

    # Defines how many different lines curve is divided into
    num_segs = 20

    # Radius of circle that curve being drawn is a part of
    radius = sqrt(x_circle * x_circle + y_circle * y_circle)

    # Pin setup
    x1_motor_switch = int(os.getenv("limitSwitchX_1"))
    x2_motor_switch = int(os.getenv("limitSwitchX_2"))
    y1_motor_switch = int(os.getenv("limitSwitchY_1"))
    y2_motor_switch = int(os.getenv("limitSwitchY_2"))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(x1_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(x2_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(y1_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(y2_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # Get start and end angle on unit circle. Default to pi / 2
    start_ang = math.pi / 2
    end_ang = math.pi / 2
    if x_circle != 0:
        start_ang = atan2(y_circle, x_circle)
    if x_circle + x_dist != 0:
        end_ang = atan2(y_circle - y_dist, x_circle + float(x_dist))

    # Changes end angle and or start angle to be relative to each other based on which direction the curve is drawn.
    # Makes end angle less than start angle to move CW, or opposite for CCW
    if rotation:
        if end_ang <= start_ang:
            end_ang += 2 * math.pi

        # Reflects both angles to opposite side of circle to enable starting from both sides
        start_ang = math.pi - start_ang
        end_ang = math.pi - end_ang
    elif not rotation and end_ang >= start_ang:
        end_ang -= 2 * math.pi
    
    # Finds the amount of change in angle per iteration
    angle_delta = (end_ang - start_ang) / float(num_segs)

    # tracks the current angle
    theta = start_ang

    # Initializes with the distance from the center of the unit circle based on start angle
    x_prev = radius * abs(cos(theta))
    y_prev = radius * abs(sin(theta))

    for _ in range(num_segs):
        # Get current angle on unit circle
        theta += angle_delta

        # Finds distance to move next
        x = (x_prev - radius * abs(cos(theta)))
        y = (y_prev - radius * abs(sin(theta)))

        # Speed changes based on how far x and y need to move, have to stop moving at the same time
        x_speed = speed_mod
        y_speed = speed_mod
        if abs(x) >= abs(y) and x != 0:
            y_speed = y_speed * abs(y / x)
        elif abs(x) < abs(y) and y != 0:
            x_speed = x_speed * abs(x / y)

        # Finds the directions the x and y motors need to move
        x_rotate = True
        y_rotate = True
        if (angle_delta < 0 and sin(theta) < 0) or (angle_delta > 0 and sin(theta) > 0):
            x_rotate = False
        if (angle_delta < 0 and cos(theta) < 0) or (angle_delta > 0 and cos(theta) > 0):
            y_rotate = False

        # Moves x and y in straight line given a distance, in a given direction, at a given speed
        xProc = mp.Process(target=xMove, args=(abs(x), x_rotate, x_speed))
        yProc = mp.Process(target=yMove, args=(abs(y), y_rotate, y_speed))
        xProc.start()
        yProc.start()
        xProc.join()
        yProc.join()

        # Stop circle if any limit switches are activated.
        if GPIO.input(y2_motor_switch) == 0 or GPIO.input(y1_motor_switch) == 0 or GPIO.input(x2_motor_switch) == 0 or GPIO.input(x1_motor_switch) == 0:
            motor_flag += 1
        else:
            motor_flag = 0
        if motor_flag == 2:
            break

        # Updates the current displacement from the center of unit circle.
        x_prev = radius * abs(cos(theta))
        y_prev = radius * abs(sin(theta))


def main():
    if len(sys.argv) == 6:
        xyCurve(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), bool(int(sys.argv[5])))
    else:
        xyCurve()

if __name__ == "__main__":
    main()