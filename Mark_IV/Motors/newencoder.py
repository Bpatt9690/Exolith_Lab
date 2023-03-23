import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pins for PUL, DIR and EB
PUL = 4 # Pulse
DIR = 27 # Direction
EA = 21 # Encoder A pin

target_position = 1000
position = 0

# 1 for forward, 0 for backward
direction = 1

# Set the encoder pin as an input
GPIO.setup(EA, GPIO.IN)

# Set the PUL and DIR pins as outputs
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

SPR = 200 # Steps Per Revolution (We cannot change this)
microstep = 5 # Step setting (We can change this)
RPM = 1500 # Revolutions Per Minute (We can change this)
freq = (SPR * microstep * RPM) / 60 #pulse frequency in Hz
dc = 50 # Set the duty cycle (We can change this)

# Set the PUL and DIR pins to their initial states
GPIO.output(PUL, GPIO.LOW)
GPIO.output(DIR, direction)

# Set up the PWM generator for the PUL pin
pwm = GPIO.PWM(PUL, freq)
pwm.start(dc)

# Define the encoder B signal interrupt handler
# def encoder_b_interrupt(channel):
#    global current_position 

#    if GPIO.input(EB) == GPIO.HIGH:
#        current_position += 1 if direction else -1
#    else:
#        current_position -= 1 if direction else 1

# Set up the encoder B signal interrupt
# GPIO.add_event_detect(EB, GPIO.BOTH, callback=encoder_b_interrupt)

# def update_position(channel):
#    global position, last_A
#    new_A = GPIO.input(EA)
#    print("A:", new_A)

#    if last_A == 0 and new_A == 1:
#        postion += 1
#    elif last_A == 1 and new_A == 0:
#       positon -= 1 

#    last_A = new_A

# GPIO.add_event_detect(EA, GPIO.BOTH, callback=update_position)
# last_A = GPIO.input(EA)

# Move the motor to the target position
while position != target_position:
    # update_position(EA)
    position += 1
    # print("current postion:", position)
    GPIO.output(PUL,GPIO.HIGH)
    time.sleep(0.000004)
    GPIO.output(PUL,GPIO.LOW)
    time.sleep(0.000004)


# Set the enable pin low to disable the motor
GPIO.remove_event_detect(EA)

# Cleanup the GPIOs
pwm.stop()
GPIO.cleanup()
