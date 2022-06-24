import serial
import time
import math
from datetime import date, datetime
import pytz
from Kalman import KalmanAngle
import smbus
import time
import math
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False) 

gps_dict = {}

#Get current date
today = date.today()
year = int(today.strftime("%Y"))
day = int(today.strftime("%d"))
month = int(today.strftime("%m").replace("0",""))

bus = smbus.SMBus(1) 
DeviceAddress = 0x68 
RestrictPitch = True    #Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf
radToDeg = 57.2957786
kalAngleX = 0
kalAngleY = 0
#some MPU6050 Registers and their Address
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

def gpsData():

    global gps_dict

    gps = serial.Serial("/dev/ttyUSB0", timeout=None, baudrate=4800, xonxoff=False, rtscts=False, dsrdtr=False)

    while True:
        line = gps.readline()

        try:
            line = line.decode("utf-8")
            sline = line.split(',')

            if sline[0] == '$GPGGA':
                gps_dict['Time UTC'] = sline[1]
                gps_dict['Lattitude'] = float(sline[2])/100
                gps_dict['Lattitude Direction'] = sline[3]
                gps_dict['Longitude'] = float(sline[4])/100
                gps_dict['Longitude Direction'] = sline[5]
                gps_dict['Number Satellites'] = sline[7]
                gps_dict['Alt Above Sea Level'] = sline[9]
                break

        except:
            print("Byte recieve issue")


def sunpos(when, location, refraction):

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
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)
# Refraction correction (optional)
    if refraction:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        elevation += (1.02 / tan(targ)) / 60
# Return azimuth and elevation in degrees
    return (round(azimuth, 2), round(elevation, 2))
def into_range(x, range_min, range_max):
    shiftedx = x - range_min
    delta = range_max - range_min
    return (((shiftedx % delta) + delta) % delta) + range_min



def logs(str):
    #log timestamp,event, process
    print(str)

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

    #Write to power management register
    bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)

    #Write to Configuration register
    #Setting DLPF (last three bit of 0X1A to 6 i.e '110' It removes the noise due to vibration.) https://ulrichbuschbaum.wordpress.com/2015/01/18/using-the-mpu6050s-dlpf/
    bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))

    #Write to Gyro configuration register
    bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)

    #Write to interrupt enable register
    bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)

def tiltAngle():

    kalmanX = KalmanAngle()
    kalmanY = KalmanAngle()
   
    MPU_Init()

    time.sleep(1)
    #Read Accelerometer raw value
    accX = read_raw_data(ACCEL_XOUT_H)
    accY = read_raw_data(ACCEL_YOUT_H)
    accZ = read_raw_data(ACCEL_ZOUT_H)

    #print(accX,accY,accZ)
    #print(math.sqrt((accY**2)+(accZ**2)))
    if (RestrictPitch):
        roll = math.atan2(accY,accZ) * radToDeg
        pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
    else:
        roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
        pitch = math.atan2(-accX,accZ) * radToDeg

    kalmanX.setAngle(roll)
    kalmanY.setAngle(pitch)
    gyroXAngle = roll;
    gyroYAngle = pitch;
    compAngleX = roll;
    compAngleY = pitch;

    timer = time.time()
    flag = 0
    while True:
        if(flag >100): #Problem with the connection
            print("Cannot get angle value")
            flag=0
            continue
        try:
            #Read Accelerometer raw value
            accX = read_raw_data(ACCEL_XOUT_H)
            accY = read_raw_data(ACCEL_YOUT_H)
            accZ = read_raw_data(ACCEL_ZOUT_H)

            #Read Gyroscope raw value
            gyroX = read_raw_data(GYRO_XOUT_H)
            gyroY = read_raw_data(GYRO_YOUT_H)
            gyroZ = read_raw_data(GYRO_ZOUT_H)

            dt = time.time() - timer
            timer = time.time()

            if (RestrictPitch):
                roll = math.atan2(accY,accZ) * radToDeg
                pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
            else:
                roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
                pitch = math.atan2(-accX,accZ) * radToDeg

            gyroXRate = gyroX/131
            gyroYRate = gyroY/131

            if (RestrictPitch):

                if((roll < -90 and kalAngleX >90) or (roll > 90 and kalAngleX < -90)):
                    kalmanX.setAngle(roll)
                    complAngleX = roll
                    kalAngleX   = roll
                    gyroXAngle  = roll
                else:
                    kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

                if(abs(kalAngleX)>90):
                    gyroYRate  = -gyroYRate
                    kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
            else:

                if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
                    kalmanY.setAngle(pitch)
                    complAngleY = pitch
                    kalAngleY   = pitch
                    gyroYAngle  = pitch
                else:
                    kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)

                if(abs(kalAngleY)>90):
                    gyroXRate  = -gyroXRate
                    kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

            #angle = (rate of change of angle) * change in time
            gyroXAngle = gyroXRate * dt
            gyroYAngle = gyroYAngle * dt

            #compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
            compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
            compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

            if ((gyroXAngle < -180) or (gyroXAngle > 180)):
                gyroXAngle = kalAngleX

            return str(kalAngleX)
            time.sleep(0.5)

        except Exception as exc:
            flag += 1


