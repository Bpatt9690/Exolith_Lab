import time
from datetime import date, datetime
import pytz


class logger:
    def __init__(self):
        self.tz_NY = pytz.timezone("America/New_York")

    def logUV(self, data):
        timestamp = self.timeStamp()
        with open("uvsensor.txt", "r") as f:
            f.write(str(data) + "\n")
            f.close()

    def logInfo(self, data):
        timestamp = self.timeStamp()
        print(f"{timestamp} INFO: {data}")
        with open(f"{datetime.now().date()}.txt", "a") as f:
            f.write(f"{data}\n")

    def timeStamp(self):
        datetime_NY = datetime.now(self.tz_NY)
        return str(datetime_NY.strftime("%H:%M:%S"))
