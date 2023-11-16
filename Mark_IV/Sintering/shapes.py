import RPi.GPIO as GPIO
import sys
import os
from xMove import xMove
from yMove import yMove
from Sintering.zMoveDeprecated import zMove
from xyMove import xyMove
from xy_curve import xyCurve
from xyMoveCoord import xyMoveCoord
from xyCircleFill import xyCircleFill
from math import sqrt
from axisReset import axis_reset

ar = axis_reset()

os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")
x_file_name = "x_coord.txt"
y_file_name = "y_coord.txt"
pause_file_name = "pause.txt"

# Defines the diameter of the focal point in cm.
layer_height = 0.3
focal_diameter = 0.7

# For sintering use 0.1 as default
speed = 0.1

def box2d(x_dist=3, y_dist=3, flip=False, x_prev_dir=True, y_prev_dir=True, speed_mod=0.1):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    if flip:
        num_lines = int(round(x_dist / focal_diameter, 0))
        y_dist = int(round(y_dist / focal_diameter - 1, 0)) * focal_diameter
    else:
        num_lines = int(round(y_dist / focal_diameter, 0))
        x_dist = int(round(x_dist / focal_diameter - 1, 0)) * focal_diameter

    # No rounding, replaces for slight overlap.
    # if flip:
    #     num_lines = ceil(x_dist / focal_diameter)
    #     y_dist -= focal_diameter
    #     x_dist = (x_dist - focal_diameter) / (num_lines - 1)
    # else:
    #     num_lines = ceil(x_dist / focal_diameter)
    #     x_dist -= focal_diameter
    #     y_dist = (y_dist - focal_diameter) / (num_lines - 1)

    #CW Away from limit switch
    try:
        # Make box with given number of lines.
        if(flip):
            for i in range(num_lines):
                yMove(y_dist, y_prev_dir, speed_mod, pause=True)
                y_prev_dir = not(y_prev_dir)
                if i == num_lines - 1:
                    break
                
                xMove(focal_diameter, x_prev_dir, speed_mod, pause=True)
                # xMove(x_dist, x_prev_dir, speed, pause=True)
            x_prev_dir = not(x_prev_dir)
        else:
            for i in range(num_lines):
                xMove(x_dist, x_prev_dir, speed_mod, pause=True)
                x_prev_dir = not(x_prev_dir)
                if i == num_lines - 1:
                    break

                yMove(focal_diameter, y_prev_dir, speed_mod, pause=True)
                # yMove(y_dist, y_prev_dir, speed, pause=True)
            y_prev_dir = not(y_prev_dir)
        return (x_prev_dir, y_prev_dir)
                


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()
    

