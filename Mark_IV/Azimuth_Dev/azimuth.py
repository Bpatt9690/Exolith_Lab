import serial
import sys
import time
import math
from datetime import date, datetime
import pytz
from Kalman import KalmanAngle
from GPS import GPS_Data
import smbus
import RPi.GPIO as GPIO
from time import sleep
from Limit_Switches import limitSwitches
from Logging import logger
from Compass_Data import Compassdata


###NOTES###
#100 = 4 degree movement
#25 = degree
####

GPIO.setwarnings(False)
gps_dict = {}
bus = smbus.SMBus(1) 

DeviceAddress = 0x68 
RestrictPitch = True 
radToDeg = 57.2957786
kalAngleX = 0
kalAngleY = 0

#Changing code here
#MPU6050 Registers and their Address
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

def sunpos(when, location, refraction):

    #Extract the passed data
    year, month, day, hour, minute, second, timezone = when
    latitude, longitude = location


    #Math typing shortcuts
    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2

    #Convert latitude and longitude to radians
    rlat = rad(latitude)
    rlon = rad(longitude)

    #Decimal hour of the day at Greenwich
    greenwichtime = hour - timezone + minute / 60 + second / 3600

   #Days from J2000, accurate from 1901 to 2099
    daynum = (
        367 * year
        - 7 * (year + (month + 9) // 12) // 4
        + 275 * month // 9
        + day
        - 730531.5
        + greenwichtime / 24
    )

    #Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873

    #Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768

    #Ecliptic longitude of the sun
    eclip_long = (
        mean_long
        + 0.03342305518 * sin(mean_anom)
        + 0.0003490658504 * sin(2 * mean_anom)
    )

    #Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * daynum

    #Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))

    #Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))

    #Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon

    #Hour angle of the sun
    hour_ang = sidereal - rasc

    #Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))


    #Local azimuth of the sun
    azimuth = atan2(
        -cos(decl) * cos(rlat) * sin(hour_ang),
        sin(decl) - sin(rlat) * sin(elevation),
    )

    #Convert azimuth and elevation to degrees
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)
    

    #Refraction correction (optional)
    if refraction:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        elevation += (1.02 / tan(targ)) / 60

    print("Calculated elevation:",elevation)

    #Return azimuth and elevation in degrees
    return (round(azimuth, 2), round(elevation, 2)) #+10 accounts for errors


def into_range(x, range_min, range_max):
    shiftedx = x - range_min
    delta = range_max - range_min
    return (((shiftedx % delta) + delta) % delta) + range_min

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(DeviceAddress, addr)
    low = bus.read_byte_data(DeviceAddress, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)

    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536

    return value

 #Read the gyro and acceleromater values from MPU6050
def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)
    bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)
    bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))
    #Write to Gyro configuration register
    bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)
    #Write to interrupt enable register
    bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)


#Current timeStamps in EST can change
def timeStamp():
    tz_NY = pytz.timezone('America/New_York') 
    datetime_NY = datetime.now(tz=tz_NY)
    return str(datetime_NY.strftime("%H:%M:%S"))


def azimuthTracking(azimuth):

    while(1):
        print(azimuth)
        print(Compassdata.getGPSData())
        print()
        time.sleep(1)


#Used to cleanup GPIO pins on a keyboard hault
def cleanup():
    logger.logInfo(timeStamp(),"GPIO Pin cleanup")
    GPIO.cleanup()
    exit()


def getDate():
    today = date.today()
    year = int(today.strftime("%Y"))
    day = int(today.strftime("%d"))
    month = int(today.strftime("%m").replace("0",""))

    return today,year,day,month

def getTime():
    now = datetime.utcnow().strftime("%H:%M:%S").replace(":","")
    hour = str(now[0:2])
    minutes = str(now[2:4])
    seconds = str(now[4:6])
    return now, hour, minutes, seconds


def main():

    global gps_dict

    #Get current date
    today, year, day, month = getDate()

    try:
        gps_dict = GPS_Data.getCurrentCoordinates()

        logger.logInfo(timeStamp(),"GPS Data: "+str(gps_dict))

        while True:

            #Get current time
            now, hour, minutes, seconds = getTime()

            print(hour)
            print(minutes)
        
            if gps_dict['Longitude Direction'] == 'W':
                longitude = -gps_dict['Longitude']
            else:
                longitude = gps_dict['Longitude']

            print(longitude)
       
            location = (gps_dict['Lattitude'], longitude)
            when = (year, month, day,int(hour)-2,int(minutes),int(seconds), 0)
       
            azimuth, elevation = sunpos(when, location, True)

            tz_NY = pytz.timezone('America/New_York') 
            datetime_NY = datetime.now(tz_NY)

            #Logging current UTC/EST time and Solar Azimuth#
            logger.logInfo(timeStamp(),"Current UTC: "+str(now))
            logger.logInfo(timeStamp(),"EST time: "+str(datetime_NY.strftime("%H:%M:%S")))
            logger.logInfo(timeStamp(),"Current Solar Azimuth: "+str(azimuth))

            azimuthTracking(azimuth)

    except KeyboardInterrupt:
        logs("GPIO Cleanup")
        GPIO.cleanup()

if __name__ == '__main__':
    main()
