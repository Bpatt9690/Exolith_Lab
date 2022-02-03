import numpy as np 
import serial
import os
import time
import sys
import _thread
import math

def findPort():

	clearScreen()
	portFound = False

	for filename in os.listdir('/dev/'):

		if filename.find('ttyUSB') !=-1:
			portName = filename
			portFound = True
		

	if portFound == False:
		print('Port not found, check connection')
		print('Press any key to return')
		returnToMain = input()
		return False

	else:
		print('Port: '+portName)
		print('Press any key to return')
		returnToMain = input()
		return portName


def moveX():

	#Possibly not needed
	setup_list = [b'M110*34\r',b'M115*36\r',b'M105*36\r',b'M114*35\r',b'M111 S6*98\r',b'T0*60\r',b'M20*22\r',b'M80*19\r',b'M105*46\r',b'M220 S100*80\r',b'M221 S100*80\r',b'M111 S6*84\r',b'T0*8\r',b'M155 S1*85\r']
	
	#Home X and Y wont be needed
	
	#Need to track the position of X at first
	move_x = [b'G1 X3 F4800*15\r',b'G1 X6 F4800*15\r',b'G1 X9 F4800*15\r',b'G1 X12 F4800*15\r',b'G1 X15 F4800*15\r',b'G1 X18 F4800*15\r',b'G1 X21 F4800*15\r',b'G1 X0 F4800*15\r']

	home_list = [b'G28 X0*111']

	#move_xx = [b'G1 X20 F4800*15\r']
	#move_y = [b'G1 Y20 F4800*15\r']
	#move_z = [b'G1 Z10 F4800*15\r']

	try:
		ser = serial.Serial('/dev/ttyUSB3', 250000)

	
		for i in setup_list:
			ser.write(i)
			time.sleep(2)
			print(i)
		print('Done setup')


		#x = 0
		
		for i in move_x:
			time.sleep(60)
			ser.write(i)
			print(i)

	
		#seconds = 600
		#while(seconds >= 0):
		#	i = 0
		#	clearScreen()
		#	sec = seconds%(24 * 3600)
		#	hour = sec//3600
		#	sec %= 3600
		#	minutes = sec//60
		#	sec %= 60
		#	print('\t\tX Positive')
		#	print('Timer:',int(minutes),':',sec)
		#	time.sleep(1)
		#	seconds-= 1
		#	ser.write(move_x[i])
		#	i+=1
		#print()
		#print('Press any button to return')
		#returnToMain = input()

		#for i in home_list:
		#	ser.write(i)
		#	time.sleep(6)


	#		for i in move_xx:
	#			ser.write(i)
	#		x+=1

		#for i in move_y:
		#	ser.write(i)
		#	time.sleep(2)


	#	print('done moving')

		#for i in setup_list:
		#	ser.write(i)
		#	print('Command'+i)
		#	time.sleep(2)
		#print('success')

		#while(true):
		#	x = ser.read()
		#	print(x)

	
	except:
		print('Fail')
		return False


def clearScreen():
	os.system('clear')


def enterPort():
	clearScreen()
	print('Enter Port: ')

	port = input()

	while(True):
		if not port:
			print('Please enter port')
			port = input()
		elif port:
			return port

def xPos():

	seconds = 600
	while(seconds >= 0):
		clearScreen()
		sec = seconds%(24 * 3600)
		hour = sec//3600
		sec %= 3600
		minutes = sec//60
		sec %= 60
		print('\t\tX Positive')
		print('Timer:',int(minutes),':',sec)
		time.sleep(1)
		seconds-= 1
	print()
	print('Press any button to return')
	returnToMain = input()
	return True
	

def xNeg():
	while(seconds >= 0):
		clearScreen()
		sec = seconds%(24 * 3600)
		hour = sec//3600
		sec %= 3600
		minutes = sec//60
		sec %= 60
		print('\t\tX Positive')
		print('Timer:',int(minutes),':',sec)
		time.sleep(1)
		seconds-= 1
	print()
	print('Press any button to return')
	returnToMain = input()
	return True

def HomingX():
	home_list = [b'G28 X0*111'] #Home X and Y

	seconds = 60

	try:
		ser = serial.Serial('/dev/ttyUSB1', 250000)

		#for i in setup_list:
		#	ser.write(i)
		#	time.sleep(2)
		#print('Done setup')

		x = 0
		
		for i in home_list:
			ser.write(i)
			time.sleep(6)
			print('hur')

	except:
		print('Fail')
		return False

	while(seconds >= 0):
		clearScreen()
		sec = seconds%(24 * 3600)
		hour = sec//3600
		sec %= 3600
		minutes = sec//60
		sec %= 60
		print('\t\tX Positive')
		print('Timer:',int(minutes),':',sec)
		time.sleep(1)
		seconds-= 1
	print()
	print('Press any button to return')
	returnToMain = input()


def userInputSelection(selection):

	if 0 < selection < 7:

		options = {
		1: findPort,
		2: enterPort,
		3: moveX,
		4: xNeg,
		5: HomingX,
		6: ShutDown
		}

		if int(selection) is 1:
			rsp = options.get(selection)()

		elif int(selection) is 2:
			rsp = options.get(selection)()

		elif int(selection) is 3:
			rsp = options.get(selection)()

		elif int(selection) is 4:
			rsp = options.get(selection)()

		elif int(selection) is 5:
			rsp = options.get(selection)()

		elif int(selection) is 6:
			rsp = options.get(selection)()

	return rsp


def ShutDown():
	try:
		# kill socket
		sys.exit(0)

	except SystemExit:
		os._exit(0)

def terminal():


	while(True):

		clearScreen()
		print('\n\t\t\t\tEXOLITH LAB\n\n')
		print('1.) Find Port')
		print()
		print('2.) Enter Port')
		print()
		print('3.) X+')
		print()
		print('4.) X-')
		print()
		print('5.) Homing X')
		print()
		print('6.) Shutdown')
		print()
	
		selection = input('Selection: ')


		if selection.isdigit() and int(selection) < 7:
			response = userInputSelection(int(selection))
		else:
			print('Please make a selection from the menu')
			time.sleep(1)


def main():

	try:
		terminal()

	except:
		ShutDown()


if __name__ == "__main__":
	main()
