import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pins for PUL, DIR and EB
PUL = 4
DIR = 27
EB = 21

# Set the target position (in pulses)
target_position = 1

# Set the current position (in pulses)
current_position = 0

# Set the direction of the motor (1 for forward, 0 for backward)
direction = 1

# Set the enable pin high to enable the motor
GPIO.setup(EB, GPIO.IN)

# Set the PUL and DIR pins as outputs
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

# Set the step mode (1=full step, 2=half step, 4=microstep, etc.)
step_mode = 1

# Set the maximum speed (in pulses per second)
max_speed = 1000

# Set the acceleration (in pulses per second squared)
acceleration = 2000

# Set the PUL frequency
freq = max_speed * step_mode

# Set the duty cycle
dc = 50

# Set the PUL and DIR pins to their initial states
GPIO.output(PUL, GPIO.LOW)
GPIO.output(DIR, direction)

# Set up the PWM generator for the PUL pin
pwm = GPIO.PWM(PUL, freq)
pwm.start(dc)

# Define the encoder B signal interrupt handler
def encoder_b_interrupt(channel):
    global current_position
    if GPIO.input(EB) == GPIO.HIGH:
        current_position += 1 if direction else -1
    else:
        current_position -= 1 if direction else 1

# Set up the encoder B signal interrupt
GPIO.add_event_detect(EB, GPIO.BOTH, callback=encoder_b_interrupt)

# Move the motor to the target position
while current_position != target_position:

    # Change direction if necessary
    if current_position == 0 or current_position == target_position:
        direction = not direction
        GPIO.output(DIR, direction)

    # Change the PWM duty cycle to generate the next pulse
    dc = 100 - dc
    pwm.ChangeDutyCycle(dc)

    # Wait for the interrupt
    GPIO.event_detected(EB)

# Set the enable pin low to disable the motor
GPIO.remove_event_detect(EB)

# Cleanup the GPIOs
pwm.stop()
GPIO.cleanup()
