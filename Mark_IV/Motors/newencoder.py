import RPi.GPIO as GPIO
import pigpio
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()

# Set the GPIO pins for PUL, DIR and EB
PUL = 4 # Pulse
DIR = 27 # Direction
EA = 21 # Encoder A pin

# One revolution = 1000 steps
# Any further specification than this requires us to know information 
# about rod diameter, thread pitch, etc.
target_position = 1000
position = 0

# 1 for forward, 0 for backward
direction = 1

# Set the PUL, DIR and EN pins to their initial states
pi.set_mode(PUL, pigpio.OUTPUT)
pi.set_mode(DIR, pigpio.OUTPUT)
# pi.set_mode(EA, pigpio.INPUT)
pi.write(PUL, 0)
pi.write(DIR, direction)
# pi.write(EA, 0)

SPR = 200 # Steps Per Revolution (We cannot change this)
microstep = 5 # Step setting (We can change this)
RPM = 1500 # Revolutions Per Minute (We can change this)
freq = (SPR * microstep * RPM) / 60 #pulse frequency in Hz
dc = 50 # Set the duty cycle (We can change this)

# Set up the PWM generator for the PUL pin
pi.set_PWM_frequency(PUL, int(freq))
pi.set_PWM_range(PUL, 100)
pi.set_PWM_dutycycle(PUL, dc)

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

while abs(position) < target_position:
    # Send a pulse to the PUL pin to move the motor one step
    pi.write(PUL, 1)
    time.sleep(1/freq)
    pi.write(PUL, 0)
    # time.sleep(1/freq) # Delay to control the speed of the motor

    if direction == 1:
        position += 1
    else:
        position -= 1
    if position == target_position or position == 0:
        # Stop the motor
        pi.stop()

pi.write(PUL, 0)
pi.stop()
GPIO.cleanup()
