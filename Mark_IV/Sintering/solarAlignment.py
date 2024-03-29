import RPi.GPIO as GPIO
import time
from datetime import date, datetime
# import pytz
import arrow
from GPS import GPS_Data
import smbus
from Logging import logger
from axisReset import axis_reset
from sensorGroup import sensor_group
import os
from dotenv import load_dotenv
from elevationTracking import elevation_tracker
from azimuthTracking import azimuth_tracker

load_dotenv()
logger = logger()
elevation_tracker = elevation_tracker()
azimuth_tracker = azimuth_tracker()
gps = GPS_Data()


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
        logger.logInfo("Axis Reset Failure: {}".format(e))

    if x_axis_status and y_axis_status and ev_status:
        logger.logInfo("Successful reset")
        return True

    else:
        logger.logInfo("Axis Reset Failure")
        logger.logInfo(
            "x_axis_status: {} \ny_axis_status: {} \nev_status: {}".format(
                x_axis_status, y_axis_status, ev_status
            )
        )
        return False


def sensorGroupCheck():
    sg = sensor_group()
    light_sensor_status = False
    orientation_sensor_status = False

    try:
        light_sensor_status = sg.light_sensor_health()
        orientation_sensor_status = sg.orientation_sensor_health()

    except Exception as e:
        logger.logInfo("Sensor Group Failure: {}".format(e))

    if light_sensor_status and orientation_sensor_status:
        logger.logInfo("Sensor Group Healthy")
        return True

    else:
        logger.logInfo(
            "Sensor Group Failure: light_sensor_status: {} \norientation_sensor_status: {}".format(
                light_sensor_status, orientation_sensor_status
            )
        )
        return False


def solarElevationLogic():
    if(bool(os.getenv("useGPS"))):
        gps_dict = gps.userDefinedCoordinates()
    else:
        gps_dict = gps.getCurrentCoordinates()
    
    today, year, day, month = gps.getDate()

    now, hour, minutes, seconds = gps.getTime()

    if gps_dict["Longitude Direction"] == "W":
        longitude = -gps_dict["Longitude"]
    else:
        longitude = gps_dict["Longitude"]

    location = (gps_dict["Lattitude"], longitude)
    when = (year, month, day, int(hour), int(minutes), int(seconds), 0)

    # tz_NY = pytz.timezone("America/New_York")
    # datetime_NY = datetime.now(tz_NY)
    tz_NY = arrow.now().to('America/New_York').tzinfo
    datetime_NY = datetime.now(tz_NY)

    azimuth, elevation = elevation_tracker.sunpos(when, location, True)

    logger.logInfo("Current UTC: {}".format(now))
    #Need to fix#logger.logInfo(("EST timezone: {}:{}:{}".format(hour, minutes, seconds)))

    status = elevation_tracker.solarElevationPositioning(elevation)

    return status


def azimuthLogic():
    azimuth_status = False

    try:
        azimuth_tracker.stepMovement(1, 100)
        time.sleep(1)
        azimuth_tracker.stepMovement(0, 100)
        uvMax = azimuth_tracker.maxValue()
        azimuth_status = azimuth_tracker.azimuthPositioning(uvMax)
        return azimuth_status

    except Exception as e:
        logger.logInfo("Azimuth Logic Failure {}".format(e))
        return False


def solarTracking():
    logger.logInfo("Solar Tracking......")

    while True:
        azimuth_tracking_status = azimuth_tracker.tracking()
        solar_elevation_status = solarElevationLogic()
        time.sleep(10)  # sleep for 10 seconds before checking positioning


def main():
    azimuth_status = True  # change to false
    sensorStatus = False
    axisStatus = False

    logger.logInfo("Step 1: Reset axes, checking sensor health")
    axisStatus = axisResets()
    sensorStatus = sensorGroupCheck()

    # Need to add fail flag to prevent endless loop on failure
    while not sensorStatus:
        sensorStatus = sensorGroupCheck()

    if axisStatus and sensorStatus:
        logger.logInfo("Step 2: Solar Elevation Logic, Solar Azimuth Logic")

        solar_elevation_status = solarElevationLogic()
        azimuth_status = azimuthLogic()

        if solar_elevation_status:
            pass

        else:
            logger.logInfo(
                "Solar Elevation Status Failure: {}".format(solar_elevation_status)
            )

        if solar_elevation_status and azimuth_status:
            logger.logInfo("Step 3: Solar Tracking")
            solarTracking()

        else:
            logger.logInfo(
                "Failure: solar_elevation_status: {} \n azimuth_status: {}".format(
                    solar_elevation_status, azimuth_status
                )
            )
    else:
        logger.logInfo(
            "Step 1 Failure: axisStatus: {} \nsensorStatus: {}".format(
                axisStatus, sensorStatus
            )
        )


if __name__ == "__main__":

    if os.path.exists("uvsensor.txt"):
        os.remove("uvsensor.txt")

    main()
