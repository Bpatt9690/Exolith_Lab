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
    speed_mod = 1
    x_prev = 0
    y_prev = 0
    x = 0
    y = 0
    ref = 18  # The number of segments that produces correct dimensions by default.
    num_segs = 18
    radius = sqrt(x_circle * x_circle + y_circle * y_circle)

    x1_motor_switch = int(os.getenv("limitSwitchX_1"))
    x2_motor_switch = int(os.getenv("limitSwitchX_2"))
    y1_motor_switch = int(os.getenv("limitSwitchY_1"))
    y2_motor_switch = int(os.getenv("limitSwitchY_2"))
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(x1_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(x2_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(y1_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(y2_motor_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    # Get start and end angle on unit circle.
    start_ang = math.pi / 2
    end_ang = math.pi / 2
    if x_circle != 0:
        start_ang = atan2(y_circle, x_circle)
    if x_circle + x_dist != 0:
        end_ang = atan2(y_circle - y_dist, x_circle + float(x_dist))

    if rotation:
        if end_ang <= start_ang:
            end_ang += 2 * math.pi
        start_ang = math.pi - start_ang
        end_ang = math.pi - end_ang
    elif not rotation and end_ang >= start_ang:
        end_ang -= 2 * math.pi
    angle_delta = abs((end_ang - start_ang) / float(num_segs))
    theta = start_ang
    if start_ang > end_ang:
        angle_delta *= -1

    x_prev = radius * abs(cos(theta))
    y_prev = radius * abs(sin(theta))

    for _ in range(num_segs):
        # Stop circle if any limit switches are activated.
        if GPIO.input(y2_motor_switch) == 0 or GPIO.input(y1_motor_switch) == 0 or GPIO.input(x2_motor_switch) == 0 or GPIO.input(x1_motor_switch) == 0:
            break

        # Get current angle on unit circle.
        theta += angle_delta

        x = (x_prev - radius * abs(cos(theta))) * (ref / num_segs)
        y = (y_prev - radius * abs(sin(theta))) * (ref / num_segs)

        x_speed = speed_mod
        y_speed = speed_mod
        if abs(x) >= abs(y) and x != 0:
            y_speed = y_speed * abs(y / x)
        elif abs(x) < abs(y) and y != 0:
            x_speed = x_speed * abs(x / y)

        x_rotate = True
        y_rotate = True
        if (angle_delta < 0 and sin(theta) < 0) or (angle_delta > 0 and sin(theta) > 0):
            x_rotate = False
        if (angle_delta < 0 and cos(theta) < 0) or (angle_delta > 0 and cos(theta) > 0):
            y_rotate = False

        xProc = mp.Process(target=xMove, args=(abs(x), x_rotate, x_speed))
        yProc = mp.Process(target=yMove, args=(abs(y), y_rotate, y_speed))
        xProc.start()
        yProc.start()
        xProc.join()
        yProc.join()

        x_prev = radius * abs(cos(theta))
        y_prev = radius * abs(sin(theta))


def main():
    if len(sys.argv) == 6:
        xyCurve(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        xyCurve()

if __name__ == "__main__":
    main()