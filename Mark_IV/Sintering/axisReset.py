from Logging import logger
import RPi.GPIO as GPIO
import multiprocessing as mp
from time import sleep
from xMove import xMove
from yMove import yMove
from zMove import zMove
from xMoveCoord import xMoveCoord
from yMoveCoord import yMoveCoord
from xyMoveCoord import xyMoveCoord
import sys
import xyMove
from Limit_Switches import limitSwitches
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class axis_reset:
    def __init__(self):
        """Constructor for axis_reset class"""
        self.logger = logger()
        self.ls = limitSwitches()

    # Responsible for resetting the elevation axis.
    # Retracts elevation boom until limit switch is triggered
    def elevation_reset(self):
        """Responsible for resetting the elevation axis."""
        GPIO.setwarnings(False)
        self.logger.logInfo("Resetting Elevation")
        GPIO.setmode(GPIO.BCM)
        switch = int(os.getenv("limitSwitchElavation"))
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Direction pin from controller
        AZ_DIR = int(os.getenv("ELAVATION_Direction"))
        # Step pin from controller
        AZ_STEP = int(os.getenv("ELAVATION_Pulse"))

        # 0/1 used to signify clockwise or counterclockwise.
        CW = 0
        CCW = 1

        # Setup pin layout on RPI
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(AZ_DIR, GPIO.OUT)
        GPIO.setup(AZ_STEP, GPIO.OUT)
        GPIO.output(AZ_DIR, CW)

        while 1:

            for x in range(200):
                GPIO.output(AZ_STEP, GPIO.HIGH)
                # Dictates how fast stepper motor will run
                sleep(0.05)
                GPIO.output(AZ_STEP, GPIO.LOW)

                if GPIO.input(switch) == 0:
                    self.logger.logInfo("Elevation Homing Successful")
                    GPIO.cleanup()
                    return True

        sleep(0.1)

    def x_axis_reset(self):
        """Responsible for resetting the x axis."""
        MAX = 10000
        xMove(MAX, 0, 0.7)
        self.logger.logInfo("X Homing Successful")

    def y_axis_reset(self):
        """Responsible for resetting the y axis."""
        MAX = 10000
        yMove(MAX, 0, 0.7)
        self.logger.logInfo("Y Homing Successful")

    def z_axis_reset(self):
        """Responsible for resetting the z axis."""
        MAX = 10000
        zMove(MAX, 0, 0.3)
        self.logger.logInfo("Z Homing Successful")
    
    def xy_reset(self):
        try:
            xProc = mp.Process(target=self.x_axis_reset)
            yProc = mp.Process(target=self.y_axis_reset)
            xProc.start()
            yProc.start()
            xProc.join()
            yProc.join()
            return True
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False
        
    def x_axis_mid(self):
        try:
            xMoveCoord(13.5, speed_mod=0.7)
            sleep(0.1)
            return True
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False

    def y_axis_mid(self):
        try:
            yMoveCoord(10, speed_mod=0.7)
            sleep(0.1)
            return True
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False
        
    def xy_axis_mid(self):
        try:
            xyMoveCoord(13.5, 10, speed_mod=0.7)
            sleep(0.1)
            return True
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False


def main():
    ar = axis_reset()
    num_args = len(sys.argv)
    if num_args > 1 and sys.argv[1] == "mid":
        ar.xy_axis_mid()
    else:
        ar.xy_reset()
    

if __name__ == "__main__":
    main()
