import RPi.GPIO as GPIO
from circle import circle
from zMove import zMove

'''
Moves x, y, and z to trace a cylinder as if sintering.
'''

def trace_bowl(radius=6, height=6):
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
    trace_bowl()
    GPIO.cleanup()

if __name__ == '__main__':
    main()