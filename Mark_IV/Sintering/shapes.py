import RPi.GPIO as GPIO
import sys
from xMove import xMove
from yMove import yMove
from zMove import zMove
from xyMove import xyMove
from xy_curve import xyCurve
from math import sqrt
from axisReset import axis_reset

ar = axis_reset()

# Defines the diameter of the focal point in cm.
layer_height = 0.4
focal_diameter = 0.7

def box2d(x_dist=7, y_dist=5, flip=False, x_prev_dir=False, y_prev_dir=True):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    if flip:
        num_lines = int(round(x_dist / focal_diameter, 0))
        y_dist = int(round(y_dist / focal_diameter, 0)) * focal_diameter
    else:
        num_lines = int(round(y_dist / focal_diameter, 0))
        x_dist = int(round(x_dist / focal_diameter, 0)) * focal_diameter
    #CW Away from limit switch
    try:
        # Make box with given number of lines.
        if(flip):
            for i in range(num_lines):
                yMove(y_dist, y_prev_dir)
                y_prev_dir = not(y_prev_dir)
                if i == num_lines - 1:
                    break
                
                xMove(focal_diameter, x_prev_dir)
            x_prev_dir = not(x_prev_dir)
        else:
            for i in range(num_lines):
                xMove(x_dist, x_prev_dir)
                x_prev_dir = not(x_prev_dir)
                if i == num_lines - 1:
                    break

                yMove(focal_diameter, y_prev_dir)
            y_prev_dir = not(y_prev_dir)
        return (x_prev_dir, y_prev_dir)
                


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()
    

def box3d(x_dist=2, y_dist=3, z_dist=2):
    x_prev_dir = True
    y_prev_dir = True
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_z_lines = int(round(z_dist / layer_height, 0))

    flip = False
    #CW Away from limit switch
    try:
        for i in range(num_z_lines):
            # Make box of given size, but flip orientation 90 degrees every layer to increase strength of brick.
            x_prev_dir, y_prev_dir = box2d(x_dist, y_dist, flip, x_prev_dir, y_prev_dir)

            # When of last layer, don't move tray down anymore.
            if i == num_z_lines - 1:
                break
            zMove(layer_height, False) 
            flip = not(flip)
            input("Press Enter to continue next layer")

    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def circle(radius=3, start_out=True):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(radius / focal_diameter, 0))

    # Start on the outside or center of filled-in circle.
    if start_out:
        radius = focal_diameter * (num_layers - 0.5)
    else:
        radius = focal_diameter / 2

    try:
        for i in range(num_layers):
            # Draw circle outline
            xyCurve(0, 0, 0, radius, True)

            if i == num_layers - 1:
                break

            # Make next circle smaller if starting on outside of circle.
            # Make next circle larger if starting on inside of circle.
            if start_out:
                yMove(focal_diameter, True)
                radius -= focal_diameter
            else:
                yMove(focal_diameter, False)
                radius += focal_diameter

    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def hexagon(width=5, start_out=False):
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
            xMove(side, True)
            xyMove(side, side * sqrt(3))
            xyMove(side * -1, side * sqrt(3))
            xMove(side * 2, False)
            xyMove(side * -1, side * sqrt(3) * -1)
            xyMove(side, side * sqrt(3) * -1)
            xMove(side, True)

            if i == num_layers - 1:
                break
            
            # Moves to start next hexagon, depending on if that hexagon is starting on inside or outside.
            if start_out:
                yMove(focal_diameter, True)
                width = width - focal_diameter * 2
            else:
                yMove(focal_diameter, False)
                width = width + focal_diameter * 2
        
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def cylinder(radius=2, height=3):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(height / layer_height, 0))
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
            input("Press Enter to continue next layer")
            
    # Once finished clean everything up.
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def hexagonal_prism(width=5, height=5):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(height / layer_height, 0))
    start_out = True

    try:
        for i in range(num_layers):
            # Traces filled-in hexagon.
            hexagon(width, start_out)

            if i == num_layers - 1:
                break
            
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(layer_height, False)
            start_out = not(start_out)
            input("Press Enter to continue next layer")
            
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
                yMove(focal_diameter, True)
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
                xyCurve(0, 0, 0, radius)

                if j == thickness - 1:
                    break
                
                # Moves to start next layer.
                yMove(focal_diameter, True)
                # Makes next circle smaller.
                radius -= focal_diameter
            
            if i == num_layers - 1:
                break  
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(layer_height, False)
            yMove(focal_diameter * (thickness - 1), False)
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
            hexagon(width=6, start_out=True)
        if sys.argv[1].lower() == "circle":
            circle(radius=3, start_out=True)
        if sys.argv[1].lower() == "box2d":
            box2d(x_dist=3, y_dist=3)
    else:
        # box3d(x_dist=3, y_dist=2, z_dist=2)
        # cylinder(radius=3, height=3)
        # hexagonal_prism(width=3, height=3)
        # semi_sphere(radius=3)
        bowl(radius=3)


if __name__ == "__main__":
    main()