# Avoidance Learning Free Manager
"""
AA 2011.08.05
Summary:
Intended to run the free swimming avoidance learning protocol.

Summary:
1. Establises a serial port connection with the Arduino sketch 'AvoidanceLearningFree'.
2. Waits for input: 'q' quits, 's' starts a new experiment.
3. During an experiment the manager:
    -tells ardiuno when/which led to turn on, and when/where to deliver shocks.
    -save trial outcomes.

Each experiment consists of a series of randomly spaced trials.  A trials involves:
1. Turning on the LED on the same side of the fish.
2. Leaving the LED for N seconds or until the fish swims to the opposite side of the tank.
3. If the LED remains on for N seconds, a shock begins on the side where the fish is.
4. The shock persists for M seconds, or until the fish swims to the opposite side of the tank.
"""

#IMPORTANT NOTE cvImg are pointers and can be modifed even if passed to a function.
#IMPORTANT NOTE cv.QueryImage returns a pointer to the same memory on every call (thus clone)

#TODO create a movie of fish tracking (diff, reflections, mask)
#TODO track multiple fish for social behavior - average proximity (or three chamber)
#TODO try 3D printed arena

#TODO Optimize by converting to grayscale and/or downsampling immediately on frame capture.
#TODO Optimize cvImages, cvMats, or maybe just switch to NumPy arrays.
#TODO Average frames to get background image.

#----------------------------------------------------------------------------#
#  Imports
#----------------------------------------------------------------------------#

# Import major libraries
import sys, os
import pygame, math, random, time, serial, logging, datetime, json, cv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyp
import tkFileDialog
#import AvoidanceAnalysis as aa
import pdb

# Initialize the random module
random.seed()

# Constants specifying trial types
ct_PAIREDTRIAL = 1
ct_TESTTRIAL = 2
ct_UNPAIREDTRIAL = 3
ct_SHOCK_ONLY = 4

# Constants for managing avoidance task state
cs_BETWEEN = 0
cs_LED = 1
cs_SHOCK = 2
cSide1 = 0
cSide2 = 1

#Serial Communication Constants (for Arduino)
cBaud = 9600
cmd_LED_1_ON = 'A' 
cmd_LED_1_OFF = 'B'
cmd_LED_2_ON = 'C'
cmd_LED_2_OFF = 'D'
cmd_SHOCK_OFF = 'E'
cmd_SHOCK_SIDE1 = 'F'
cmd_SHOCK_SIDE2 = 'G'
cmd_PULSESHOCK_SIDE1 = 'H'; 
cmd_PULSESHOCK_SIDE2 = 'I';
cmd_END = 'M'
cmd_FAIL = 'N'
cmd_HANDSHAKE = 'Z'

#Constants related to detection parameters
pgScale = 2; #how to much to scale images before displaying.
minArea = 0 #the minimum blob size
maxArea = 300000 #the maximum blob size
bMask = True #whether to mask the image to remove reflections

#Simply function that waits for keypress (required pygame window)
def waitForKeyPress():
    bKeyPress = False
    while not bKeyPress:
        event = pygame.event.poll()
        keyinput = pygame.key.get_pressed()
        if keyinput[pygame.K_ESCAPE]:
            raise SystemExit
        elif event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            bKeyPress = True
            
import datetime as dt
 
def obtainDate(prompt):
    isValid=False
    while not isValid:
        userIn = raw_input(prompt + '(format mm/dd/yy)')
        try: # strptime throws an exception if the input doesn't match the pattern
            userDate = datetime.datetime.strptime(userIn, "%m/%d/%y")
            isValid=True
        except ValueError, what_error:
            print what_error
            print "Try again! mm/dd/yy\n"
    return userDate.date()         
           
#convert opencv image to pygame image.           
def cvImg2pgSurf(cvImg):
	cvrgb = cv.CreateMat(cvImg.height, cvImg.width, cv.CV_8UC3)
	if cvImg.channels == 3:	
		cv.CvtColor(cvImg, cvrgb, cv.CV_BGR2RGB)
	else:
		cv.CvtColor(cvImg, cvrgb, cv.CV_GRAY2RGB)
	return pygame.image.frombuffer(cvrgb.tostring(), cv.GetSize(cvrgb), "RGB")            

