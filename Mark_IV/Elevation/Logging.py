class logger:
    def __init__(self):
        pass

    def logInfo(timestamp, str):
        print(timestamp + " INFO: " + str)
        print()
        f = open("gpsData.txt", "a")
        f.write(str + "\n")
        f.close()
