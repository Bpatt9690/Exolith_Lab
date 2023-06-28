import RPi.GPIO as GPIO
from time import sleep
import time
from Logging import logger
import board
import adafruit_ltr390
from dotenv import load_dotenv
import os 

# Load environment variables from .env file
load_dotenv()

azVal = None
uvUpper = None
uvLower = None


class azimuth_tracker:
    def __init__(self):
        self.logger = logger()

    def stepMovement(self, direction, steps):
        GPIO.setwarnings(False)
        GPIO.cleanup()

        DIR_1 = int(os.getenv("AZIMUTH_Direction"))  # DIR+
        STEP_1 = int(os.getenv("AZIMUTH_Pulse"))  # PULL+

        # 0/1 used to signify clockwise or counterclockwise.
        CW = direction

        if direction is 1:
            CCW = 0
        else:
            CCW = 1

        MAX = 100

        # Setup pin layout on PI
        GPIO.setmode(GPIO.BCM)

        # Establish Pins in software
        GPIO.setup(DIR_1, GPIO.OUT)
        GPIO.setup(STEP_1, GPIO.OUT)

        # Set the first direction you want it to spin
        GPIO.output(DIR_1, CW)

        uv_current = self.uv_sensor()

        uv_high = uv_current
        uv_low = uv_current

        try:

            self.logger.logInfo("Adjusting....")

            for x in range(steps):
                for _ in range(75):
                    GPIO.output(STEP_1, GPIO.HIGH)
                    # .5 == super slow
                    # .00005 == breaking
                    sleep(0.005)
                    GPIO.output(STEP_1, GPIO.LOW)
                    sleep(0.005)

                uv = self.uv_sensor()

                if uv > uv_high:
                    uv_low = uv_high
                    uv_high = uv

                self.logger.logUV(uv_high)

        # Once finished clean everything up
        except Exception as e:
            self.logger.logInfo("Step Movement Exception: " + str(e))
            GPIO.cleanup()

    def maxValue(self):
        inputFile = open("uvsensor.txt", "r")
        num_list = [float(num) for num in inputFile.read().split()]

        counter = len(num_list)
        total = sum(num_list)

        # Your desired values
        max_val = max(num_list)
        min_val = min(num_list)

        return max_val

    def uv_sensor(self):
        i2c = board.I2C()  
        sensor = adafruit_ltr390.LTR390(i2c)

        values = []

        while 1:

            try:

                print('light')
       
                for i in range(10):
                    vis = sensor.uvi
                    values.append(vis)
                    time.sleep(0.005)
                    
                print('UV index {}'.format(sum(values)/len(values)))
                sensor.initialize()
                return (sum(values)/len(values))

            except Exception as e:
                print(e)
                pass


    def azimuthPositioning(self, uvMax):

        global uvLower
        global uvUpper

        uvUpper = uvMax + (uvMax * (0.10))
        uvLower = uvMax - (uvMax * (0.10))

        self.logger.logInfo("UV Max: " + str(uvMax))
        self.logger.logInfo("UV Upper: " + str(uvUpper))
        self.logger.logInfo("UV Lower: " + str(uvLower))

        azstatus = self.azimuthMaxPosition(0, int(os.getenv("AZIMUTH_Steps")), uvMax, uvUpper, uvLower)
        return azstatus

    def azimuthMaxPosition(self, direction, steps, uvMax, uvUpper, uvLower):
        global uvVal
        GPIO.setwarnings(False)
        GPIO.cleanup()

        DIR_1 = int(os.getenv("AZIMUTH_Direction"))  # DIR+
        STEP_1 = int(os.getenv("AZIMUTH_Pulse"))  # PULL+

        # 0/1 used to signify clockwise or counterclockwise.
        CW = direction

        if direction is 1:
            CCW = 0
        else:
            CCW = 1

        MAX = 100

        # Setup pin layout on PI
        GPIO.setmode(GPIO.BCM)

        # Establish Pins in software
        GPIO.setup(DIR_1, GPIO.OUT)
        GPIO.setup(STEP_1, GPIO.OUT)

        # Set the first direction you want it to spin
        GPIO.output(DIR_1, CW)

        uv_current = self.uv_sensor()
        self.logger.logInfo("Stationary UV value: {}".format(uv_current))

        self.logger.logInfo("UV Lower: {}".format(uvLower))
        self.logger.logInfo("UV Upper: {}".format(uvUpper))

        try:

            for x in range(steps):
                self.logger.logInfo("Azimuth Adjustment...")
                
                for _ in range(75):
                    GPIO.output(STEP_1, GPIO.HIGH)
                    # .5 == super slow
                    # .00005 == breaking
                    sleep(0.005)
                    GPIO.output(STEP_1, GPIO.LOW)
                    sleep(0.005)

                uv = self.uv_sensor()

                if uvLower <= uv:
                    uvVal = uv
                    self.logger.logInfo("Azimuth Reached,stopping here...")
                    self.stepMovement(0, 1)  # used as a brake
                    return True

            return False

        # Once finished clean everything up
        except Exception as e:
            self.logger.logInfo("Exception in track: {}".format(e))
            GPIO.cleanup()

            # simple tracking solution that relies on UV values being close

    def tracking(self):
        global uvVal
        global uvLower
        global uvUpper

        uvVal = self.uv_sensor()

        print(uvLower, uvVal, uvUpper)

        if uvLower <= uvVal:
            self.logger.logInfo("Azimuth adjustment reached...")
            return True

        else:

            self.logger.logInfo("Azimuth adjustment required...")

            GPIO.setwarnings(False)
            GPIO.cleanup()

            DIR_1 = int(os.getenv("AZIMUTH_Direction"))  # DIR+
            STEP_1 = int(os.getenv("AZIMUTH_Pulse"))  # PULL+

            # 0/1 used to signify clockwise or counterclockwise.
            CW = 1
            CCW = 0
            steps = 10  # small increment of search

            # Setup pin layout on PI
            GPIO.setmode(GPIO.BCM)

            # Establish Pins in software
            GPIO.setup(DIR_1, GPIO.OUT)
            GPIO.setup(STEP_1, GPIO.OUT)

            # Set the first direction you want it to spin
            GPIO.output(DIR_1, CW)

            try:

                for x in range(steps):
                    self.logger.logInfo("Adjusting azimuth....")

                    for _ in range(75):
                        GPIO.output(STEP_1, GPIO.HIGH)
                        # .5 == super slow
                        # .00005 == breaking
                        sleep(0.005)
                        GPIO.output(STEP_1, GPIO.LOW)
                        sleep(0.005)

                    uvVal = self.uv_sensor()

                    if uvLower <= uvVal:
                        uvUpper = uvVal + uvVal * (0.10)
                        uvLower = uvVal - (uvVal * (0.10))
                        self.logger.logInfo("Azimuth Adjusted")
                        return True

                return False

            # Once finished clean everything up
            except Exception as e:
                self.logger.logInfo("Tracking Exception: {}".format(e))
                GPIO.cleanup()


def main():
    at = azimuth_tracker()
    at.stepMovement(1, 100)

if __name__ == "__main__":
    main()