#draw an opencv image in the current pygame display (image will be rescaled to fit the window)
def draw_cvImgInPyGame(cvImg):
    pgImg = cvImg2pgSurf(cvImg)
    screen = pygame.display.get_surface()
    pgImg = pygame.transform.scale(pgImg,(screen.get_width(),screen.get_height()))
    screen.blit(pgImg, pgImg.get_rect())
    
#background subtract and threshold img. 
#img and baseimg are subtracted.
#mask is an image, which if 0, causes the binary img to be zero.
def subtractAndThreshold(img, baseImg, threshold, mask):
    imgM = cv.GetMat(img)
    baseImgM = cv.GetMat(baseImg)
    sub_cvImg = cv.CloneMat(imgM)
    cv.AbsDiff(img, baseImgM , sub_cvImg)
    cv.Threshold ( sub_cvImg , sub_cvImg , threshold , 255 , cv.CV_THRESH_BINARY )
    if bMask:
        cv.And( sub_cvImg, mask, sub_cvImg )
    return sub_cvImg    

#compute the center of mass
grayImg = None
dilateKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)
erodeKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)
def getFirstMoments(cvImg, nErode = 0, nDilate = 0):
	global grayImg
	bPos = False
	pos = (0,0)
	if grayImg == None:
	    grayImg = cv.CreateImage((cvImg.width,cvImg.height), 8L, 1) #1channel vs 3
	cv.CvtColor(cvImg,grayImg,cv.CV_BGR2GRAY)
	if True:
		#Erode to eliminate speckle
		cv.Erode(grayImg, grayImg, erodeKernal, nErode)
		#Dilate to remove merge eyes and body
		cv.Dilate(grayImg, grayImg, dilateKernal, nDilate)
		#Get List of connected components	
		seq = cv.FindContours(grayImg, cv.CreateMemStorage(0), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)
		
		#Get each connected components area and center of mass (first moments)
		areas = []
		moments = []	
		if len(seq)>0:
			while seq != None:
				#bx, by, bwidth, bheight = cv.BoundingRect(seq, 0)
				areas.append(cv.ContourArea(seq))
				moments.append(cv.Moments(seq))
				seq = seq.h_next()
			#get the largest connected component
			ndx = areas.index(max(areas))
			if(moments[ndx].m00 > minArea and moments[ndx].m00 < maxArea):
				bPos = True
				pos = (moments[ndx].m10/moments[ndx].m00, moments[ndx].m01/moments[ndx].m00)
		del seq
	else:
		#Simple algorithm... just return the center of mass...
		moments = cv.Moments(cv.GetMat(grayImg));    
		if(moments.m00 > minArea and moments.m00 < maxArea):
			bPos = True
			pos = (moments.m10/moments.m00,moments.m01/moments.m00)
	return bPos, pos

#temp function	
def trackTwo(cvImg, nErode = 0, nDilate = 0):
	global grayImg
	bPos = False
	pos = (0,0)
	pos2 = (0,0)
	if grayImg == None:
	    grayImg = cv.CreateImage((cvImg.width,cvImg.height), 8L, 1) #1channel vs 3
	cv.CvtColor(cvImg,grayImg,cv.CV_BGR2GRAY)
	cv.Erode(grayImg, grayImg, erodeKernal, nErode)
	cv.Dilate(grayImg, grayImg, dilateKernal, nDilate)	
	seq = cv.FindContours(grayImg, cv.CreateMemStorage(0), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)

	#Get each connected components area and center of mass (first moments)
	areas = []
	moments = []	
	if len(seq)>0:
		while seq != None:
			#bx, by, bwidth, bheight = cv.BoundingRect(seq, 0)
			areas.append(cv.ContourArea(seq))
			moments.append(cv.Moments(seq))
			seq = seq.h_next()
		#get the largest connected component
		ndx = areas.index(max(areas))
		if(moments[ndx].m00 > minArea and moments[ndx].m00 < maxArea):
			bPos = True
			pos = (moments[ndx].m10/moments[ndx].m00, moments[ndx].m01/moments[ndx].m00)
			#get second largest connected component
			areas.remove(areas[ndx])
			moments.remove(moments[ndx])
			if(len(areas)>0):
				ndx = areas.index(max(areas))
				if(moments[ndx].m00 > minArea and moments[ndx].m00 < maxArea):
					pos2 = (moments[ndx].m10/moments[ndx].m00, moments[ndx].m01/moments[ndx].m00)
		
	del seq
	return bPos, pos, pos2
		
	
