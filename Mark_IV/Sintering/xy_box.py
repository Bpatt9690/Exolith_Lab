import RPi.GPIO as GPIO
from xMove import xMove
from yMove import yMove
from axisReset import axis_reset

'''
Moves x and y to trace a box as if sintering.
'''

def trace_box(x_dist=14, y_dist=9):
    GPIO.cleanup()
    ar = axis_reset()
    ar.x_axis_reset()
    ar.y_axis_reset()

    # Direction pin from controller
    y_increment = 3
    num_lines = int(y_dist / y_increment)

    clockwise = True
    #CW Away from limit switch
    try:
        # Make box with given number of lines.
        for _ in range(num_lines):
            xMove(x_dist, clockwise)
            yMove(y_increment, True)
            clockwise = not(clockwise)


    # Once finished clean everything up
    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def main():
    trace_box()
    GPIO.cleanup()

if __name__ == '__main__':
    main()