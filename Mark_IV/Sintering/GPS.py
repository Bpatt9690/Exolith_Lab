import serial
from Logging import logger
import time
import arrow
from datetime import date, datetime, timezone

class GPS_Data:
    def __init__(self):
        self.logger = logger()
        pass

    def getCurrentCoordinates(self):

        gps_dict = {}

        reading = "$GPGGA"

        with serial.Serial(
            "/dev/ttyUSB0",
            timeout=None,
            baudrate=4800,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        ) as gps:

            while True:
                line = gps.readline()

                try:
                    line = line.decode("utf-8")
                    sline = line.split(",")

                    if str(sline[0]) == str(reading):
                        print(sline)
                        gps_dict["Time UTC"] = sline[1]
                        gps_dict["Lattitude"] = float(sline[2]) / 100
                        gps_dict["Lattitude Direction"] = sline[3]
                        gps_dict["Longitude"] = float(sline[4]) / 100
                        gps_dict["Longitude Direction"] = sline[5]
                        gps_dict["Number Satellites"] = sline[7]
                        gps_dict["Alt Above Sea Level"] = sline[9]
                        self.logger.logInfo("GPS Data Retrieval Successful")
                        self.logger.logInfo("GPS Data: {}".format(gps_dict))
                        return gps_dict

                except Exception as e:
                    print(e)
                    self.logger.logInfo("Failed to retrieve GPS Data....")
                    time.sleep(1)

    def userDefinedCoordinates(self):
        gps_dict = {}

        gps_dict["Time UTC"] = str(datetime.now(arrow.now().to("America/New_York").tzinfo).strftime("%H%M%S"))
        gps_dict["Lattitude"] = float(2833.2327) / 100
        gps_dict["Lattitude Direction"] = "N"
        gps_dict["Longitude"] = float(8111.11886) / 100
        gps_dict["Longitude Direction"] = "W"
        gps_dict["Number Satellites"] = "09"
        gps_dict["Alt Above Sea Level"] = "34.2"
        return gps_dict

    def getDate(self):
        today = date.today()
        year = today.year
        day = today.day
        month = today.month

        return today, year, day, month

    def getTime(self):
        # now = "175520.00"
        datetime_NY = datetime.now(arrow.now().to("America/New_York").tzinfo)
        now = str(datetime_NY.strftime("%H%M%S"))
        hour = str(now[0:2])
        minutes = str(now[2:4])
        seconds = str(now[4:6])
        return now, hour, minutes, seconds
