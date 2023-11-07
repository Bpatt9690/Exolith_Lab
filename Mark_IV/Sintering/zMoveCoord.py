import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches
import time
from dotenv import load_dotenv
import os
import sys
from azimuthTracking import azimuth_tracker

# Load environment variables from .env file
load_dotenv()

"""
Moves motor for Z axis. Currently CCW || 1 moves the z axis down
"""

ls = limitSwitches()

def zMoveCoord(coord=2, speed_mod=0.3):
    GPIO.setwarnings(False)

    if speed_mod > 0.5:
        print("Speed modifier above 0.5 , z motor cannot go above max speed.")
        exit()

    if speed_mod < 0.001:
        return
    
    if coord < 0:
        print("Coordinate less than 0, set to 0")
        coord = 0

    # Direction pin from controller
    DIR = int(os.getenv("MOTOR_Z_Direction"))  # DIR+
    STEP = int(os.getenv("MOTOR_Z_Pulse"))  # PULL+

    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    Z_MAX = 10.6
    motor_flag_top = 0
    z_coord = 0.0
    z_file_name = "z_coord.txt"
    os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")

    # Based on distance traveled each step of the motor.
    increment = 0.001

    GPIO.setmode(GPIO.BCM)
    motor1_switch = int(os.getenv("limitSwitchZ_1"))
    GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    #CW Away from limit switch
    try:
        if(os.path.exists(z_file_name)) and os.stat(z_file_name).st_size != 0:
            with open(z_file_name, "r") as f:
                z_coord = float(f.readline())
        else:
            with open(z_file_name, "w") as f:
                f.write("0\n")
        distance = abs(coord - z_coord)
        
        # Set the first direction you want it to spin
        if coord > z_coord and distance > increment / 2:
            GPIO.output(DIR, CCW)
        elif coord < z_coord and distance > increment / 2:
            GPIO.output(DIR, CW)
            increment *= -1
        else:
            with open(z_file_name, "w") as f:   
                f.write(str(z_coord) + "\n")
            print("y: " + str(z_coord))
            return
        
        num_steps = int(round(distance / abs(increment), 0))
        
        f = open(z_file_name, "w")
        # # Run for 200 steps. This will change based on how you set you controller
        for x in range(num_steps):
            if z_coord + increment > Z_MAX and increment > 0:
                print("Y Coordinate out of bounds")
                return
            
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            #.5 == super slow
            # .00005 == breaking
            sleep(.001 / speed_mod) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.001 / speed_mod) # Dictates how fast stepper motor will run

            z_coord += increment
            f.write(str(z_coord) + "\n")
            f.seek(0)

            if GPIO.input(motor1_switch) == 0 and increment < 0:
                motor_flag_top += 1
            else:
                motor_flag_top = 0

            if motor_flag_top >= 5:
                z_coord = 0
                f.close()
                with open(z_file_name, "w") as f:
                    f.write(str(z_coord) + "\n")
                break
        f.close()
        print("z: " + str(z_coord))
        GPIO.cleanup()

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        f.close()
        GPIO.cleanup()


def main():
    num_args = len(sys.argv)
    if num_args == 2:
        zMoveCoord(float(sys.argv[1]))
    elif num_args == 3:
        zMoveCoord(float(sys.argv[1]), float(int(sys.argv[2])))
    else:
        zMoveCoord()
    
if __name__ == '__main__':
    main()