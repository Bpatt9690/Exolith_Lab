import time
import multiprocessing as mp
from solarAlignment import solarTracking, solarElevationLogic, azimuthLogic
from xMove import xMove
from yMove import yMove
from axisReset import axis_reset

"""
Moves both X and Y axis a specified distance simultaneously and ending at the same time.
Uses multithreading.
"""

def xyMove(x_dist=6, y_dist=6):
    # x and y rotate determine if motors move clockwise or counterclockwise.
    # True for CW and False for CCW.
    x_rotate = True
    y_rotate = True
    if x_dist < 0:
        x_rotate = False
    if y_dist < 0:
        y_rotate = False

    # Decides which axis with move at max speed (1), and which will be slowed down.
    if x_dist > y_dist:
        x_speed_mod = 1
        y_speed_mod = y_dist / x_dist
    else:
        x_speed_mod = x_dist / y_dist
        y_speed_mod = 1

    print(mp.cpu_count)

    # ar = axis_reset()
    # ar.elevation_reset()
    # if not(solarElevationLogic()):
    #     exit()
    # if not(azimuthLogic()):
    #     exit()
    # alignProc = mp.Process(target=solarTracking, args=())

    # Starts moving x and y simultaneously in different processes.
    xProc = mp.Process(target=xMove, args=(x_dist, x_rotate, x_speed_mod))
    yProc = mp.Process(target=yMove, args=(y_dist, y_rotate, y_speed_mod))
    # alignProc.start()
    xProc.start()
    yProc.start()
    xProc.join()
    yProc.join()
    time.sleep(5)
    # alignProc.terminate()
    print("X and Y finished!")
    

def main():
    xyMove()

if __name__ == "__main__":
    main()