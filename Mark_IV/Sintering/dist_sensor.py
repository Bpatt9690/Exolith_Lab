from time import sleep
import board
import busio
import adafruit_vl53l0x

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
dSensor = adafruit_vl53l0x.VL53L0X(i2c)

try:
    while True:
        print('Range: {}mm'.format(dSensor.range))
        sleep(0.5)
except KeyboardInterrupt:
    exit()

