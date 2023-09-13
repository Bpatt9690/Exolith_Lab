import multiprocessing as mp
from xMove import xMove
from yMove import yMove
# from zMove import zMove
import sys

"""
Moves both X and Y axis a specified distance simultaneously and ending at the same time.
Uses multithreading.
"""

def xyMove(x_dist=8, y_dist=8, speed=0.5, pause=False):
    x_speed_mod = speed
    y_speed_mod = speed

    # x and y rotate determine if motors move clockwise or counterclockwise.
    # True for CW and False for CCW.
    x_rotate = True
    y_rotate = True
    if x_dist < 0:
        x_rotate = False
        x_dist = abs(x_dist)
    if y_dist < 0:
        y_rotate = False
        y_dist = abs(y_dist)

    # Decides which axis with move at max speed (1), and which will be slowed down.
    # max_dist = max(x_dist, y_dist, z_dist)
    max_dist = max(x_dist, y_dist)
    if x_dist == max_dist:
        y_speed_mod = (y_dist / x_dist) * y_speed_mod
    elif y_dist == max_dist:
        x_speed_mod = (x_dist / y_dist) * x_speed_mod

    # Starts moving x and y simultaneously in different processes.
    xProc = mp.Process(target=xMove, args=(x_dist, x_rotate, x_speed_mod, pause))
    yProc = mp.Process(target=yMove, args=(y_dist, y_rotate, y_speed_mod, pause))
    xProc.start()
    yProc.start()
    xProc.join()
    yProc.join()
    print("X and Y finished!")
    

def main():
    num_args = len(sys.argv)
    if num_args == 2:
        xyMove(float(sys.argv[1]))
    elif num_args == 3:
        xyMove(float(sys.argv[1]), float(sys.argv[2]))
    elif num_args == 4:
        xyMove(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        xyMove(pause=True)

if __name__ == "__main__":
    main()