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

# SETUP THE CAMERA (output cvCam, imgBuffDir, scr_size, scr_w, scr_h)
pygame.quit()
pygame.init()
bCamera = False
scr_size = scr_w, scr_h = 640, 480
screen = pygame.display.set_mode(scr_size)
pygame.display.set_caption("Press cv camera number [0,1..]. Press 'a' for any. Press 'y' when ready to shock.")
while not bCamera:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		raise SystemExit
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_ESCAPE:
			raise SystemExit
		elif event.key == pygame.K_y:
			bCamera = True
		else:
			try:
				print event
				print event.unicode
				if event.unicode == 'a':
					camNdx = -1
				else:
					camNdx = int(event.unicode)
				print camNdx
				cvCam = cv.CaptureFromCAM(int(camNdx))
				(bNewImage, cvImg) = alf.getNextImage(cvCam)
				scr_size = scr_w, scr_h = cvImg.width/2, cvImg.height/2
				screen = pygame.display.set_mode(scr_size)
				alf.draw_cvImgInPyGame(cvImg)
				pygame.display.flip()     
			except:
				print "Cam load failed."
				raise

# RUN THE SCOCK
startT = time.time()
shockStartT = 0.0
shockEndT = 0.0
frametime = []
nImg = -1
bShock = False
bShockDone = False
bDone = False
while not bDone:
	(bNewImage, cvImg) = alf.getNextImage(cvCam)
	t = time.time()
	if bNewImage:
		nImg = nImg + 1
		frametime.append(t)
		cvImgFileName = fileDir + os.sep +  'img_' + str(nImg) + '.tiff'
		#cv.SaveImage(cvImgFileName, cvImg)
	if not bShock and t - startT > 5:
		shockStartT = time.time()
		bShock = True
		ser.write(alf.cmd_LED_1_ON+alf.cmd_LED_2_ON+alf.cmd_SHOCK_SIDE1+alf.cmd_END);
        #if not alf.confirmUpdate(ser):
        #	print 'Command Failed'
        #	raise SystemExit
	if bShock and not bShockDone and t - startT > 5.1:
		shockEndT = time.time()
		bShockDone = True
		ser.write(alf.cmd_LED_1_OFF+alf.cmd_LED_2_OFF+alf.cmd_SHOCK_OFF+alf.cmd_END);
        #if not alf.confirmUpdate(ser):
        #	print 'Command Failed'
        #	raise SystemExit
	if bShockDone and time.time() - startT > 10:
		bDone = True

#store date
shockdata['startT'] = startT
shockdata['shockStartT'] = shockStartT
shockdata['shockEndT'] = shockEndT
shockdata['frametime'] = frametime	
		
		
		
#write the experimental data to disk
f = open(name=jsonFileName, mode='w')
json.dump(shockdata,f)
f.close()

print len(frametime)