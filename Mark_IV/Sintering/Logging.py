import time
from datetime import date, datetime
import arrow
import os


class logger:
    def __init__(self):
        self.tz_NY = arrow.now().to("America/New_York").tzinfo

    def logUV(self, data):
        os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")
        timestamp = self.timeStamp()
        with open("uvsensor.txt", "w") as f:
            f.write(str(data) + "\n")
            f.close()

    def logInfo(self, data):
        os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")
        timestamp = self.timeStamp()
        print(f"{timestamp} INFO: {data}")
        with open(f"./logs/{datetime.now().date()}.txt", "a") as f:
            f.write(f"{data}\n")

    def timeStamp(self):
        datetime_NY = datetime.now(self.tz_NY)
        return str(datetime_NY.strftime("%H:%M:%S"))
