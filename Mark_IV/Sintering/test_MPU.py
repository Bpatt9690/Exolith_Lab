import time
import sys
import math
import smbus
from elevationTracking import elevation_tracker
import RPi.GPIO as GPIO
from time import sleep
import os
import inspect



PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


bus = smbus.SMBus(1)
DeviceAddress = 0x68
bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)
bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)
bus.write_byte_data(DeviceAddress, CONFIG, int("0000110", 2))
bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)
bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)

high = bus.read_byte_data(DeviceAddress, ACCEL_YOUT_H)
low = bus.read_byte_data(DeviceAddress, ACCEL_YOUT_H)
t0 = time.time()

et = elevation_tracker()

# Wait for MPU to Settle
settling_time = 4
print('Settling MPU for %d seconds' % settling_time)
time.sleep(4)
print('MPU is Done Settling')

def accel_calibration(calibration_time=20):
    """
        Description: This is a function to get the offset values
            for gyro calibration for mpu6050.
        
        Parameters:
        
        calibration_time[int]: Time in seconds you want to calibrate
            mpu6050. The longer the time the more accurate the
            calibration
    
        Outputs: Array with offsets pertaining to three axes of
            rotation [offset_gx, offset_gy, offset_gz]. Add these
            offsets to your sensor readins later on for more
            accurate readings!
    """
    print('--' * 25)
    print('Beginning Accelerometer Calibration - Do not move the MPU6050')
    
    # placeholder for the average of tuples in mpu_gyro_array
    offsets = [0, 0, 0]
    # placeholder for number of calculations we get from the mpu
    num_of_points = 0
    
    # We get the current time and add the calibration time
    end_loop_time = time.time() + calibration_time
    # We end the loop once the calibration time has passed
    while end_loop_time > time.time():
        num_of_points += 1
        
        offsets[0] += read_raw_data(ACCEL_XOUT_H) - 300
        offsets[1] += read_raw_data(ACCEL_YOUT_H) - 200
        offsets[2] += read_raw_data(ACCEL_ZOUT_H) - 1200
        
        # This is just to show you its still calibrating :)
        if num_of_points % 500 == 0:
            xAngle, yAngle = et.tiltAngle()
            print('Still Calibrating Accelerometer... %d points so far' % num_of_points)
            print('Angle: ' + str(xAngle))
            
        
    print('Calibration for Accelerometer is Complete! %d points total' % num_of_points)
    offsets = [i/num_of_points for i in offsets] # we divide by the length to get the mean
    print('X Offset: ' + str(offsets[0]))
    print('Y Offset: ' + str(offsets[1]))
    print('Z Offset: ' + str(offsets[2]))
    return offsets

def gyro_calibration(calibration_time=10):
    """
        Description: This is a function to get the offset values
            for gyro calibration for mpu6050.
        
        Parameters:
        
        calibration_time[int]: Time in seconds you want to calibrate
            mpu6050. The longer the time the more accurate the
            calibration
    
        Outputs: Array with offsets pertaining to three axes of
            rotation [offset_gx, offset_gy, offset_gz]. Add these
            offsets to your sensor readins later on for more
            accurate readings!
    """
    print('--' * 25)
    print('Beginning Gyro Calibration - Do not move the MPU6050')
    
    # placeholder for the average of tuples in mpu_gyro_array
    offsets = [0, 0, 0]
    # placeholder for number of calculations we get from the mpu
    num_of_points = 0
    
    # We get the current time and add the calibration time
    end_loop_time = time.time() + calibration_time
    # We end the loop once the calibration time has passed
    while end_loop_time > time.time():
        num_of_points += 1
        (gx, gy, gz) = (GYRO_XOUT_H, GYRO_YOUT_H, GYRO_ZOUT_H)
        offsets[0] += GYRO_XOUT_H
        offsets[1] += GYRO_YOUT_H
        offsets[2] += GYRO_ZOUT_H
        
        # This is just to show you its still calibrating :)
        if num_of_points % 100 == 0:
            print('Still Calibrating Gyro... %d points so far' % num_of_points)
        
    print('Calibration for Gyro is Complete! %d points total' % num_of_points)
    offsets = [i/num_of_points for i in offsets] # we divide by the length to get the mean
    return offsets
  
def read_raw_data(addr):
        while 1:
            # Accelero and Gyro value are 16-bit
            high = bus.read_byte_data(DeviceAddress, addr)
            low = bus.read_byte_data(DeviceAddress, addr + 1)

            # concatenate higher and lower value
            value = (high << 8) | low

            # to get signed value from mpu6050
            if value > 32768:
                value = value - 65536

            return value

def main():
    accel_calibration()


if __name__ == "__main__":
    main()