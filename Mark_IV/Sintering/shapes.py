import RPi.GPIO as GPIO
from xMove import xMove
from yMove import yMove
from xyMove import xyMove
from xy_curve import xyCurve
from math import sqrt
from axisReset import axis_reset

# Defines the diameter of the focal point in cm.
focal_diameter = 1

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


def hexagon(width=5, start_out=True):
    # Rounds the dimensions to the nearest multiple of the focal point's diameter.
    num_layers = int(round((width) / (2 * focal_diameter), 0))

    # Start on the outside or center of filled-in hexagon.
    if start_out:
        width = focal_diameter * (num_layers - 0.5) * 2
    else:
        width = focal_diameter
    side = width / 4

    try:
        for i in range(num_layers):
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
                side -= focal_diameter / 2
            else:
                yMove(focal_diameter, False)
                side += focal_diameter / 2
        
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    # hexagon(width=8, start_out=False)
    # circle(radius=4, start_out=False)
    box2d()


if __name__ == "__main__":
    main()