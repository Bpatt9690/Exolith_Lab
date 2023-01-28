import time
from datetime import date, datetime
import pytz


class logger:

    def __init__(self):
        pass

    def logUV(self, data):
        timestamp = self.timeStamp()
        with open("uvsensor.txt", "r") as f:
            f.write(str(data) + "\n")
            f.close()

    def logInfo(self, data):
        timestamp = self.timeStamp()
        print(timestamp + " INFO: " + str(data))
        print()

        with open(f'{datetime.now().date()}.txt', 'a') as f:
            f.write(f'{data}\n')

    def timeStamp(self):
        tz_NY = pytz.timezone('America/New_York')
        datetime_NY = datetime.now(tz_NY)
        return str(datetime_NY.strftime("%H:%M:%S"))
