import serial
import time
from time import sleep
import board
import smbus
import RPi.GPIO as GPIO
import adafruit_ltr390

def gpsTest():
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
				print("GPS Sensor Data Retrieval Successful \n {}".format(gps_dict))
				return True

		except:
			print('GPS Sensor Data Retrieval Failure')

def lightTest():

	i2c = board.I2C()
	values = []

	while 1:
		print('waiting for device')
		ltr = adafruit_ltr390.LTR390(i2c)
		print(ltr.data_ready)

		if ltr.data_ready:
			break

		time.sleep(1)

	for i in range(10):
		vis = ltr.uvi
		values.append(vis)

	if sum(values)/len(values) > 0:
		print('Light Sensor Data Retrieval Successful')
		print(values)
		ltr.initialize()
		return True
	else:
		print('Light Sensor Data Retrieval Failure')


def orientationtest():
	PWR_MGMT_1 = 0x6B
	SMPLRT_DIV = 0x19
	CONFIG = 0x1A
	GYRO_CONFIG = 0x1B
	INT_ENABLE = 0x38
	ACCEL_XOUT_H = 0x3B
	ACCEL_YOUT_H = 0x3D
	ACCEL_ZOUT_H = 0x3F
	GYRO_XOUT_H = 0x43
	GYRO_YOUT_H = 0x45
	GYRO_ZOUT_H = 0x47


	bus = smbus.SMBus(1)
	DeviceAddress = 0x68
	bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)
	bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)
	bus.write_byte_data(DeviceAddress, CONFIG, int("0000110", 2))
	bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)
	bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)

	high = bus.read_byte_data(DeviceAddress, ACCEL_YOUT_H)
	low = bus.read_byte_data(DeviceAddress, ACCEL_YOUT_H)

	# concatenate higher and lower value
	value = (high << 8) | low

	# to get signed value from mpu6050
	if value > 32768:
	    value = value - 65536

	if value != 0:
	    print('Orietation Sensor Data Retrieval Successful')
	    return True
	else:
		print('Orietation Sensor Data Retrieval Failure')
		return False

def limitswitchTest():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	flag = 0
	timeVal = 0
	expiration = 10000

	while timeVal < expiration:

		if GPIO.input(25) == 0:
		    flag += 1
		    
		else:
		    flag = 0

		if flag > 5:
			print('Limit Switch Data Retrieval Successful')
			return True

		timeVal += 1
		time.sleep(0.05)

	print('Limit Switch Data Retrieval Failure')
	return False

def motortest():
	# Direction pin from controller
    GPIO.cleanup()
    DIR_1 = 19  # DIR+r
    STEP_1 = 20  # PULL+
    # 0/1 used to signify clockwise or counterclockwise.
    CW = 0
    CCW = 1
    MAX = 1000
    flag = 0

    GPIO.setmode(GPIO.BCM)

    # Setup pin layout on PI
    GPIO.setmode(GPIO.BCM)
    # Establish Pins in software
    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)
    # Set the first direction you want it to spin
    GPIO.output(DIR_1, CW)
    try:

        for x in range(MAX):

            # Set one coil winding to high
            GPIO.output(STEP_1, GPIO.HIGH)
            #        GPIO.output(STEP_2,GPIO.HIGH)
            # .5 == super slow
            # .00005 == breaking
            sleep(0.0005)  # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP_1, GPIO.LOW)
            #       GPIO.output(STEP_2,GPIO.LOW)
            sleep(0.0005)  # Dictates how fast stepper motor will run


        print('Motor Movement Successful')
        return True

    except Exception as e:
        print("Motor Movement Failure")
        return False
        GPIO.cleanup()


def main():
	systemTest = []

	systemTest.append(gpsTest())
	systemTest.append(lightTest())
	systemTest.append(orientationtest())
	systemTest.append(limitswitchTest())
	systemTest.append(motortest())

	if all(systemTest):
		print('\nAll Systems Go')
	else:
		print('Systems Failure')


if __name__ == '__main__':
	main()