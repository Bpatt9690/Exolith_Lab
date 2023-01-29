import os


class logger:
    def __init__(self):
        pass

    def logInfo(timestamp, st):
        print(timestamp + " INFO: " + str(st))
        print()
        f = open("uvsensor.txt", "a")
        f.write(str(st) + "\n")
        f.close()
