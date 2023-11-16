from solarAlignment import main as Alignment
from axisReset import axis_reset
from shapes import box2d
import multiprocessing as mp
import time

def main():
    # Max distance for x and y axis on each rod, in cm.
    X_MAX = 27
    Y_MAX = 20

    ar = axis_reset()
    alignProc = mp.Process(target=Alignment)
    alignProc.start()
    ar.xy_reset()
    time.sleep(20)
    box2d(x_dist=X_MAX, y_dist=Y_MAX, speed_mod=0.2)
    alignProc.join()

if __name__ == "__main__":
    main()
