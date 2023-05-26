import time
from math import cos, sin, tan, sqrt
import math
import multiprocessing as mp
from xMove import xMove
from yMove import yMove

def xyCurve(x_dist=6, y_dist=6, x_circle=0, y_circle=6):
    speed_mod = 1
    x_prev = 0
    y_prev = 0
    x = 0
    y = 0
    num_segs = 10
    radius = sqrt(x_circle * x_circle + y_circle * y_circle)

    # x and y rotate determine if motors move clockwise or counterclockwise.
    # True for CW and False for CCW.
    x_rotate = True
    y_rotate = True
    if x_dist < 0:
        x_rotate = False
    if y_dist < 0:
        y_rotate = False

    # Get start and end angle on unit circle.
    if(x_circle == 0):
        start_ang = math.pi / 2
    else:
        start_ang = tan(y_circle / x_circle)
    end_ang = tan((y_circle - y_dist) / (x_circle + float(x_dist)))
    angle_delta = (start_ang - end_ang) / float(num_segs)
    theta = start_ang

    y_max = radius * sin(theta)

    for _ in range(num_segs):
        # Get current angle on unit circle.
        theta -= angle_delta

        x = abs(x_prev - radius * abs(cos(theta)))
        y = abs(y_max - y_prev - radius * abs(sin(theta)))

        # Use angle to change the travel distance and speed for the segments.
        # NEEDS TO BE CHANGED

        x_speed = speed_mod
        y_speed = speed_mod
        if x >= y and x != 0:
            y_speed = speed_mod * (y / x)
        elif x < y and y != 0:
            x_speed = speed_mod * (x / y)

        xProc = mp.Process(target=xMove, args=(x, x_rotate, x_speed))
        yProc = mp.Process(target=yMove, args=(y, y_rotate, y_speed))
        xProc.start()
        yProc.start()
        xProc.join()
        yProc.join()

        x_prev += x
        y_prev += y


def main():
    xyCurve()

if __name__ == "__main__":
    main()