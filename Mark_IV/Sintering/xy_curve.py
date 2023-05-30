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

    # Get start and end angle on unit circle.
    if(x_circle == 0):
        start_ang = math.pi / 2
    else:
        start_ang = tan(y_circle / x_circle)
    end_ang = tan((y_circle - y_dist) / (x_circle + float(x_dist)))
    angle_delta = (start_ang - end_ang) / float(num_segs)
    theta = start_ang
    if start_ang > end_ang:
        angle_delta *= -1

    x_prev = radius * abs(cos(theta))
    y_prev = radius * abs(sin(theta))

    for _ in range(num_segs):
        # Get current angle on unit circle.
        theta += angle_delta

        x = x_prev - radius * abs(cos(theta))
        y = y_prev - radius * abs(sin(theta))

        # Use angle to change the travel distance and speed for the segments.
        # NEEDS TO BE CHANGED

        x_speed = speed_mod
        y_speed = speed_mod
        if abs(x) >= abs(y) and x != 0:
            y_speed = speed_mod * abs(y / x)
        elif abs(x) < abs(y) and y != 0:
            x_speed = speed_mod * abs(x / y)

        x_rotate = True
        y_rotate = True
        if (angle_delta < 0 and y > 0) or (angle_delta > 0 and y < 0):
            x_rotate = False
        if (angle_delta < 0 and x < 0) or (angle_delta > 0 and x > 0):
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
    xyCurve()

if __name__ == "__main__":
    main()