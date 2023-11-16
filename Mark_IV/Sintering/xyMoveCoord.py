import multiprocessing as mp
from xMoveCoord import xMoveCoord
from yMoveCoord import yMoveCoord
# from zMove import zMove
import os
import sys

"""
Moves both X and Y axis a specified distance simultaneously and ending at the same time.
Uses multithreading.
"""

def xyMoveCoord(x_coord=5, y_coord=5, speed_mod=0.5, pause=False):
    x_file_name = "x_coord.txt"
    y_file_name = "y_coord.txt"
    os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")
    x_speed_mod = speed_mod
    y_speed_mod = speed_mod

    with open(x_file_name, "r") as f:
        x_curr = float(f.readline())
    with open(y_file_name, "r") as f:
        y_curr = float(f.readline())

    x_dist = abs(x_curr - x_coord)
    y_dist = abs(y_curr - y_coord)

    # Decides which axis with move at max speed (1), and which will be slowed down.
    # max_dist = max(x_dist, y_dist, z_dist)
    max_dist = max(x_dist, y_dist)
    if x_dist == max_dist:
        y_speed_mod = (y_dist / x_dist) * y_speed_mod
    elif y_dist == max_dist:
        x_speed_mod = (x_dist / y_dist) * x_speed_mod

    # Starts moving x and y simultaneously in different processes.
    xProc = mp.Process(target=xMoveCoord, args=(x_coord, x_speed_mod, pause))
    yProc = mp.Process(target=yMoveCoord, args=(y_coord, y_speed_mod, pause))
    xProc.start()
    yProc.start()
    xProc.join()
    yProc.join()
    print("X and Y finished!")
    

def main():
    num_args = len(sys.argv)
    if num_args == 2:
        xyMoveCoord(float(sys.argv[1]))
    elif num_args == 3:
        xyMoveCoord(float(sys.argv[1]), float(sys.argv[2]))
    elif num_args == 4:
        xyMoveCoord(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    else:
        xyMoveCoord()

if __name__ == "__main__":
    main()