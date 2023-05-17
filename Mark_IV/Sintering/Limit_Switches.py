import RPi.GPIO as GPIO
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class limitSwitches:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def limitLogic(self, switch):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        flag = 0

        while 1:

            if GPIO.input(switch) == 0:
                flag += 1

            else:
                flag = 0

            if flag > 5:
                return True

            else:
                return False

            time.sleep(0.05)

    def motorx1(self):
        return self.limitLogic(int(os.getenv("limitSwitchX_1")))

    def motorx2(self):
        return self.limitLogic(int(os.getenv("limitSwitchX_2")))

    def motory1(self):
        return self.limitLogic(int(os.getenv("limitSwitchY_1")))

    def motory2(self):
        return self.limitLogic(int(os.getenv("limitSwitchY_2")))

    def elevation(self):
        return self.limitLogic(int(os.getenv("limitSwitchElavation")))