def elevationMovement(elevation):

    #GPIO Setup

    # Direction pin from controller
    AZ_DIR = 25

    # Step pin from controller
    AZ_STEP = 24

    # 0/1 used to signify clockwise or counterclockwise.
    CW = 1
    CCW = 0

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)

    # Establish Pins in software
    GPIO.setup(AZ_DIR, GPIO.OUT)
    GPIO.setup(AZ_STEP, GPIO.OUT)


    # Set the first direction you want it to spin
    currentTiltAngle = tiltAngle()

    logs("Current Tilt Angle: "+str(currentTiltAngle))
    logs("Current Solar Elevation: "+str(elevation))

    accuracy = 3.0

    #Used for angle adjustment
    if float(currentTiltAngle) < 0:
        currentTiltAngle = float(currentTiltAngle) * (-1)

    degreeDifference = float(elevation) - float(currentTiltAngle)
    logs("Current Degree Difference: "+str(degreeDifference))
    
    try:

        while degreeDifference > accuracy or degreeDifference < 0:

            logs(" ")
            logs("Adjusting Elevation Angle")
            logs("Current Degree Difference: "+str(degreeDifference))

            sleep(.005)
            # Esablish the direction you want to go
            if degreeDifference > 0:
                GPIO.output(AZ_DIR, CW)
                logs("CW Rotation")
            else:
                GPIO.output(AZ_DIR, CCW)
                logs("CWw Rotation")

            GPIO.output(AZ_STEP,GPIO.HIGH)

            # Allow it to get there.
            sleep(.00001) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(AZ_STEP,GPIO.LOW)

            sleep(.005)
            
            #sleep(.00001)
            #GPIO.output(AZ_DIR, CW)
            #GPIO.output(AZ_STEP,GPIO.HIGH)

            #Allow it to get there.
            #sleep(.0005) # Dictates how fast stepper motor will run
            #Set coil winding to low
            #GPIO.output(AZ_STEP,GPIO.LOW)
            #Dictates how fast stepper motor will run



             #new readings

            currentTiltAngle = tiltAngle()
            degreeDifference = float(elevation) - float(currentTiltAngle)

            #changing dir
            #GPIO.cleanup()

            #   """Change Direction: Changing direction requires time to switch. The
            #   time is dictated by the stepper motor and controller. """
            #   sleep(1.0)
            #   GPIO.output(DIR,CCW)
            #   for x in range(200):
            #       GPIO.output(STEP,GPIO.HIGH)
            #       sleep(.005)
            #       GPIO.output(STEP,GPIO.LOW)
            #       sleep(.005)

        
        logs('Tilt angle reached, stopping adjustment')

    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()


def cleanup():
    print("cleanup")
    GPIO.cleanup()
    exit()


def main():

    global year, month, day

    try:
        gpsData()
        logs(str(gps_dict))

        while True:

            now = datetime.utcnow().strftime("%H:%M:%S").replace(":","")
            
            hour = str(now[0:2])
            minutes = str(now[2:4])
            seconds = str(now[4:6])

            if gps_dict['Longitude Direction'] == 'W':
                longitude = -gps_dict['Longitude']
            else:
                longitude = gps_dict['Longitude']
          
            location = (gps_dict['Lattitude'], longitude)
            when = (year, month, day,int(hour),int(minutes),int(seconds), 0) #(year,month,date,hour,minue,sec,timezone adj)
       
            azimuth, elevation = sunpos(when, location, True)

            tz_NY = pytz.timezone('America/New_York') 
            datetime_NY = datetime.now(tz_NY)

            logs("Current UTC: "+str(now))
            logs("EST time: "+str(datetime_NY.strftime("%H:%M:%S")))
            logs("Current Solar Azimuth: "+str(azimuth))
            elevationMovement(elevation)
            print()

            time.sleep(1)

    except KeyboardInterrupt:
        print("cleanup")
        GPIO.cleanup()

if __name__ == '__main__':
    main()

        
