import RPi.GPIO as GPIO
from time import sleep

from time import sleep
from Limit_Switches import limitSwitches

ls = limitSwitches()


def xMovement():
    # Direction pin from controller
    GPIO.cleanup()
    DIR_1 = 19 #DIR+
    DIR_2 = 25 #DIR+
    # Step pin from controller
    STEP_1 = 20 #PULL+
    STEP_2 = 24 #PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    flag = 0

    GPIO.setmode(GPIO.BCM)
    motor1_switch=18
    motor2_switch=12
    GPIO.setup(motor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(motor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)



    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)
    GPIO.setup(DIR_2, GPIO.OUT)
    GPIO.setup(STEP_2, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CW)
    GPIO.output(DIR_2, CW)
    #CW Away from limit switch
    try:
        # Run forever.
        while(1):

            """Change Direction: Changing direction requires time to switch. The
            time is dictated by the stepper motor and controller. """
            #sleep()
            # Esablish the direction you want to go
            #GPIO.output(DIR_1,CCW)
            #GPIO.output(DIR_2,CCW)

            # Run for 200 steps. This will change based on how you set you controller
            for x in range(MAX):

                # Set one coil winding to high
                GPIO.output(STEP_1,GPIO.HIGH)
                GPIO.output(STEP_2,GPIO.HIGH)
                # Allow it to get there.
                #.5 == super slow
                # .00005 == breaking
                sleep(.005) # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(STEP_1,GPIO.LOW)
                GPIO.output(STEP_2,GPIO.LOW)
                sleep(.005) # Dictates how fast stepper motor will run

                
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    xMovement()


if __name__ == '__main__':
    main()