#return if the fish is on side1 of the arena.   
def isOnSide(point, line, sideSign):
    side = (line[1][0] - line[0][0]) * (point[1] - line[0][1]) - (line[1][1] - line[0][1]) * (point[0] - line[0][0])
    return cmp(side,0)==sideSign  

#return the line dividing the center of the arena, and a definition of side 1.
def processArenaCorners(arenaCorners, linePosition):
	a = 1-linePosition
	b = linePosition
	ac = np.array(arenaCorners)
	#arenaDivideLine = [tuple(np.mean(ac[(0,3),:],axis = 0)),tuple(np.mean(ac[(1,2),:],axis = 0))]
	arenaDivideLine = [(a*ac[0,0]+b*ac[3,0], a*ac[0,1]+b*ac[3,1]),(a*ac[1,0]+b*ac[2,0], a*ac[1,1]+b*ac[2,1])]
	side1Sign = 1
	if not isOnSide(arenaCorners[1], arenaDivideLine, side1Sign):
		side1Sign = -1
	return (arenaDivideLine, side1Sign)
    
#convert the arena corners into a color mask image (arena=255, not=0)    
def getArenaMask(cvImg, arenaCorners):        
    arenaCvMask = cv.CreateImage((cvImg.width,cvImg.height), cvImg.depth, cvImg.channels) 
    cv.SetZero(arenaCvMask)
    print arenaCorners
    cv.FillConvexPoly(arenaCvMask, arenaCorners, (255,)*cvImg.channels)
    return arenaCvMask
    
#Gets the next image from the camera.
#IMPORTANT NOTE queryImage returns a pointer to the same memory every time it is called.
#Thus cvImg will overwrite the previously returned image unless it is cloned. ie. no allocation.
def getNextImage(cvCam):
    cvImg = cv.QueryFrame(cvCam)
    return (True, cvImg)
    #IF USING BUFFERIMAGES.cpp to write TIFFs to disk, then ...
    #Modify BUFFERIMAGES to use naming convention such that one of the following work:
    #simple way: each file is numbered with a larger number: get all filenames alphabetically, 
    #   check if the greatest number is greater than last image. 
    #save memory: finite number of buffer images named ib_img01_time...ib_img30_time.
    #   load all the filenames, choose the one with the newest time, check that time has changed.
	#	filelist = os.listdir(os.getcwd())
	#	filelist = filter(lambda x: not os.path.isdir(x), filelist)
	#	filelist = filter(lambda x: not x.endswith('tiff'), filelist)
	#	newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
    #if debugging:
    #    maintain current imgNum, if 30ms have passed return a new image, otherwise (false, NULL)
    #    fn = "%s%sib_%d.tiff" % (imgBuffDir, os.sep, nImg%1000)
    #    curr_cvImg = cv.LoadImage(fn)
    
    
#Initialize conection with arduino (must be running avoidanceLearningFree.sketch)
def establishArduinoConnection():
    ser = serial.Serial(port='/dev/tty.usbmodemfd121', baudrate=cBaud, bytesize=8, parity='N', stopbits=1, timeout=1)
    ser.open()
    ser.flushInput()
    ser.flushOutput()
    print "Restart Arduino to complete handshake."
    for nAttempt in range(10):
        call = ser.read()
        if(call == cmd_HANDSHAKE):
            ser.write(cmd_HANDSHAKE)
            #add a cmd_END exchange..
            time.sleep(5)
            ser.flushInput()
            ser.flushOutput()
            return ser, True
        time.sleep(1);
    return ser, False

