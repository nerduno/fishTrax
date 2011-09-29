# Test shock levels

# Import libraries
import sys, os
import pygame, math, random, time, serial, logging, datetime, json, cv
import numpy as np
import matplotlib as mpl
import tkFileDialog
import AvoidanceLearningFree as alf #establishConnection / obtainData

#SETUP SERIAL CONNECTION WITH ARDUNIO
ser, bSer = alf.establishArduinoConnection();
if not bSer:
	raise SystemExit

#GET TRIAL INFO
rootDir = '/Users/andalman/Documents/Stanford/Data/AvoidanceLearning/ShockTest'
shockdata = {}
voltage = float(raw_input('Enter shock voltage: '))
birthday = alf.obtainDate('Enter fish birthday: ')
age = (datetime.date.today() - birthday).days
print 'age ', age
fileDir = rootDir + os.sep + 'volt' + str(int(voltage*10)) + 'age' + str(age) + '_' + time.strftime('%Y%m%d%H%M%S')
os.mkdir(fileDir)
jsonFileName = fileDir + os.sep + 'volt' + str(int(voltage*10)) + 'age' + str(age) + '.json'
shockdata['fishage'] = (datetime.date.today() - birthday).days
shockdata['voltage'] = voltage
shockdata['shockLen'] = 0.1
shockdata['pyfile'] = 'ShockTestSimple.py'

raw_input('Press any key when ready')
shockdata['startT'] = time.time()
time.sleep(5)
ser.write(alf.cmd_LED_1_OFF+alf.cmd_LED_2_OFF+alf.cmd_SHOCK_SIDE1+alf.cmd_END)
shockdata['shockStartT'] = time.time()
time.sleep(0.1)
ser.write(alf.cmd_LED_1_OFF+alf.cmd_LED_2_OFF+alf.cmd_SHOCK_OFF+alf.cmd_END)
shockdata['shockEndT'] = time.time()
time.sleep(2)
ser.write(alf.cmd_LED_1_ON+alf.cmd_LED_2_ON+alf.cmd_SHOCK_OFF+alf.cmd_END)
shockdata['ledOnT'] = time.time()
time.sleep(0.1)
ser.write(alf.cmd_LED_1_OFF+alf.cmd_LED_2_OFF+alf.cmd_SHOCK_OFF+alf.cmd_END)
time.sleep(3)
print 'Done'

#write the experimental data to disk
f = open(name=jsonFileName, mode='w')
json.dump(shockdata,f)
f.close()