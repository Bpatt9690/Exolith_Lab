#prod ready

import RPi.GPIO as GPIO
from time import sleep
import time
import SI1145.SI1145 as SI1145


sensor = SI1145.SI1145()


def stepMovement(direction,steps):
    GPIO.setwarnings(False) 
    # Direction pin from controller
    GPIO.cleanup()
    DIR_1 = 13 #DIR+

    # Step pin from controller
    STEP_1 = 26 #PULL+

    # 0/1 used to signify clockwise or counterclockwise.
    CW = direction

    if direction is 1:
        CCW = 0
    else:
        CCW = 1

    MAX = 100

    GPIO.setmode(GPIO.BCM)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CW)

    try:

        for x in range(steps):
            print('Adjusting....')
 
            GPIO.output(STEP_1,GPIO.HIGH)
            #.5 == super slow
            # .00005 == breaking
            sleep(.5) 
            GPIO.output(STEP_1,GPIO.LOW)
            sleep(.5)

        #rotate opposite way; used as break
        GPIO.output(DIR_1, CCW)

        GPIO.output(STEP_1,GPIO.HIGH)
        sleep(.5)
        GPIO.output(STEP_1,GPIO.LOW)
        sleep(.5)


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()



def uv_sensor():
    global sensor
    uvAverage = 0
    for i in range(10):
            UV = sensor.readUV()
            uvIndex = UV
            uvAverage += uvIndex
            time.sleep(.1)
    return (uvAverage/10)
    
def main():

    uv_current = uv_sensor()
    print('Stationary UV value: ', uv_current)

    uv_high = uv_current
    uv_low = uv_current 

    while(1):

        #move clockwise
        stepMovement(1,2)
        uv = uv_sensor()

        if uv > uv_high:
            uv_low = uv_high
            uv_high = uv

        print("UV High: ", uv_high)
        print("UV Low: ", uv_low) 

        if uv_high > uv:
            uv_max = uv_high
            print('We need to pause')
            stepMovement(0,2)


            break
    print('current uv:',uv_sensor())
    print('uv high', uv_high)

if __name__ == '__main__':
    main()