#Implments the logic of the experiment...    
def updateState(ser, currState, trialSide, currTrialType, bPulsed, bLedOnOppositeSide):
	#Set up Pulsed Shock
	if not bPulsed:
		shockSide1 = cmd_SHOCK_SIDE1
		shockSide2 = cmd_SHOCK_SIDE2
	else:
		shockSide1 = cmd_PULSESHOCK_SIDE1
		shockSide2 = cmd_PULSESHOCK_SIDE2
	
	#Set up LED on Opposite Side if necessary
	led1On = cmd_LED_1_ON
	led1Off = cmd_LED_1_OFF
	led2On = cmd_LED_2_ON
	led2Off = cmd_LED_2_OFF
	if bLedOnOppositeSide:
		led1On = cmd_LED_2_ON
		led1Off = cmd_LED_2_OFF
		led2On = cmd_LED_1_ON
		led2Off = cmd_LED_1_OFF
		
	#Set up shock only trials	
	if currTrialType == ct_SHOCK_ONLY:
		led1On = cmd_LED_1_OFF
		led1Off = cmd_LED_1_OFF
		led2On = cmd_LED_2_OFF
		led2Off = cmd_LED_2_OFF							
		
	if currState==cs_BETWEEN:
		ser.write(led1Off+led2Off+cmd_SHOCK_OFF+cmd_END)
		return confirmUpdate(ser)
	elif currState==cs_LED or (currState==cs_SHOCK and (currTrialType == ct_TESTTRIAL or currTrialType == ct_UNPAIREDTRIAL)):  
		if(trialSide == cSide1): 
			ser.write(led1On+led2Off+cmd_SHOCK_OFF+cmd_END)
			return confirmUpdate(ser)
		elif(trialSide == cSide2):
			ser.write(led2On+led1Off+cmd_SHOCK_OFF+cmd_END)
			return confirmUpdate(ser)
	elif currState==cs_SHOCK and currTrialType == ct_PAIREDTRIAL:
		if(trialSide == cSide1): 
			ser.write(led1On+led2Off+shockSide1+cmd_END)
			return confirmUpdate(ser)
		elif(trialSide == cSide2): 
			ser.write(led2On+led1Off+shockSide2+cmd_END)
			return confirmUpdate(ser)
	return False

#verify that the arduino is recieving the commands we send
def confirmUpdate(ser):
    startT = time.time();
    while time.time() - startT < .25:
        if(ser.inWaiting() > 0):
            if(ser.read() == cmd_END):
                return True
    return False    
   
def outputExperimentUpdate(avoidData):
	pyp.figure(1)
	ctNum = len(avoidData['trials'])-1
	#aa.plotTrialTimeByDistFromLED(avoidData,ctNum)
	print 'Trial Num %d Duration %f Side# %d' % (ctNum, avoidData['trials'][ctNum]['endT'] - avoidData['trials'][ctNum]['startT'], avoidData['trials'][ctNum]['side'])

def start_experiment():
	#experimental parameters
	currTrialType = ct_PAIREDTRIAL #this value remains the same for all but last trial 
	nNumTrials = 50
	fAcclimationTime = 600000 #ms
	fMinBetweenTrials = 150000 #ms #180000
	fMaxBetweenTrials = 210000 #ms #240000
	fMaxLED = 10000 #ms
	fMaxShock = 30000 #000 #ms #the maximum duration of the shock.
	bPulsed = True #if true the fish is shock at regular intervals rather than continuously.
	bLedOnOppositeSide = False #if the True the LED appears on the opposite side of the fish
	bDiffuseLED = True #was there diffusion paper in front of the LED.
	fEscapePosition = .55 #the percent of the lenght the of the arena the fish must go from the LED
	bCanEscape = True #if false, shock can't be avoided (on minimized by moving away from anode)
	
	#debug parameters
