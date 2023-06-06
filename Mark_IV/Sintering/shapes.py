import RPi.GPIO as GPIO
from xMove import xMove
from yMove import yMove
from zMove import zMove
from xy_curve import xyCurve
from axisReset import axis_reset

def box2d(x_dist=7, y_dist=5):
    GPIO.cleanup()
    ar = axis_reset()
    ar.x_axis_reset()
    ar.y_axis_reset()

    # Direction pin from controller
    focal_diameter = 1
    num_lines = int(y_dist / focal_diameter)

    clockwise = True
    #CW Away from limit switch
    try:
        # Make box with given number of lines.
        for _ in range(num_lines):
            xMove(x_dist, clockwise)
            yMove(focal_diameter, True)
            clockwise = not(clockwise)


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()
    

def box3d(x_dist=14, y_dist=8, z_dist=8):
    GPIO.cleanup()
    ar = axis_reset()
    ar.x_axis_reset()
    ar.y_axis_reset()

    # Direction pin from controller
    focal_diameter = 1
    num_y_lines = int(round(y_dist / focal_diameter, 0))
    num_z_lines = int(round(z_dist / focal_diameter, 0))

    x_rotation = True
    y_rotation = True
    #CW Away from limit switch
    try:
        for i in range(num_z_lines):
            # Make box with given number of lines.
            for _ in range(num_y_lines):
                xMove(x_dist, x_rotation)
                yMove(focal_diameter, y_rotation)
                x_rotation = not(x_rotation)
            zMove(focal_diameter, True) 
            y_rotation = not(y_rotation)


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def circle(radius=3, start_out=True):
    GPIO.cleanup()

    # Diameter of focal point in cm.
    focal_diameter = 1
    num_layers = int(round(radius / focal_diameter, 0))
    if start_out:
        radius = focal_diameter * (num_layers - 0.5)
    else:
        radius = focal_diameter / 2

    try:
        for i in range(num_layers):
            xyCurve(0, 0, 0, radius, True)

            if i == num_layers - 1:
                break
            if start_out:
                yMove(focal_diameter, True)
                radius -= focal_diameter
            else:
                yMove(focal_diameter, False)
                radius += focal_diameter

    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def cylinder(radius=6, height=6):
    GPIO.cleanup()

    # Direction pin from controller
    focal_diameter = 1
    num_layers = int(round(height / focal_diameter, 0))
    start_out = True

    # True moves linear actuator forward.
    try:
        for i in range(num_layers):
            circle(radius, start_out)

            if i == num_layers - 1:
                break
            
            zMove(focal_diameter, True)
            start_out = not(start_out)
            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def bowl(radius=6, height=6):
    GPIO.cleanup()

    # Direction pin from controller
    focal_diameter = 1
    num_layers = int(round(height / focal_diameter, 0))
    start_out = True

    # True moves linear actuator forward.
    try:
        for i in range(num_layers):
            circle(radius, start_out)

            if i == num_layers - 1:
                break
            
            zMove(focal_diameter, True)
            start_out = not(start_out)
            radius -= focal_diameter
            
    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    box2d()

if __name__ == "__main__":
    main()