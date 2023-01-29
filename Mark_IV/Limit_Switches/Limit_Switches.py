import RPi.GPIO as GPIO
from time import sleep


class limitSwitches:
    def __init__(self):
        pass

    def limitLogic(self, switch):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.OUT)
        GPIO.output(switch, GPIO.HIGH)
        flag = 0

        try:

            while 1:

                if GPIO.input(switch) == 0:
                    flag += 1

                else:
                    flag = 0

                if flag > 5:
                    return True

                sleep(0.05)

        except KeyboardInterrupt:
            print("GPIO Cleanup")
            GPIO.cleanup()

    def motorx1(self):
        return self.limitLogic(27)

    def motorx2(self):
        return self.limitLogic(21)

    def motory1(self):
        return self.limitLogic(18)

    def motory2(self):
        return self.limitLogic(12)

    def elevation(self):
        return self.limitLogic(17)