def box3d(x_dist=4, y_dist=4, z_dist=4):
    x_prev_dir = True
    y_prev_dir = True
    pause = "1"
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_z_lines = int(round(z_dist / layer_height, 0))

    flip = False
    #CW Away from limit switch
    with open(pause_file_name, "w") as f:
        f.write("1")
    try:
        for i in range(num_z_lines):
            # Make box of given size, but flip orientation 90 degrees every layer to increase strength of brick.
            x_prev_dir, y_prev_dir = box2d(x_dist, y_dist, flip, x_prev_dir, y_prev_dir)

            # When of last layer, don't move tray down anymore.
            if i == num_z_lines - 1:
                break
            zMove(layer_height, False)
            flip = not(flip)
            while(pause != "0"):
                with open(pause_file_name, "r") as f:
                    pause = f.readline()
            with open(pause_file_name, "w") as f:
                pause = "1"
                f.write("1")

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def circle(radius=2, flip=False):
    try:
        if not(flip):
            xyCurve(0, 0, 0, radius, True, speed_mod=speed, pause=True)
        else:
            xyCurve(0, 0, radius, 0, True, speed_mod=speed, pause=True)
        xyCircleFill(radius, speed_mod=speed, flip=flip)

    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def hexagon(width=3, start_out=False):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round((width) / (2 * focal_diameter), 0))

    # Start on the outside or center of filled-in hexagon.
    if start_out:
        width = focal_diameter * (num_layers - 0.5) * 2
    else:
        width = focal_diameter

    try:
        for i in range(num_layers):
            side = width / 4
            # Traces hexagon outline (in xy)
            xMove(side, True, speed_mod=speed, pause=True)
            xyMove(side, side * sqrt(3), speed=speed, pause=True)
            xyMove(side * -1, side * sqrt(3), speed=speed, pause=True)
            xMove(side * 2, False, speed_mod=speed, pause=True)
            xyMove(side * -1, side * sqrt(3) * -1, speed=speed, pause=True)
            xyMove(side, side * sqrt(3) * -1, speed=speed, pause=True)
            xMove(side, True, speed_mod=speed, pause=True)

            if i == num_layers - 1:
                break
            
            # Moves to start next hexagon, depending on if that hexagon is starting on inside or outside.
            if start_out:
                yMove(focal_diameter, True, speed_mod=speed, pause=True)
                width = width - focal_diameter * 2
            else:
                yMove(focal_diameter, False, speed_mod=speed, pause=True)
                width = width + focal_diameter * 2
        
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def cylinder(radius=2, height=3):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(height / layer_height, 0))
    flip = False
    pause = "1"
    x_coord = 0
    y_coord = 0

    if(os.path.exists(x_file_name)) and os.stat(x_file_name).st_size != 0:
        with open(x_file_name, "r") as f:
            x_coord = float(f.readline())
    else:
        with open(x_file_name, "w") as f:
            f.write("0\n")
    if(os.path.exists(y_file_name)) and os.stat(y_file_name).st_size != 0:
        with open(y_file_name, "r") as f:
            y_coord = float(f.readline())
    else:
        with open(y_file_name, "w") as f:
            f.write("0\n")

    try:
        with open(pause_file_name, "w") as f:
            f.write("1")
        for i in range(num_layers):
            # Traces filled-in circle.
            circle(radius, flip)
            flip = not(flip)

            if i == num_layers - 1:
                break
            
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(layer_height, False)
            if flip:
                x_coord -= radius
                y_coord += radius
            if not(flip):
                x_coord += radius
                y_coord -= radius
            xyMoveCoord(x_coord, y_coord, speed_mod=0.5)
            
            while(pause != "0"):
                with open(pause_file_name, "r") as f:
                    pause = f.readline()
            with open(pause_file_name, "w") as f:
                pause = "1"
                f.write("1")
            
    # Once finished clean everything up.
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def hexagonal_prism(width=5, height=5):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(height / layer_height, 0))
    start_out = True
    pause = "1"

    try:
        with open(pause_file_name, "w") as f:
            f.write("1")
        for i in range(num_layers):
            # Traces filled-in hexagon.
            hexagon(width, start_out)

            if i == num_layers - 1:
                break
            
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(layer_height, False)
            start_out = not(start_out)
            while(pause != "0"):
                with open(pause_file_name, "r") as f:
                    pause = f.readline()
            with open(pause_file_name, "w") as f:
                pause = "1"
                f.write("1")
            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def semi_sphere(radius=4):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(radius / focal_diameter, 0))
    start_out = True

    try:
        for i in range(num_layers):
            # Traces filled-in circle.
            circle(radius, start_out)

            if i == num_layers - 1:
                break
            
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(layer_height, False)
            start_out = not(start_out)

            # Makes next circle smaller.
            radius -= focal_diameter

            if start_out:
                yMove(focal_diameter, True, pause=True)
            input("Press Enter to move to start of next layer")
            

            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def bowl(radius=4):
    # Thickness defines how many layers thick the bowl will be.
    thickness = 3
    num_layers = int(round(radius / focal_diameter, 0))

    # True moves linear actuator forward.
    try:
        for i in range(num_layers):
            for j in range(thickness):
                # Traces circle outline, makes bowl with given number of circles as thickness.
                xyCurve(0, 0, 0, radius, speed_mod=0.1, pause=True)

                if j == thickness - 1:
                    break
                
                # Moves to start next layer.
                yMove(focal_diameter, True, pause=True)
                # Makes next circle smaller.
                radius -= focal_diameter
            
            if i == num_layers - 1:
                break
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(layer_height, False)
            yMove(focal_diameter * (thickness - 1), False, pause=True)
            radius += focal_diameter * (thickness - 1)
            input("Press Enter to continue next layer")
            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    num_args = len(sys.argv)
    if num_args > 1:
        if sys.argv[1].lower() == "hexagon":
            hexagon(width=3, start_out=True)
        if sys.argv[1].lower() == "circle":
            circle(radius=2, start_out=True)
        if sys.argv[1].lower() == "box2d":
            box2d(x_dist=3, y_dist=3)
        if sys.argv[1].lower() == "cylinder":
            if num_args > 3:
                cylinder(float(sys.argv[2]), float(sys.argv[3]))
            else:
                cylinder(radius=2, height=2)
        if sys.argv[1].lower() == "box3d":
            if num_args > 4:
                box3d(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
            else:
                box3d(x_dist=3, y_dist=3, z_dist=3)
    else:
        box3d(x_dist=3, y_dist=3, z_dist=3)
        # cylinder(radius=2, height=2)
        # hexagonal_prism(width=3, height=3)
        # semi_sphere(radius=2)
        # bowl(radius=4.5)


if __name__ == "__main__":
    main()