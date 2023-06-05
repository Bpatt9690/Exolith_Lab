import RPi.GPIO as GPIO
from xMove import xMove
from yMove import yMove
from zMove import zMove
from axisReset import axis_reset

'''
Moves x and y to trace a box as if sintering.
'''

def trace_box(x_dist=14, y_dist=8, z_dist=8):
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


def main():
    trace_box()
    GPIO.cleanup()

if __name__ == '__main__':
    main()