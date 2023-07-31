# # Simple demo of the VL53L0X distance sensor.
# # Will print the sensed range/distance every second.
# import time

# import board
# import busio

# import adafruit_vl53l0x

# # Initialize I2C bus and sensor.
# i2c = busio.I2C(board.SCL, board.SDA)
# vl53 = adafruit_vl53l0x.VL53L0X(i2c)

# # Optionally adjust the measurement timing budget to change speed and accuracy.
# # See the example here for more details:
# #   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# # For example a higher speed but less accurate timing budget of 20ms:
# # vl53.measurement_timing_budget = 20000
# # Or a slower but more accurate timing budget of 200ms:
# # vl53.measurement_timing_budget = 200000
# # The default timing budget is 33ms, a good compromise of speed and accuracy.

# # Main loop will read the range and print it every second.
# while True:
#     print("Range: {0}mm".format(vl53.range))
#     time.sleep(1.0)

# Simple demo of the VL53L1X distance sensor.
# Will print the sensed range/distance every second.

import time
import board
import adafruit_vl53l1x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
print("hey")
vl53 = adafruit_vl53l1x.VL53L1X(i2c)
print("Huzzah!")

# OPTIONAL: can set non-default values
vl53.distance_mode = 1
vl53.timing_budget = 100

print("VL53L1X Simple Test.")
print("--------------------")
model_id, module_type, mask_rev = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Mask Revision: 0x{:0X}".format(mask_rev))
print("Distance Mode: ", end="")
if vl53.distance_mode == 1:
    print("SHORT")
elif vl53.distance_mode == 2:
    print("LONG")
else:
    print("UNKNOWN")
print("Timing Budget: {}".format(vl53.timing_budget))
print("--------------------")

vl53.start_ranging()

while True:
    if vl53.data_ready:
        print("Distance: {} cm".format(vl53.distance))
        vl53.clear_interrupt()
        time.sleep(1.0)


