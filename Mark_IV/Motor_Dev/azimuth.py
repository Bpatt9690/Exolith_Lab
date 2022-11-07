import RPi.GPIO as GPIO
from time import sleep

'''
Used to test the azimuth motor WITHOUT compass data to compare against.
'''

def azimuth():
    # Direction pin from controller
    GPIO.cleanup()
    DIR_1 = #CHANGE #DIR+
    # Step pin from controller
    STEP_1 = #CHANGE #PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000

    GPIO.setmode(GPIO.BCM)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CW)

    try:
        
        while(1):

            # Run for 200 steps. This will change based on how you set you controller
            for x in range(MAX):

                # Set one coil winding to high
                GPIO.output(STEP_1,GPIO.HIGH)
                #.5 == super slow
                # .00005 == breaking
                sleep(.0005) # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(STEP_1,GPIO.LOW)
                sleep(.0005) # Dictates how fast stepper motor will run

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()

def main():
    azimuth()

if __name__ == '__main__':
    main()