import time
import RPi.GPIO as GPIO
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Set ADC stuff
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT) # Set up GPIO 2 as an output for the ADS1115 ALERT/RDY pin
GPIO.setup(3, GPIO.OUT)

i2c = busio.I2C(3, 2) # Manually specify the I2C pins (SDA = GPIO 2, SCL = GPIO 3)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0, gain=2)

value = chan.value  # read raw ADC value
voltage = chan.voltage  # convert raw value to voltage
print('ADC Value: {}\t Voltage: {}V'.format(value, voltage))

