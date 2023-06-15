from Logging import logger
import RPi.GPIO as GPIO
import multiprocessing as mp
from time import sleep
from xMove import xMove
from yMove import yMove
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

        sleep(0.5)

    def x_axis_reset(self):
        """Responsible for resetting the x axis."""
        GPIO.setwarnings(False)
        GPIO.cleanup()

        DIR_1 = int(os.getenv("MOTOR_X_Direction"))  # DIR+
        STEP_1 = int(os.getenv("MOTOR_X_Pulse"))  # PULL+

        # 0/1 used to signify clockwise or counterclockwise.
        CW = 0
        CCW = 1

        MAX = 10000

        motor1_flag = 0
        motor2_flag = 0

        GPIO.setmode(GPIO.BCM)
        motor1_switch = int(os.getenv("limitSwitchX_1"))
        motor2_switch = int(os.getenv("limitSwitchX_2"))

        GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(motor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Establish Pins in software
        GPIO.setup(DIR_1, GPIO.OUT)
        GPIO.setup(STEP_1, GPIO.OUT)

        # Set the first direction
        GPIO.output(DIR_1, CCW)

        # !!!Not Calling LimitSwitches Class!!!#

        try:
            while 1:

                for x in range(MAX):

                    GPIO.output(STEP_1, GPIO.HIGH)
                    # .5 == super slow
                    # .00005 == breaking
                    sleep(0.0005)  # Dictates how fast stepper motor will run
                    GPIO.output(STEP_1, GPIO.LOW)
                    sleep(0.0005)

                    if GPIO.input(motor2_switch) == 0:
                        motor2_flag += 1
                    elif GPIO.input(motor1_switch) == 0:
                        motor1_flag += 1
                    else:
                        motor2_flag = 0
                        motor1_flag = 0

                    if motor2_flag >= 5:
                        self.logger.logInfo("X Homing Successful")
                        sleep(1)
                        return True

                    elif motor1_flag >= 5:
                        self.logger.logInfo("X Homing Successful")
                        sleep(1)
                        return True

        # Once finished clean everything up
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False

    def y_axis_reset(self):
        """Responsible for resetting the y axis."""
        GPIO.setwarnings(False)
        GPIO.cleanup()

        DIR_1 = int(os.getenv("MOTOR_Y_Direction"))  # DIR+
        STEP_1 = int(os.getenv("MOTOR_Y_Pulse"))  # PULL+

        # 0/1 used to signify clockwise or counterclockwise.
        CW = 0
        CCW = 1

        MAX = 10000

        motor1_flag = 0
        motor2_flag = 0

        GPIO.setmode(GPIO.BCM)
        motor1_switch = int(os.getenv("limitSwitchY_1"))
        motor2_switch = int(os.getenv("limitSwitchY_2"))
        GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(motor2_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Establish Pins in software
        GPIO.setup(DIR_1, GPIO.OUT)
        GPIO.setup(STEP_1, GPIO.OUT)

        # Set the first direction
        GPIO.output(DIR_1, CCW)

        try:

            while 1:

                for x in range(MAX):

                    GPIO.output(STEP_1, GPIO.HIGH)
                    # Allow it to get there.
                    # .5 == super slow
                    sleep(0.0005)  # Dictates how fast stepper motor will run
                    GPIO.output(STEP_1, GPIO.LOW)

                    sleep(0.0005)

                    if GPIO.input(motor2_switch) == 0:
                        motor2_flag += 1
                    elif GPIO.input(motor1_switch) == 0:
                        motor1_flag += 1
                    else:
                        motor2_flag = 0
                        motor1_flag = 0

                    if motor2_flag >= 5:
                        self.logger.logInfo("Y Homing Successful")
                        sleep(1)
                        return True

                    elif motor1_flag >= 5:
                        self.logger.logInfo("Y Homing Successful")
                        sleep(1)
                        return True

        # Once finished clean everything up

        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False
    
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
        self.x_axis_reset()
        try:
            xMove(14)
            sleep(1)
            return True
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False

    def y_axis_mid(self):
        self.y_axis_reset()
        try:
            yMove(9.5)
            sleep(1)
            return True
        except Exception as e:
            self.logger.logError("Failure {}".format(e))
            GPIO.cleanup()
            return False
        
    def xy_axis_mid(self):
        self.xy_reset()
        try:
            xyMove.xyMove(14, 9.5)
            sleep(1)
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
