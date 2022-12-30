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
from elevationTracking import elevation_tracker
from azimuthTracking import azimuth_tracker


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
		logger.logInfo("Axis Reset Failure: "+e)
	
	if x_axis_status and y_axis_status and ev_status:
		logger.logInfo("Successful reset")
		return True
		
	else:
		logger.logInfo("Axis Reset Failure")
		logger.logInfo("x_axis_status: "+x_axis_status+" y_axis_status: "+y_axis_status+" ev_status: "+ev_status)
		return False


def sensorGroupCheck():

	sg = sensor_group()
	light_sensor_status = False
	orientation_sensor_status = False

	try:
		light_sensor_status = sg.light_sensor_health()
		orientation_sensor_status = sg.orientation_sensor_health()

	except Exception as e:
		logger.logInfo("Sensor Group Failure: "+e)

	if light_sensor_status and orientation_sensor_status:
		logger.logInfo("Sensor Group Healthy")
		return True

	else:
		logger.logInfo("Sensor Group Failure, light_sensor_status: "+light_sensor_status+" orientation_sensor_status: "+orientation_sensor_status)
		return False


def solarElevationLogic():

	response = input('User Provided GPS Data? (y/n)')
	gps_dict = {}

	if response is 'y':
		gps_dict = GPS_Data.userDefinedCoordinates()

	else:
		gps_dict = GPS_Data.getCurrentCoordinates()
	
	today, year, day, month = GPS_Data.getDate()

	now, hour, minutes, seconds = GPS_Data.getTime()


	if gps_dict['Longitude Direction'] == 'W':
        longitude = -gps_dict['Longitude']
	else:
        longitude = gps_dict['Longitude']

    location = (gps_dict['Lattitude'], longitude)
    when = (year, month, day,int(hour),int(minutes),int(seconds), 0)

	tz_NY = pytz.timezone('America/New_York') 
	datetime_NY = datetime.now(tz_NY)

	azimuth, elevation = elevation_tracker.sunpos(when, location, True)

    logger.logInfo("Current UTC: "+str(now))
    logger.logInfo("EST time: "+str(datetime_NY.strftime("%H:%M:%S")))
    logger.logInfo("Current Solar Azimuth: "+str(azimuth))

    elevation_tracker.solarTracking(elevation)


def main():

	logger.logInfo("Step 1: Reset all axis, check sensor health")
	axisStatus = axisResets()
	sensorStatus = sensorGroupCheck()

	#Need to add fail flag to prevent endless loop on failure
	while not sensorStatus:
		sensorStatus = sensorGroupCheck()

	logger.logInfo("Step 2: Solar Elevation Logic, Solar Azimuth Logic")

	if axisStatus and sensorStatus:
		solar_elevation_status = solarElevationLogic()

		if solar_elevation_status:
			azimuth_tracker.stepMovement(1,25)
			sleep(1)
			azimuth_tracker.stepMovement(0,25)
			uvMax = azimuth_tracker.maxValue()
			azimuth_tracker.azimuthPosition(uvMax)

		else:
			logger.logInfo('Solar Elvation Status Failure: '+solar_elevation_status)


	else:
		logger.logInfo("Step 1 Failure: axisStatus: "+axisStatus+" sensorStatus: "+sensorStatus)


if __name__ == '__main__':
	os.remove("uvsensor.txt")
    main()
