import RPi.GPIO as GPIO

"""
Initial background info to know about encoders:
 
CLOCKWISE DIRECTION ->
  ______    ______    ______
  |    |    |    |    |    |
__| 1  |_0__| 1  |_0__| 1  |___

    ______    ______    ______
    |    |    |    |    |    |
____| 1  |_0__| 1  |_0__| 1  |___

COUNTERCLOCKWISE DIRECTION <-
___    ______    ______
  |    |    |    |    |
  |_0__| 1  |_0__| 1  |___

    ______    ______    ______
    |    |    |    |    |    |
0___| 1  |_0__| 1  |_0__| 1  |___

A'B'A B = meaning;                                                action
--------------------------------------------------------------------------------------
0 0 0 0 = transition from 00 to 00 = no change in reading;        do a jump to line 17
0 0 0 1 = transition from 00 to 01 = clockwise rotation;          do a jump to CW  
0 0 1 0 = transition from 00 to 10 = counter clockwise rotation;  do a jump to CCW
0 0 1 1 = transition from 00 to 11 = error;                       do a jump to line 17
0 1 0 0 = transition from 01 to 00 = counter clockwise rotation;  do a jump to CCW 
0 1 0 1 = transition from 01 to 01 = no change in reading;        do a jump to line 17
0 1 1 0 = transition from 01 to 10 = error;                       do a jump to line 17
0 1 1 1 = transition from 01 to 11 = clockwise rotation;          do a jump to CW  
1 0 0 0 = transition from 10 to 00 = clockwise rotation;          do a jump to CW  
1 0 0 1 = transition from 10 to 01 = error;                       do a jump to line 17
1 0 1 0 = transition from 10 to 10 = no change in reading;        do a jump to line 17
1 0 1 1 = transition from 10 to 11 = counter clockwise rotation;  do a jump to CCW
1 1 0 0 = transition from 11 to 00 = error;                       do a jump to line 17
1 1 0 1 = transition from 11 to 01 = counter clockwise rotation;  do a jump to CCW
1 1 1 0 = transition from 11 to 10 = clockwise rotation;          do a jump to CW  
1 1 1 1 = transition from 11 to 11 = no change in reading;        do a jump to line 17

"""

class Encoder(object):
    """
    Encoder class allows to work with rotary encoder
    which connected via two pin A and B.
    Works only on interrupts because all RPi pins allow that.
    This library is a simple port of the Arduino Encoder library
    (https://github.com/PaulStoffregen/Encoder)
    """

    def __init__(self, A, B):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A, GPIO.IN)
        GPIO.setup(B, GPIO.IN)
        self.A = A
        self.B = B
        self.pos = 0 # counts the number of state changes from inital position
        self.state = 0
        # to switch direction we can maybe just switch the input states here?
        if GPIO.input(A):
            self.state |= 1
        if GPIO.input(B):
            self.state |= 2
        GPIO.add_event_detect(A, GPIO.BOTH, callback=self.__update)
        GPIO.add_event_detect(B, GPIO.BOTH, callback=self.__update)

    """
    update() calling every time when value on A or B pins changes.
    It updates the current position based on previous and current states
    of the rotary encoder.
    """
    def __update(self, channel):
        state = self.state & 3
        if GPIO.input(self.A):
            state |= 4
        if GPIO.input(self.B):
            state |= 8

        self.state = state >> 2


        """
        state values 0, 5, 10, and 15 do not have to be included because 
        that is when there is no change in the reading so the position
        does not need to be moved
        """
        if state == 1 or state == 7 or state == 8 or state == 14:
            self.pos += 1
        elif state == 2 or state == 4 or state == 11 or state == 13:
            self.pos -= 1
        elif state == 3 or state == 12:
            self.pos += 2
        elif state == 6 or state == 9:
            self.pos -= 2


    """
    read() simply returns the current position of the rotary encoder.
    """
    def read(self):
        return self.pos