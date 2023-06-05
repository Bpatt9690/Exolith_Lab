import RPi.GPIO as GPIO
from xy_curve import xyCurve
from yMove import yMove

'''
Moves x and y to trace a circle as if sintering.
'''

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

def main():
    circle()

if __name__ == "__main__":
    main()