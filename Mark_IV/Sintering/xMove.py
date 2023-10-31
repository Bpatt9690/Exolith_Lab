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
Moves both motor 1 and motor 2 of the X axis. Currently CW || 0 moves the x axis forward
"""

ls = limitSwitches()

def xMove(distance=10, clockwise=True, speed_mod=0.6, pause=False):
    GPIO.setwarnings(False)

    if speed_mod > 1:
        print("Speed mod too large, set to 1")
        speed_mod = 1

    if speed_mod < 0.001:
        return
    
    if distance == 0:
        return

    # Direction pin from controller
    DIR = int(os.getenv("MOTOR_X_Direction"))  # DIR+
    STEP = int(os.getenv("MOTOR_X_Pulse"))  # PULL+
    uvMin = float(os.getenv("uvMin"))
    useGPS = os.getenv("useGPS")

    # Max x coordinate in cm
    X_MAX = 32

    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    motor_flag = 0
    x_coord = 0.0
    x_file_name = "x_coord.txt"
    uv_file_name = "uv_current.txt"
    os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")

    # Based on distance traveled each step of the motor in cm.
    increment = 0.000635

    GPIO.setmode(GPIO.BCM)
    motor1_switch = int(os.getenv("limitSwitchX_1"))
    GPIO.setup(motor1_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Establish Pins in software
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

    # Set the first direction you want it to spin
    if clockwise == True:
        GPIO.output(DIR, CW)
    else:
        GPIO.output(DIR, CCW)
        increment *= -1

    #CW Away from limit switch
    try:
        if(os.path.exists(x_file_name)) and os.stat(x_file_name).st_size != 0:
            with open(x_file_name, "r") as f:
                x_coord = float(f.readline())
        else:
            with open(x_file_name, "w") as f:
                f.write("0\n")
        num_steps = int(round(distance / 0.000635, 0))
        
        f = open(x_file_name, "w")
        f.write(str(x_coord) + "\n")
        f.seek(0)
        uv_file = open(uv_file_name, "r+")
        # # Run for 200 steps. This will change based on how you set you controller
        for x in range(num_steps):
            if pause and useGPS == "True":
                if x % 50 == 0:
                    uvVal = uv_file.readline()
                    if uvVal != "":
                        uvVal = float(uvVal)
                    else:
                        uvVal = uvVal = uvMin
                    uv_file.seek(0)

                while(uvVal < uvMin):
                    time.sleep(0.01)
                    uvVal = uv_file.readline()
                    if uvVal != "":
                        uvVal = float(uvVal)
                    else:
                        uvVal = 0
                    uv_file.seek(0)

            if x_coord + increment > X_MAX and clockwise:
                print("X Coordinate out of bounds")
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

            x_coord += increment
            f.write(str(x_coord) + "\n")
            f.seek(0)

            if GPIO.input(motor1_switch) == 0 and clockwise == False:
                motor_flag += 1
            else:
                motor_flag = 0

            if motor_flag >= 5:
                x_coord = 0.0
                f.close()
                with open(x_file_name, "w") as f:
                    f.write(str(x_coord) + "\n")
                break
        f.close()
        print("x: " + str(x_coord))
        GPIO.cleanup()

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        f.close()
        GPIO.cleanup()


def main():
    num_args = len(sys.argv)
    if num_args == 2:
        xMove(float(sys.argv[1]))
    elif num_args == 3:
        xMove(float(sys.argv[1]), bool(int(sys.argv[2])))
    elif num_args == 4:
        xMove(float(sys.argv[1]), bool(sys.argv[2]), float(sys.argv[3]))
    else:
        xMove()
    
if __name__ == '__main__':
    main()