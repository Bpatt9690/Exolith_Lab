import serial
import time


class GPS_Data:
    def __init__(self):
        pass

    def getCurrentCoordinates(self):

        gps_dict = {}

        gps = serial.Serial(
            "/dev/ttyUSB0",
            timeout=None,
            baudrate=4800,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False,
        )

        while True:
            line = gps.readline()
            time.sleep(1)

            try:
                line = line.decode("utf-8")
                sline = line.split(",")

                if sline[0] == "$GPGGA":
                    gps_dict["Time UTC"] = sline[1]
                    gps_dict["Lattitude"] = float(sline[2]) / 100
                    gps_dict["Lattitude Direction"] = sline[3]
                    gps_dict["Longitude"] = float(sline[4]) / 100
                    gps_dict["Longitude Direction"] = sline[5]
                    gps_dict["Number Satellites"] = sline[7]
                    gps_dict["Alt Above Sea Level"] = sline[9]
                    print("GPS Data Recieved")
                    return gps_dict


            except:
                print("Failed to retrieve GPS Data")

                gps_dict["Time UTC"] = "194430"
                gps_dict["Lattitude"] = float(2833.2327) / 100
                gps_dict["Lattitude Direction"] = "N"
                gps_dict["Longitude"] = float(8111.11886) / 100
                gps_dict["Longitude Direction"] = "W"
                gps_dict["Number Satellites"] = "09"
                gps_dict["Alt Above Sea Level"] = "34.2"

                # return gps_dict
