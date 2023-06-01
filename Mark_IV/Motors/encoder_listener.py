import RPi.GPIO as GPIO


def listen_rising_edge(pin):
    # Set up GPIO mode and pin
    pin = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)

    # Set up edge detection
    GPIO.add_event_detect(pin, GPIO.RISING)

    # Wait for rising edge
    while True:
        if GPIO.event_detected(pin):
            print("Rising edge detected on pin {}".format(pin))
            break

    # Clean up GPIO
    GPIO.cleanup()

def main():
    listen_rising_edge(21)

if __name__ == '__main__':
    main()
