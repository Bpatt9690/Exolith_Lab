import RPi.GPIO as GPIO
from time import sleep
import time
import SI1145.SI1145 as SI1145
from Kalman import KalmanAngle
import smbus
import math
from Logging import logger

class sensor_group:

	def __init__(self):
        	pass

	def light_sensor_health(self):
		sensor = SI1145.SI1145()

		uvAverage = 0

		for i in range(10):
			UV = sensor.readUV()
			uvIndex = UV
			uvAverage += uvIndex
			time.sleep(.1)

		if uvAverage/10 > 0:
			return True
		else:
			print('in here')
			return True

	def orientation_sensor_health(self):

		PWR_MGMT_1   = 0x6B
		SMPLRT_DIV   = 0x19
		CONFIG       = 0x1A
		GYRO_CONFIG  = 0x1B
		INT_ENABLE   = 0x38
		ACCEL_XOUT_H = 0x3B
		ACCEL_YOUT_H = 0x3D
		ACCEL_ZOUT_H = 0x3F
		GYRO_XOUT_H  = 0x43
		GYRO_YOUT_H  = 0x45
		GYRO_ZOUT_H  = 0x47

		bus = smbus.SMBus(1) 	
		DeviceAddress = 0x68
		bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)
		bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)
		bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))
		bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)
		bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)


		high = bus.read_byte_data(DeviceAddress, ACCEL_YOUT_H)
		low = bus.read_byte_data(DeviceAddress, ACCEL_YOUT_H)

		#concatenate higher and lower value
		value = ((high << 8) | low)

		#to get signed value from mpu6050
		if(value > 32768):
			value = value - 65536

		if value is not 0:
			print('value is',value)
			return True
		else:
			return False
