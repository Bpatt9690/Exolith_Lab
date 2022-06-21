import serial
import time
import math

gps_dict = {}


def gpsData():

    global gps_dict

    gps = serial.Serial("/dev/ttyUSB0", timeout=None, baudrate=4800, xonxoff=False, rtscts=False, dsrdtr=False)

    while True:
        line = gps.readline()
        line = line.decode("utf-8")

        sline = line.split(',')

        if sline[0] == '$GPGGA':
            gps_dict['Time UTC'] = sline[1]
            gps_dict['Lattitude'] = sline[2]
            gps_dict['Lattitude Direction'] = sline[3]
            gps_dict['Longitude'] = sline[4]
            gps_dict['Longitude Direction'] = sline[5]
            gps_dict['Number Satellites'] = sline[7]
            gps_dict['Alt Above Sea Level'] = sline[9]
            break


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




def main():
    gpsData()
    print(gps_dict)
    #Close Encounters latitude, longitude
    location = (28.332315, 81.111895)
    #Fourth of July, 2022 at 11:20 am MDT (-6 hours) (-0 for UTC)
    when = (2022, 6, 21, 12, 45, 0, 0) #(year,month,date,hour,minue,sec,timezone adj)
    #Get the Sun's apparent location in the sky
    azimuth, elevation = sunpos(when, location, True)
    #sunpos(when,location,True)
    print(azimuth)
    print(elevation)

if __name__ == '__main__':
    main()