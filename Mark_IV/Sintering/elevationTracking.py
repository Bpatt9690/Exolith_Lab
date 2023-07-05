import time
import sys
import math
from Kalman import KalmanAngle
import smbus
import RPi.GPIO as GPIO
from time import sleep
from Logging import logger
from dotenv import load_dotenv
import os
import inspect

# Load environment variables from .env file
load_dotenv()

class elevation_tracker:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.DeviceAddress = 0x68
        self.RestrictPitch = True
        self.radToDeg = 57.2957786
        self.kalAngleX = 0
        self.kalAngleY = 0

        # MPU6050 Registers and their Address
        self.PWR_MGMT_1 = 0x6B
        self.SMPLRT_DIV = 0x19
        self.CONFIG = 0x1A
        self.GYRO_CONFIG = 0x1B
        self.INT_ENABLE = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H = 0x43
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47
        self.logger = logger()

    def sunpos(self, when, location, refraction):

        # Extract the passed data
        year, month, day, hour, minute, second, timezone = when
        latitude, longitude = location

        # Math typing shortcuts
        rad, deg = math.radians, math.degrees
        sin, cos, tan = math.sin, math.cos, math.tan
        asin, atan2 = math.asin, math.atan2

        # Convert latitude and longitude to radians
        rlat = rad(latitude)
        rlon = rad(longitude)

        # Decimal hour of the day at Greenwich
        greenwichtime = hour - timezone + minute / 60 + second / 3600

        # Days from J2000, accurate from 1901 to 2099
        daynum = (
            367 * year
            - 7 * (year + (month + 9) // 12) // 4
            + 275 * month // 9
            + day
            - 730531.5
            + greenwichtime / 24
        )

        # Mean longitude of the sun
        mean_long = daynum * 0.01720279239 + 4.894967873

        # Mean anomaly of the Sun
        mean_anom = daynum * 0.01720197034 + 6.240040768

        # Ecliptic longitude of the sun
        eclip_long = (
            mean_long
            + 0.03342305518 * sin(mean_anom)
            + 0.0003490658504 * sin(2 * mean_anom)
        )

        # Obliquity of the ecliptic
        obliquity = 0.4090877234 - 0.000000006981317008 * daynum

        # Right ascension of the sun
        rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))

        # Declination of the sun
        decl = asin(sin(obliquity) * sin(eclip_long))

        # Local sidereal time
        sidereal = 4.894961213 + 6.300388099 * daynum + rlon

        # Hour angle of the sun
        hour_ang = sidereal - rasc

        # Local elevation of the sun
        elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))

        # Local azimuth of the sun
        azimuth = atan2(
            -cos(decl) * cos(rlat) * sin(hour_ang),
            sin(decl) - sin(rlat) * sin(elevation),
        )

        # Convert azimuth and elevation to degrees
        azimuth = self.into_range(deg(azimuth), 0, 360)
        elevation = self.into_range(deg(elevation), -180, 180)

        # Refraction correction (optional)
        if refraction:
            targ = rad((elevation + (10.3 / (elevation + 5.11))))
            elevation += (1.02 / tan(targ)) / 60

        # Return azimuth and elevation in degrees
        return (round(azimuth, 2), round(elevation, 2))

    def solarElevationPositioning(self, elevation):
        GPIO.setwarnings(False)

        # Direction pin from controller
        DIR = int(os.getenv("ELAVATION_Direction"))

        # Step pin from controller
        STEP = int(os.getenv("ELAVATION_Pulse"))

        # 0/1 used to signify clockwise or counterclockwise.
        CW = 1
        CCW = 0

        # Should be set by user, either via flag or direct input
        accuracy = 1
        degOffset = 2.7

        # Setup pin layout on RPI
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        # GPIO.output(DIR, CW)

        # for x in range(1000):
        #     GPIO.output(STEP, GPIO.HIGH)
        #     sleep(0.02)  # Dictates how fast stepper motor will run
        #     GPIO.output(STEP, GPIO.LOW)

        # time.sleep(1)

        currentTiltAngleX, currentTiltAngleY = self.tiltAngle()

        # Gathering current tilt angle from sensor
        currentTiltAngleX = 90 - (float(currentTiltAngleX) * (-1)) - degOffset

        self.logger.logInfo(
            "Current Tilt Elevation Angle: {}".format(currentTiltAngleX)
        )
        self.logger.logInfo("Current Solar Elevation: {}".format(elevation))
        time.sleep(1)

        degreeDifferenceX = float(currentTiltAngleX) - float(elevation)

        try:

            while degreeDifferenceX > accuracy or (degreeDifferenceX * (-1)) > accuracy:

                self.logger.logInfo("Adjusting Elevation Angle...")

                degreeDev = (int(degreeDifferenceX)) * 5

                degreeDev = math.floor(degreeDev)

                sleep(1.0)

                if degreeDifferenceX > 0:
                    GPIO.output(DIR, CW)
                else:
                    GPIO.output(DIR, CCW)

                for x in range(int(degreeDev)):
                    GPIO.output(STEP, GPIO.HIGH)
                    sleep(0.2)  # Dictates how fast stepper motor will run
                    GPIO.output(STEP, GPIO.LOW)

                time.sleep(1)

                # New Angle Readings
                currentTiltAngleX, currentTiltAngleY = self.tiltAngle()
                currentTiltAngleX = 90 - (float(currentTiltAngleX) * (-1)) - degOffset
                self.logger.logInfo("Lens Tilt angle: {}".format(currentTiltAngleX))
                self.logger.logInfo("Solar Elevation: {}".format(elevation))

                degreeDifferenceX = float(currentTiltAngleX) - float(elevation)

            self.logger.logInfo("Elevation Angle Reached, Stopping Adjustment")
            return True

        except Exception as e:
            self.logger.logInfo("Failure: {}".format(e))
            GPIO.cleanup()
            return False

    def tiltAngle(self):

        self.kalAngleY = 0

        kalmanX = KalmanAngle()
        kalmanY = KalmanAngle()

        self.MPU_Init()

        time.sleep(1)

        # Read Accelerometer raw value
        accX = self.read_raw_data(self.ACCEL_XOUT_H)
        accY = self.read_raw_data(self.ACCEL_YOUT_H)
        accZ = self.read_raw_data(self.ACCEL_ZOUT_H)

        if self.RestrictPitch:
            roll = math.atan2(accY, accZ) * self.radToDeg
            pitch = (
                math.atan(-accX / math.sqrt((accY**2) + (accZ**2))) * self.radToDeg
            )
        else:
            roll = (
                math.atan(accY / math.sqrt((accX**2) + (accZ**2))) * self.radToDeg
            )
            pitch = math.atan2(-accX, accZ) * self.radToDeg

        kalmanX.setAngle(roll)
        kalmanY.setAngle(pitch)
        gyroXAngle = roll
        gyroYAngle = pitch
        compAngleX = roll
        compAngleY = pitch

        timer = time.time()
        flag = 0

        while True:
            if flag > 100:  # Problem with the connection
                self.logger.logInfo("Failed to find data")
                flag = 0
                continue
            try:
                # Read Accelerometer raw value
                accX = self.read_raw_data(self.ACCEL_XOUT_H)
                accY = self.read_raw_data(self.ACCEL_YOUT_H)
                accZ = self.read_raw_data(self.ACCEL_ZOUT_H)

                # Read Gyroscope raw value
                gyroX = self.read_raw_data(self.GYRO_XOUT_H)
                gyroY = self.read_raw_data(self.GYRO_YOUT_H)
                gyroZ = self.read_raw_data(self.GYRO_ZOUT_H)

                dt = time.time() - timer
                timer = time.time()

                if self.RestrictPitch:
                    roll = math.atan2(accY, accZ) * self.radToDeg
                    pitch = (
                        math.atan(-accX / math.sqrt((accY**2) + (accZ**2)))
                        * self.radToDeg
                    )
                else:
                    roll = (
                        math.atan(accY / math.sqrt((accX**2) + (accZ**2)))
                        * self.radToDeg
                    )
                    pitch = math.atan2(-accX, accZ) * self.radToDeg

                gyroXRate = gyroX / 131
                gyroYRate = gyroY / 131

                if self.RestrictPitch:

                    if (roll < -90 and self.kalAngleX > 90) or (
                        roll > 90 and self.kalAngleX < -90
                    ):
                        kalmanX.setAngle(roll)
                        complAngleX = roll
                        self.kalAngleX = roll
                        gyroXAngle = roll
                    else:
                        self.kalAngleX = kalmanX.getAngle(roll, gyroXRate, dt)

                    if abs(self.kalAngleX) > 90:
                        gyroYRate = -gyroYRate
                        self.kalAngleY = kalmanY.getAngle(pitch, gyroYRate, dt)
                else:

                    if (pitch < -90 and self.kalAngleY > 90) or (
                        pitch > 90 and self.kalAngleY < -90
                    ):
                        kalmanY.setAngle(pitch)
                        complAngleY = pitch
                        self.kalAngleY = pitch
                        gyroYAngle = pitch
                    else:
                        self.kalAngleY = kalmanY.getAngle(pitch, gyroYRate, dt)

                    if abs(self.kalAngleY) > 90:
                        gyroXRate = -gyroXRate
                        self.kalAngleX = kalmanX.getAngle(roll, gyroXRate, dt)

                    # angle = (rate of change of angle) * change in time
                gyroXAngle = gyroXRate * dt
                gyroYAngle = gyroYAngle * dt

                # compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
                compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
                compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

                if (gyroXAngle < -180) or (gyroXAngle > 180):
                    gyroXAngle = self.kalAngleX
                if (gyroYAngle < -180) or (gyroYAngle > 180):
                    gyroYAngle = self.kalAngleY

                return str(self.kalAngleX), str(self.kalAngleY)

            except Exception as e:
                self.logger.logInfo("Tilt Angle Failure {}".format(e))
                flag += 1

    def into_range(self, x, range_min, range_max):
        shiftedx = x - range_min
        delta = range_max - range_min
        return (((shiftedx % delta) + delta) % delta) + range_min

    def read_raw_data(self, addr):

        while 1:
            try:
                # Accelero and Gyro value are 16-bit
                high = self.bus.read_byte_data(self.DeviceAddress, addr)
                low = self.bus.read_byte_data(self.DeviceAddress, addr + 1)

                # concatenate higher and lower value
                value = (high << 8) | low

                # to get signed value from mpu6050
                if value > 32768:
                    value = value - 65536

                return value

            except Exception as e:
                self.logger.logInfo("Failed to read raw MPU data: {}".format(e))

    # Read the gyro and acceleromater values from MPU6050
    def MPU_Init(self):
        while 1:
            try:
                # write to sample rate register
                self.bus.write_byte_data(self.DeviceAddress, self.SMPLRT_DIV, 7)
                self.bus.write_byte_data(self.DeviceAddress, self.PWR_MGMT_1, 1)
                self.bus.write_byte_data(
                    self.DeviceAddress, self.CONFIG, int("0000110", 2)
                )
                # Write to Gyro configuration register
                self.bus.write_byte_data(self.DeviceAddress, self.GYRO_CONFIG, 24)
                # Write to interrupt enable register
                self.bus.write_byte_data(self.DeviceAddress, self.INT_ENABLE, 1)
                return
            except Exception as e:
                self.logger.logInfo("MPU Init Failure {}".format(e))
