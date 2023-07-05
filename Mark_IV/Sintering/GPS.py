import serial
from Logging import logger
import time
import arrow
from datetime import date, datetime, timezone

class GPS_Data:
    def __init__(self):
        self.logger = logger()
        self.gps_dict = {}
        pass

    def getCurrentCoordinates(self):
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
                        self.gps_dict["Time UTC"] = sline[1]
                        self.gps_dict["Lattitude"] = float(sline[2]) / 100
                        self.gps_dict["Lattitude Direction"] = sline[3]
                        self.gps_dict["Longitude"] = float(sline[4]) / 100
                        self.gps_dict["Longitude Direction"] = sline[5]
                        self.gps_dict["Number Satellites"] = sline[7]
                        self.gps_dict["Alt Above Sea Level"] = sline[9]
                        self.logger.logInfo("GPS Data Retrieval Successful")
                        self.logger.logInfo("GPS Data: {}".format(self.gps_dict))
                        return self.gps_dict

                except Exception as e:
                    print(e)
                    self.logger.logInfo("Failed to retrieve GPS Data....")
                    time.sleep(1)

    def userDefinedCoordinates(self):
        self.gps_dict["Time UTC"] = "192020"
        self.gps_dict["Lattitude"] = float(2833.2327) / 100
        self.gps_dict["Lattitude Direction"] = "N"
        self.gps_dict["Longitude"] = float(8111.11886) / 100
        self.gps_dict["Longitude Direction"] = "W"
        self.gps_dict["Number Satellites"] = "09"
        self.gps_dict["Alt Above Sea Level"] = "34.2"
        return self.gps_dict

    def getDate(self):
        today = date.today()
        year = today.year
        day = today.day
        month = today.month

        return today, year, day, month

    def getTime(self):
        now = self.gps_dict["Time UTC"]
        hour = str(now[0:2])
        minutes = str(now[2:4])
        seconds = str(now[4:6])
        return now, hour, minutes, seconds
