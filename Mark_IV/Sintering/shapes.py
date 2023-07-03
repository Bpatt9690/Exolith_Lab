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
focal_diameter = 0.8

def box2d(x_dist=7, y_dist=5):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_lines = int(y_dist / focal_diameter)

    clockwise = True
    #CW Away from limit switch
    try:
        # Make box with given number of lines.
        for i in range(num_lines):
            xMove(x_dist, clockwise)
            if i == num_lines - 1:
                break

            yMove(focal_diameter, True)
            clockwise = not(clockwise)


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()
    

def box3d(x_dist=14, y_dist=8, z_dist=8):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_y_lines = int(round(y_dist / focal_diameter, 0))
    num_z_lines = int(round(z_dist / focal_diameter, 0))

    x_rotation = True
    y_rotation = True
    #CW Away from limit switch
    try:
        for i in range(num_z_lines):
            # Make box with given number of lines.
            for j in range(num_y_lines):
                # Makes layer of box.
                xMove(x_dist, x_rotation)
                x_rotation = not(x_rotation)

                # When on last line of layer, keep tray still and start at that same point on the next layer.
                if j == num_y_lines - 1:
                    break
                yMove(focal_diameter, y_rotation)

            # When of last layer, don't move tray down anymore.
            if i == num_z_lines - 1:
                break
            zMove(focal_diameter, True) 
            y_rotation = not(y_rotation)


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


def cylinder(radius=6, height=6):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(height / focal_diameter, 0))
    start_out = True

    try:
        for i in range(num_layers):
            # Traces filled-in circle.
            circle(radius, start_out)

            if i == num_layers - 1:
                break
            
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(focal_diameter, True)
            start_out = not(start_out)
            
    # Once finished clean everything up.
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def hexagonal_prism(width=5, height=5):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round(height / focal_diameter, 0))
    start_out = True

    try:
        for i in range(num_layers):
            # Traces filled-in hexagon.
            hexagon(width, start_out)

            if i == num_layers - 1:
                break
            
            # Moves to start next layer.
            # True moves linear actuator forward.
            zMove(focal_diameter, True)
            start_out = not(start_out)
            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def semi_sphere(radius=6):
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
            zMove(focal_diameter, True)
            start_out = not(start_out)

            # Makes next circle smaller.
            radius -= focal_diameter
            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def bowl(radius=6):
    # Thickness defines how many layers thick the bowl will be.
    thickness = 2
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
            zMove(focal_diameter, True)
            
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
            circle(radius=3, start_out=False)
        if sys.argv[1].lower() == "box2d":
            box2d(x_dist=3, y_dist=3)
    else:
        box2d(x_dist=3, y_dist=3)


if __name__ == "__main__":
    main()