#   currTrialType = ct_PAIREDTRIAL
# 	nNumTrials = 5
# 	fAcclimationTime = 6000 #ms
# 	fMinBetweenTrials = 15000 #ms
# 	fMaxBetweenTrials = 15001 #ms
# 	fMaxLED = 5000 #ms
# 	fMaxShock = 5000 #000 #ms
# 	bPulsed = True
# 	bLedOnOppositeSide = True	
# 	bDiffuseLED = True #was there diffusion paper in front of the LED.
# 	fEscapePosition = .75 #the percent of the lenght the of the arena the fish must go from the LED
# 	bCanEscape = False #if false, shock can't be avoided (on minimized by moving away from anode)
	
	#get directory for data storage
	#experDir = raw_input("Enter a directory path for experimental data ['~\Documents\Stanford\Data\AvoidanceLearning\test']: ")
	#if experDir == '':
	#	experDir = '/Users/andalman/Documents/Stanford/Data/AvoidanceLearning/test'
	#if not os.path.isdir(experDir):
	#	os.mkdir(experDir)
	#Or try using pgu.gui (a pygame extension)
	experDir = tkFileDialog.askdirectory()
	
	#initialized the output data structure
	avoidData = {}
	experName = raw_input('Enter experiment file name: ')
	jsonFileName = experDir + os.sep +  experName + time.strftime('%Y%m%d%H%M%S') + '.json'
	birthday = obtainDate('Enter fish birthday: ')
	avoidData['fishbirthday'] = str(birthday)
	print 'age ', (datetime.date.today() - birthday).days
	avoidData['fishage'] =  (datetime.date.today() - birthday).days
	#avoidData['fishsize_approx'] = int(raw_input('Enter fish size (mm): '))
	avoidData['fishstrain'] = raw_input('Enter fish strain: ')
	avoidData['parameters'] = { 'numtrials':nNumTrials,
								'LEDTimeMS':fMaxLED,
								'ShockTimeMS':fMaxShock,
								'ShockV':float(raw_input('Enter shock voltage: ')),
								'AcclimationTime':fAcclimationTime,
								'MinTrialInterval':fMinBetweenTrials,
								'MaxTrialInterval':fMaxBetweenTrials,
								'bPulsedShocks':bPulsed,
								'bLedOnOppositeSide': bLedOnOppositeSide,
								'bDiffuseLED': bDiffuseLED,
								'fEscapePosition': fEscapePosition,
								'bCanEscape': bCanEscape,
								'CodeVersion':None }
	avoidData['trackingParameters'] = {}
	avoidData['trials'] = list() #outcome on each trial
	avoidData['tracking'] = list() #list of tuples (frametime, posx, posy)
	avoidData['video'] = list() #list of tubles (frametime, filename)
	
	#INIT EXPERIMENTAL PARAMETERS 
	nTrial = 0
	currState = cs_BETWEEN
	timeState = 0 #time the current state was entered
	currSide  = cSide1 #the side the fish is on.
	trialSide = cSide1 #the side the fish was on when the trial started.
	timeOfNextTrial = 0
	ser = None #serial connection
	bSer = False #is serial connection open	
	
	#SETUP SERIAL CONNECTION WITH ARDUNIO
	ser, bSer = establishArduinoConnection();
	if not bSer:
  		raise SystemExit
	
	#INIT PYGAME (handy for user interaction especially with PGU module; could also learn pyqt or wxPython or Tkinker
	pygame.quit()
	pygame.init()
	
	# SETUP THE CAMERA (output cvCam, imgBuffDir, scr_size, scr_w, scr_h)
	bCamera = False
	scr_size = scr_w, scr_h = 640, 480
	screen = pygame.display.set_mode(scr_size)
	pygame.display.set_caption("Press cv camera number [0,1..]. Press 'a' for any. Press 'y' if the camera looks correct.")
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
					(bNewImage, cvImg) = getNextImage(cvCam)
					scr_size = scr_w, scr_h = cvImg.width/pgScale, cvImg.height/pgScale
					screen = pygame.display.set_mode(scr_size)
					draw_cvImgInPyGame(cvImg)
					pygame.display.flip()     
				except:
					print "Cam load failed."

	#GET A BACKGROUND IMAGE FOR SUBTRACTION (output: bcvImg)
	#fn = imgBuffDir + os.sep + 'ib_base.tiff'
	bLive = True
	bBaseSelected = False
	pygame.display.set_caption('Press p to pause/play. Press return when stable background image is displayed:')
	while not bBaseSelected:
		if bLive: 
			(bNewImage, cvImg) = getNextImage(cvCam)
			draw_cvImgInPyGame(cvImg)
			pygame.display.flip()
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			raise SystemExit
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				bBaseSelected = True
			elif event.key == pygame.K_ESCAPE:
				raise SystemExit
			elif event.key == pygame.K_p:
				bLive = not bLive
	bcvImg = cv.CloneImage(cvImg)
	bcvImgFileName = experDir + os.sep +  experName + '_BackImg.tiff'
	cv.SaveImage(bcvImgFileName, bcvImg)
	
	#ASK USER TO SPECIFY LOCATION OF THE ARENA (output: arenaCorners, arenaDivideLine, side1Sign, arenaCVMask)
	#TODO: Allow more complex polygons
	pygame.display.set_caption('Carefully click on 4 inside corners of the arena. Start two corners on side 1, and go clockwise.')
	nNumClicks = 0
	bCancel = False
	arenaCorners = [];
	while nNumClicks<4 and not bCancel:
		event = pygame.event.poll()
		keyinput = pygame.key.get_pressed()
		# exit on corner 'x' click or escape key press
		if keyinput[pygame.K_ESCAPE]:
			raise SystemExit
		elif event.type == pygame.QUIT:
			raise SystemExit
		elif event.type == pygame.MOUSEBUTTONDOWN:
			arenaCorners.append((event.pos[0]*pgScale, event.pos[1]*pgScale))
			nNumClicks = nNumClicks+1;
			pygame.draw.circle(screen, (0,0,0), event.pos, 5, 2)
			pygame.display.flip()
	#Solve for midline, avoidance lines, and arena mask
	(arenaDivideLine, side1Sign) = processArenaCorners(arenaCorners, .5)
	(side1EscapeLine, side1EscapeSign) = processArenaCorners(arenaCorners, fEscapePosition)
	side1EscapeSign = -side1EscapeSign
	(side2EscapeLine, side2EscapeSign) = processArenaCorners(arenaCorners, 1-fEscapePosition)
	arenaCvMask = getArenaMask(bcvImg, arenaCorners)
	#Store the info
	avoidData['trackingParameters']['arenaPoly'] = arenaCorners
	avoidData['trackingParameters']['arenaDivideLine'] = arenaDivideLine
	avoidData['trackingParameters']['side1Sign'] = side1Sign
	avoidData['trackingParameters']['side1EscapeLine'] = side1EscapeLine
	avoidData['trackingParameters']['side1EscapeSign'] = side1EscapeSign
	avoidData['trackingParameters']['side2EscapeLine'] = side2EscapeLine
	avoidData['trackingParameters']['side2EscapeSign'] = side2EscapeSign

	#ASK USER TO SET THE DIFFERENCE THRESHOLD (output: nThreshold)
	bThresholdSet = False
	nThreshold = 50
	nDilate = 0
	nErode = 0
	view = 0
	formatCap = '</>: threshold. a/s:erode. z/x:dilate. v:view. return:finish. thres=%d erode=%d dilate=%d' 
	pygame.display.set_caption( formatCap % (nThreshold,nErode,nDilate))
	while not bThresholdSet:
		#Handle input
		event = pygame.event.poll()
		keyinput = pygame.key.get_pressed()
		if keyinput[pygame.K_ESCAPE]:
			raise SystemExit
		elif event.type == pygame.QUIT:
			raise SystemExit
		elif keyinput[pygame.K_RETURN]:
			bThresholdSet = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				nThreshold = nThreshold + 1
			elif event.key == pygame.K_LEFT:
				nThreshold = nThreshold - 1
			elif event.key == pygame.K_v:
				view = (view + 1) % 6
			elif event.key == pygame.K_a:
				nErode = nErode - 1 if nErode>0 else 0
			elif event.key == pygame.K_s:
				nErode = nErode + 1
			elif event.key == pygame.K_z:
				nDilate = nDilate - 1 if nDilate>0 else 0
			elif event.key == pygame.K_x:
				nDilate = nDilate + 1
			pygame.display.set_caption(formatCap % (nThreshold,nErode,nDilate))
							
		#DISPLAY BACKGRND SUBTRACTED THRESHOLDED IMAGE
		(bNewImage, curr_cvImg) = getNextImage(cvCam)
		if bNewImage: 
			#background subtract and find center of mass
			diff_cvImg = subtractAndThreshold(curr_cvImg, bcvImg, nThreshold, arenaCvMask)
			
			(bSucc, centerOfMass) = getFirstMoments(diff_cvImg,nErode,nDilate)   
			#choose fish color based on side of cage
			fishColor = (0,255,0)
			if not isOnSide(centerOfMass,arenaDivideLine, side1Sign):
				fishColor = (255,0,0)
			#draw the current view
			if view == 0:
				draw_cvImgInPyGame(diff_cvImg)
			elif view == 1:
				draw_cvImgInPyGame(curr_cvImg)
				pygame.draw.circle(screen, fishColor, map(lambda x:x/pgScale,centerOfMass), 3, 2)
			elif view == 2:
				tempImg = cv.CreateImage((diff_cvImg.width,diff_cvImg.height), 8L, 1) #1channel vs 3
				cv.CvtColor(diff_cvImg,tempImg,cv.CV_BGR2GRAY)
				cv.Erode(tempImg, tempImg, erodeKernal, nErode)
				cv.Dilate(tempImg, tempImg, dilateKernal, nDilate)
				draw_cvImgInPyGame(tempImg)
			elif view == 3:
				cv.And(curr_cvImg, arenaCvMask, curr_cvImg)
				#cv.Line(curr_cvImg, arenaDivideLine[0], arenaDivideLine[1], cv.CV_RGB(0,0,255), thickness=1, lineType=8, shift=0)
				draw_cvImgInPyGame(curr_cvImg)
				pygame.draw.circle(screen, fishColor, map(lambda x:x/pgScale,centerOfMass), 3, 2) 
			elif view == 4:
				draw_cvImgInPyGame(bcvImg)
			elif view == 5:
				draw_cvImgInPyGame(curr_cvImg)
			pygame.display.flip()
	avoidData['trackingParameters']['nDiffThreshold'] = nThreshold
	avoidData['trackingParameters']['nErode'] = nErode
	avoidData['trackingParameters']['nDilate'] = nDilate
	
	#APPROXIMATE THE FISH SIZE  (output, fishImg and 
	bFinished = False
	bLive = True
	nClick = 0
	fishSize = [(0,0),(0,0)] #head pos, tail pos
	pygame.display.set_caption('First press p to pause/play. Then click on fish head and tail. Press return when finished.')
	while not bFinished:
		if bLive: 
			(bNewImage, cvImg) = getNextImage(cvCam)
			draw_cvImgInPyGame(cvImg)
			pygame.display.flip()
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			raise SystemExit
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if nClick>=2:
					bFinished = True
			elif event.key == pygame.K_ESCAPE:
				raise SystemExit
			elif event.key == pygame.K_p:
				bLive = not bLive
		elif event.type == pygame.MOUSEBUTTONDOWN:
			fishSize[nClick%2] = (event.pos[0]*pgScale, event.pos[1]*pgScale)
			nClick = nClick+1
			pygame.draw.circle(screen, (0,0,0), event.pos, 5, 2)
			pygame.display.flip()
	avoidData['fishsize'] = fishSize	
	print fishSize
	fishImg = cv.CloneImage(cvImg)
	fishImgFileName = experDir + os.sep +  experName + '_FishImg.tiff'
	cv.SaveImage(fishImgFileName, fishImg)
                
	#INIT EXPERIMENTAL STATE
	nTrial = -1
	currState = cs_BETWEEN
	timeState = time.time()
	timeOfNextTrial = timeState + fAcclimationTime/1000.0;
	updateState(ser, currState, currSide, currTrialType, bPulsed, bLedOnOppositeSide)
	bDidEscape = False
	nView = 0
	#RUN THE EXPERIMENT
	while nTrial < nNumTrials:
		if nTrial>=0:
			pygame.display.set_caption('NextTrial# %d TimeTilNextTrial %f TrialTime %f' % (nTrial+1, timeOfNextTrial - time.time(), time.time() - avoidData['trials'][nTrial]['startT']))
		else:
			pygame.display.set_caption('NextTrial# %d TimeTilNextTrial %f' % (nTrial+1, timeOfNextTrial - time.time()))
		
		#Check for user input - for premature exit.
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			break;
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				break;
			elif event.key == pygame.K_v:
				nView = (nView+1)%2
	
		#Get fish location
		(bNewImage, curr_cvImg) = getNextImage(cvCam)
		if bNewImage: 
			frametime = time.time();
			avoidData['video'].append((frametime, None)) 
			#background subtract and find center of mass
			diff_cvImg = subtractAndThreshold(curr_cvImg, bcvImg, nThreshold, arenaCvMask)
			(bFound, centerOfMass) = getFirstMoments(diff_cvImg,nErode,nDilate)  
			if bFound:
				#record the fish location
				avoidData['tracking'].append((frametime, centerOfMass[0], centerOfMass[1]))
				
				#determine the side the fish is on
				if isOnSide(centerOfMass,arenaDivideLine, side1Sign):
					currSide = cSide1
					fishColor = (0,255,0)
				else:
					currSide = cSide2
					fishColor = (255,0,0)
				
				#determine if the fish has escaped a shock event
				escapeLine = arenaDivideLine
				if bCanEscape and (currState == cs_LED or currState == cs_SHOCK):
					if trialSide == cSide1:
						escapeLine = side1EscapeLine
						escapeSideSign = side1EscapeSign
					else:
						escapeLine = side2EscapeLine
						escapeSideSign = side2EscapeSign
					bDidEscape = isOnSide(centerOfMass, escapeLine, escapeSideSign)
					
				#Draw the fish
				cv.Line(curr_cvImg, escapeLine[0], escapeLine[1], cv.CV_RGB(0,0,255), thickness=2, lineType=8, shift=0)
				draw_cvImgInPyGame(curr_cvImg)
				if nView == 0: 
					pygame.draw.circle(screen, fishColor, map(lambda x:x/pgScale,centerOfMass), 3, 2)
				pygame.display.flip()
			else:				
				avoidData['tracking'].append((frametime, -1, -1))
				cv.Line(curr_cvImg, arenaDivideLine[0], arenaDivideLine[1], cv.CV_RGB(0,0,255), thickness=2, lineType=8, shift=0)
				draw_cvImgInPyGame(curr_cvImg)
				pygame.display.flip()
	 
		#Manage State Changes
		if(currState==cs_BETWEEN):
			if(time.time() >= timeOfNextTrial): 
				nTrial+=1
				#check if there are any trials remaining...
				if nTrial < nNumTrials:
					if nTrial == nNumTrials-1:
						#if last trial, then switch to test trial...
						currTrialType = ct_TESTTRIAL
					timeOfNextTrial = timeOfNextTrial + random.randint(fMinBetweenTrials,fMaxBetweenTrials)/1000.0
					currState = cs_LED;
					trialSide = currSide;
					timeState = time.time();
					bDidEscape = False
					bSuccess = updateState(ser, currState, trialSide, currTrialType, bPulsed, bLedOnOppositeSide)
					if not bSuccess: print "update state failed"; break
					avoidData['trials'].append({'trialNum':nTrial,
												'trialType':currTrialType,
												'startT':timeState,
												'side':currSide,
												'endT':-1})
		elif(currState==cs_LED):  
			if bDidEscape: 
				currState=cs_BETWEEN;
				timeState = time.time();
				bSuccess = updateState(ser, currState, trialSide, currTrialType, bPulsed, bLedOnOppositeSide)
				if not bSuccess: print "update state failed"; break
				avoidData['trials'][nTrial]['endT'] = timeState
				avoidData['trials'][nTrial]['bAvoidedShock'] = True
				outputExperimentUpdate(avoidData)
			elif((time.time() - timeState) > fMaxLED/1000.0):   
				currState= cs_SHOCK;
				timeState = time.time();
				bSuccess = updateState(ser, currState, trialSide, currTrialType, bPulsed, bLedOnOppositeSide)
				if not bSuccess: print "update state failed"; break
				avoidData['trials'][nTrial]['bAvoidedShock'] = False
		elif(currState==cs_SHOCK):
			#End shock state when fish switchs sides or when has elapsed.
			if bDidEscape or time.time() - timeState > fMaxShock/1000.0:
				currState=cs_BETWEEN;
				timeState = time.time();
				bSuccess = updateState(ser, currState, trialSide, currTrialType, bPulsed, bLedOnOppositeSide)
				if not bSuccess: print "update state failed"; break
				avoidData['trials'][nTrial]['endT'] = timeState
				outputExperimentUpdate(avoidData)

	#write the experimental data to disk
	f = open(name=jsonFileName, mode='w')
	json.dump(avoidData,f)
	f.close()
    
    #Clean up
	#ser.close()
	pygame.quit()

#invoke start experiment if run from command line.
if __name__ == '__main__':
    start_experiment()
