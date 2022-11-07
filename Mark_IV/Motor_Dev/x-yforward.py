import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches

ls = limitSwitches()


def Movement():
    # Direction pin from controller
    GPIO.cleanup()
    xDIR_1 = 6 #DIR+
    xDIR_2 = 22 #DIR+
    # Step pin from controller
    xSTEP_1 = 5 #PULL+
    xSTEP_2 = 23 #PULL+
    yDIR_1 = 19 #DIR+
    yDIR_2 = 25 #DIR+
    # Step pin from controller
    ySTEP_1 = 20 #PULL+
    ySTEP_2 = 24 #PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 10000
    flag = 0

    GPIO.setmode(GPIO.BCM)
    xmotor1_switch=27
    xmotor2_switch=21
    ymotor1_switch=18
    ymotor2_switch=12
    GPIO.setup(xmotor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(xmotor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ymotor1_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)    
    GPIO.setup(ymotor2_switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)



    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(xDIR_1, GPIO.OUT)
    GPIO.setup(xSTEP_1, GPIO.OUT)
    GPIO.setup(xDIR_2, GPIO.OUT)
    GPIO.setup(xSTEP_2, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(xDIR_1, CW)
    GPIO.output(xDIR_2, CW)


    GPIO.setup(yDIR_1, GPIO.OUT)
    GPIO.setup(ySTEP_1, GPIO.OUT)
    GPIO.setup(yDIR_2, GPIO.OUT)
    GPIO.setup(ySTEP_2, GPIO.OUT)

    # Set the first direction you want it to spin
    GPIO.output(yDIR_1, CW)
    GPIO.output(yDIR_2, CW)

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
                GPIO.output(xSTEP_1,GPIO.HIGH)
                GPIO.output(xSTEP_2,GPIO.HIGH)
                GPIO.output(ySTEP_1,GPIO.HIGH)
                GPIO.output(ySTEP_2,GPIO.HIGH)
                # Allow it to get there.
                #.5 == super slow
                # .00005 == breaking
                sleep(.005) # Dictates how fast stepper motor will run
                # Set coil winding to low
                GPIO.output(xSTEP_1,GPIO.LOW)
                GPIO.output(xSTEP_2,GPIO.LOW)
                GPIO.output(ySTEP_1,GPIO.LOW)
                GPIO.output(ySTEP_2,GPIO.LOW)
                sleep(.005) # Dictates how fast stepper motor will run


                


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    Movement()


if __name__ == '__main__':
    main()