import time
import multiprocessing as mp
from solarAlignment import solarTracking, solarElevationLogic, azimuthLogic
from xMove import xMove
from yMove import yMove
# from zMove import zMove
from axisReset import axis_reset

"""
Moves both X and Y axis a specified distance simultaneously and ending at the same time.
Uses multithreading.
"""

def xyMove(x_dist=8, y_dist=8, z_dist=6):
    x_speed_mod = 1
    y_speed_mod = 1
    z_speed_mod = 1

    # x and y rotate determine if motors move clockwise or counterclockwise.
    # True for CW and False for CCW.
    x_rotate = True
    y_rotate = True
    z_dir = True
    if x_dist < 0:
        x_rotate = False
    if y_dist < 0:
        y_rotate = False
    if z_dist < 0:
        z_dir = False

    # Decides which axis with move at max speed (1), and which will be slowed down.
    # max_dist = max(x_dist, y_dist, z_dist)
    max_dist = max(x_dist, y_dist)
    if x_dist == max_dist:
        y_speed_mod = y_dist / x_dist
        z_speed_mod = z_dist / x_dist
    elif y_dist == max_dist:
        x_speed_mod = x_dist / y_dist
        z_speed_mod = z_dist / y_dist
    # else:
    #     x_speed_mod = x_dist / z_dist
    #     y_speed_mod = y_dist / z_dist

    # ar = axis_reset()
    # ar.elevation_reset()
    # if not(solarElevationLogic()):
    #     exit()
    # if not(azimuthLogic()):
    #     exit()
    # alignProc = mp.Process(target=solarTracking)

    # Starts moving x and y simultaneously in different processes.
    xProc = mp.Process(target=xMove, args=(x_dist, x_rotate, x_speed_mod))
    yProc = mp.Process(target=yMove, args=(y_dist, y_rotate, y_speed_mod))
    # alignProc.start()
    xProc.start()
    yProc.start()
    # zMove(z_dist, z_dir, z_speed_mod)
    xProc.join()
    yProc.join()
    time.sleep(5)
    # alignProc.terminate()
    print("X and Y finished!")
    

def main():
    xyMove()

if __name__ == "__main__":
    main()