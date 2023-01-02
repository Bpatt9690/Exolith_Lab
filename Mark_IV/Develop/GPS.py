import serial
from Logging import logger
import time
from time import sleep
from datetime import date, datetime

class GPS_Data:

    def __init__(self):
        self.logger = logger()
        pass

    def getCurrentCoordinates():

        gps_dict = {}

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
                    logger.logInfo('GPS Data Retrieval Successful')
                    logger.logInfo("GPS Data: "+str(gps_dict))
                    return gps_dict

            except:
                self.logger.logInfo('Failed to retrieve GPS Data....')
                time.sleep(1)

    def userDefinedCoordinates():
        gps_dict = {}

        gps_dict['Time UTC'] = '173651.00'
        gps_dict['Lattitude'] = float(2833.2327)/100
        gps_dict['Lattitude Direction'] = 'N'
        gps_dict['Longitude'] = float(8111.11886)/100
        gps_dict['Longitude Direction'] = 'W'
        gps_dict['Number Satellites'] = '09'
        gps_dict['Alt Above Sea Level'] = '34.2'
        return gps_dict


    def getDate():
        today = date.today()
        year = 2023#int(today.strftime("%Y"))
        day = 2#int(today.strftime("%d"))
        month = 1#int(today.strftime("%m").replace("0",""))

        return today,year,day,month

    def getTime():
        now = datetime.utcnow().strftime("%H:%M:%S").replace(":","")
        hour = 20#str(now[0:2])
        minutes = 36#str(now[2:4])
        seconds = 51#str(now[4:6])
        return now, hour, minutes, seconds

