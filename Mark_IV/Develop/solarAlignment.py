import RPi.GPIO as GPIO
import time
from time import sleep
import SI1145.SI1145 as SI1145
import serial
import math
from datetime import date, datetime
import pytz
from Kalman import KalmanAngle
from GPS import GPS_Data
import smbus
from Logging import logger
from axisReset import axis_reset
from sensorGroup import sensor_group
import os


def sensorGroupCheck():

	sg = sensor_group()
	light_sensor_status = False
	orientation_sensor_status = False

	try:
		light_sensor_status = sg.light_sensor_health()
		orientation_sensor_status = sg.orientation_sensor_health()

	except Exception as e:
		print('Fail',e)


	print('Orienatation Sensor, Light Sensor',light_sensor_status,orientation_sensor_status)

	if light_sensor_status and orientation_sensor_status:
		print('Sensors Healthy')
		return True

	else:
		print('Sensors Failed')
		return False


def axisResets():

	ar = axis_reset()
	x_axis_status = False
	y_axis_status = False
	ev_status = False

	try:

		x_axis_status = ar.x_axis_reset()
		y_axis_status = ar.y_axis_reset()
		ev_status = ar.elevation_reset()

	except Exception as e:
		print("Fail",e)

	print('X,Y,EV',x_axis_status,y_axis_status,ev_status)

	if x_axis_status and y_axis_status and ev_status:
		print('Succesful Reset')
		return True
		
	else:
		print('Failed Reset')
		return False

def main():

	#step 1 (reset axis, check sensor health)

	axisStatus = axisResets()
	sensorStatus = sensorGroupCheck()

	while not sensorStatus:
		sensorStatus = sensorGroupCheck()

if __name__ == '__main__':
    main()
