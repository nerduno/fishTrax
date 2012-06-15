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

AA 2012.01.24
Modifying to use Qt and adding two windows: one to control projector
"""

#IMPORTANT NOTE cvImg are pointers and can be modifed even if passed to a function.
#IMPORTANT NOTE cv.QueryImage returns a pointer to the same memory on every call (thus clone)

#TODO track multiple fish for social behavior - average proximity (or three chamber)
#TODO try 3D printed arena
#TODO Optimize by converting to grayscale and/or downsampling immediately on frame capture.
#TODO Optimize cvImages, cvMats, or maybe just switch to NumPy arrays.
#TODO Average frames to get background image.

#----------------------------------------------------------------------------#
#  Imports
#----------------------------------------------------------------------------#
import sys
import os
import math
import random; random.seed()
import time
import serial
import logging
import datetime
import json
import cv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as pyp
from PyQt4 import QtGui
from PyQt4 import QtCore
import pdb

#----------------------------------------------------------------------------#
#  Constants
#----------------------------------------------------------------------------#

dilateKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)
erodeKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)

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

class AvoidanceStimuli(QtGui.QWidget):
# 	cBLANK = 0
# 	cCHECKER = 1
# 	cSTRIP = 2
	cWHITE = 3
# 	cGRAY = 4
# 	cBLACK = 5
	cRED = 6
	
	def __init__(self):
		super(AvoidanceStimuli, self).__init__()
		self.res = (848,400)
		self.side1 = self.cWHITE
		self.side2 = self.cWHITE
		self.divideLineTop = 424
		self.divideLineBottom = 400
		self.bFlip = False
		self.setGeometry(100,100,self.res[0],self.res[1])
		self.show()
	
	def incDivideLineTop(self):
		self.divideLineTop+=1
		self.update()
		
	def incDivideLineBottom(self):
		self.divideLineBottom+=1
		self.update()
		
	def decDivideLineTop(self):
		self.divideLineTop-=1
		self.update()
		
	def decDivideLineBottom(self):
		self.divideLineBottom-=1
		self.update()
	
	def updateTankDisplay(self, side1stimulus, side2stimulus):
		self.side1 = side1stimulus
		self.side2 = side2stimulus
		self.update()
	
	def paintEvent(self, e):
		sp1 = 0
		sp2 = self.res[0]-1
		if self.bFlip:
			sp1 = self.res[0]-1
			sp2 = 0
			
 		painter = QtGui.QPainter()
 		painter.begin(self)
 		try:		
 			#Draw side one
			if self.side1 == self.cRED:
				brush = QtGui.QBrush(QtCore.Qt.red)
			elif self.side1 == self.cWHITE:
				brush = QtGui.QBrush(QtCore.Qt.white)
			painter.setBrush(brush)
			poly = QtGui.QPolygonF()
			poly.append(QtCore.QPointF(sp1,0))
			poly.append(QtCore.QPointF(self.divideLineTop,0))
			poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]-1))
			poly.append(QtCore.QPointF(sp1,self.res[1]-1))
			painter.drawPolygon(poly)
			
 			#Draw side one
			if self.side2 == self.cRED:
				brush = QtGui.QBrush(QtCore.Qt.red)
			elif self.side2 == self.cWHITE:
				brush = QtGui.QBrush(QtCore.Qt.white)
			painter.setBrush(brush)
			poly = QtGui.QPolygonF()
			poly.append(QtCore.QPointF(sp2,0))
			poly.append(QtCore.QPointF(self.divideLineTop,0))
			poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]-1))
			poly.append(QtCore.QPointF(sp2,self.res[1]-1))
			painter.drawPolygon(poly)	
			
		finally:
	 		painter.end()

# 		
# 		#draw side 1

# 		painter.setBrush(brush)
# 		poly = QtGui.QPolygonF()
# 		poly.append(QtCore.QPointF(sp1,0))
# 		poly.append(QtCore.QPointF(self.divideLineTop,0))
# 		poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]))
# 		poly.append(QtCore.QPointF(sp1,self.res[1]))
# 		painter.drawPolygon(poly)
# 		
# 		#draw side 2
# 		if self.side2 == self.cRED:
# 			brush = QtGui.QBrush(QtCore.Qt.red)
# 		elif self.side2 == self.cWHITE:
# 			brush = QtGui.QBrush(QtCore.Qt.white)
# 		painter.setBrush(brush)
# 		poly = QtGui.QPolygonF()
# 		poly.append(QtCore.QPointF(sp2,0))
# 		poly.append(QtCore.QPointF(self.divideLineTop,0))
# 		poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]))
# 		poly.append(QtCore.QPointF(sp2,self.res[1]))
# 		painter.drawPolygon(poly)

def obtainDate(prompt):
    isValid=False
    while not isValid:
        userIn, ok = QtGui.QInputDialog.getText(None, 'Enter date', prompt+'(format mm/dd/yy)')
        if not ok: return None
        try: # strptime throws an exception if the input doesn't match the pattern
            userIn = str(userIn);
            userDate = datetime.datetime.strptime(userIn, "%m/%d/%y")
            isValid=True
        except:
            pass
    return userDate.date()  

class OpenCVQImage(QtGui.QImage):

    def __init__(self, opencvImg):
		depth, nChannels = opencvImg.depth, opencvImg.nChannels
		if depth == cv.IPL_DEPTH_8U and nChannels == 3:
			#image is assumed to be in BGR because that is cv standard.
			w, h = cv.GetSize(opencvImg)
			opencvRgbImg = cv.CreateImage((w, h), depth, nChannels)
			cv.CvtColor(opencvImg, opencvRgbImg, cv.CV_BGR2RGB)
			self._imgData = opencvRgbImg.tostring()
			super(OpenCVQImage, self).__init__(self._imgData, w, h, \
				QtGui.QImage.Format_RGB888)
		elif depth == cv.IPL_DEPTH_8U and nChannels == 1:
			w, h = cv.GetSize(opencvImg)
			opencvRgbImg = cv.CreateImage((w, h), depth, 3)
			cv.CvtColor(opencvImg, opencvRgbImg, cv.CV_GRAY2BGR)
			cv.CvtColor(opencvRgbImg, opencvRgbImg, cv.CV_BGR2RGB)
			self._imgData = opencvRgbImg.tostring()
			super(OpenCVQImage, self).__init__(self._imgData, w, h, \
				QtGui.QImage.Format_RGB888)
		else:
			raise ValueError("Convert CV to QImage: image type not handled.")

class CameraDevice(QtCore.QObject):

    _DEFAULT_FPS = 30

    newFrame = QtCore.pyqtSignal(cv.iplimage)

    def __init__(self, cameraId=0, mirrored=False, parent=None):
        super(CameraDevice, self).__init__(parent)

        self.mirrored = mirrored
        self._cameraDevice = cv.CaptureFromCAM(cameraId)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(1000/self.fps)

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        frame = cv.QueryFrame(self._cameraDevice)
        if self.mirrored:
            mirroredFrame = cv.CreateImage(cv.GetSize(frame), frame.depth, \
                frame.nChannels)
            cv.Flip(frame, mirroredFrame, 1)
            frame = mirroredFrame
        self.newFrame.emit(frame)

    @property
    def paused(self):
        return not self._timer.isActive()

    @paused.setter
    def paused(self, p):
        if p:
            self._timer.stop()
        else:
            self._timer.start()

    @property
    def frameSize(self):
        w = cv.GetCaptureProperty(self._cameraDevice, \
            cv.CV_CAP_PROP_FRAME_WIDTH)
        h = cv.GetCaptureProperty(self._cameraDevice, \
            cv.CV_CAP_PROP_FRAME_HEIGHT)
        return int(w), int(h)

    @property
    def fps(self):
        fps = int(cv.GetCaptureProperty(self._cameraDevice, cv.CV_CAP_PROP_FPS))
        if not fps > 0:
            fps = self._DEFAULT_FPS
        return fps
        
class CameraWidget(QtGui.QWidget):

    def __init__(self, cameraDevice, parent=None):
        super(CameraWidget, self).__init__(parent)

        self._frame = None
        self._cameraDevice = cameraDevice
        self._cameraDevice.newFrame.connect(self._onNewFrame)

        w, h = self._cameraDevice.frameSize
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

    @QtCore.pyqtSlot(cv.iplimage)
    def _onNewFrame(self, frame):
        self._frame = cv.CloneImage(frame)
        self.update()

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), OpenCVQImage(self._frame))   
        
class FishTrackingDisplay(QtGui.QLabel):

	clicked = QtCore.pyqtSignal(int, int)

	def __init__(self, parent=None):
		super(FishTrackingDisplay, self).__init__(parent)
		print 't'	
		
	def mousePressEvent(self, ev):
		self.clicked.emit(ev.x(), ev.y())		

class AvoidanceLearningController(QtGui.QMainWindow):
		
	def __init__(self):
		super(AvoidanceLearningController, self).__init__()
		
		self.cam = None
		self.ser = None
		self.nDispMode = 0
		self.currCvFrame = None
		self.bcvImg = None
		self.fishImg = None
		self.currG = None
		self.tracG = None
		self.debugG = None
		self.currArenaClick = 0
		self.bExperRunning = False
		self.bTrackRunning = False
		self.bSavingFrames = False
		
		#arena info
		self.fEscapePosition = .5 #free parameter: sets position of safety line.
		self.arenaCorners = []
		self.arenaCvMask = None
		self.arenaDivideLine = [] #center line
		self.side1Sign = None
		self.side1EscapeLine = []
		self.side1EscapeSign = None
		self.side2EscapeLine = []
		self.side2EscapeSign = None
		
		#fish info
		self.fishSize = None
		
		#fish tracking parameters
		self.nThreshold = 5
		self.nDilate = 0
		self.nErode = 0
		self.minFishArea = 0 #the minimum blob size
		self.maxFishArea = 600000 #the maximum blob size
		
		self.bDebug = False
		
		self.initUI()
		
	def initUI(self):
		self.visStimWin = AvoidanceStimuli()
	
		#Create important actions
		exitAction = QtGui.QAction('Exit',self)
		#exitAction.setStatusTip('Exit Application')
		exitAction.triggered.connect(self.close)
		
		camAction = QtGui.QAction('Camera',self)
		#camAction.setStatusTip('Connect to a Camera')
		camAction.triggered.connect(self.connectToCamera)
		
		ardAction = QtGui.QAction('Arduino',self)
		#ardAction.setStatusTip('Connect to the Arduino')
		ardAction.triggered.connect(self.connectToArduino)
		
		backAction = QtGui.QAction('Background',self)
		#backAction.setStatusTip('Capture a background image for subtraction during tracking.')
		backAction.triggered.connect(self.getBackgroundImage)
		
		arenaAction = QtGui.QAction('Arena',self)
		#arenaAction.setStatusTip('Specify location of the Arena.')
		arenaAction.triggered.connect(self.getArenaLocation)
		
		fishAction = QtGui.QAction('Fish',self)
		#fishAction.setStatusTip('Specify size of fish.')
		fishAction.triggered.connect(self.getFishSize)
		
		playAction = QtGui.QAction('Play/Pause',self)
		#playAction.setStatusTip('Start and stop live view.')
		playAction.triggered.connect(self.playpause)
		
		prevViewAction = QtGui.QAction('<View',self)
		#prevViewAction.setStatusTip('Change to previous display mode.')
		prevViewAction.triggered.connect(self.prevDispMode)
		
		nextViewAction = QtGui.QAction('View>',self)
		#nextViewAction.setStatusTip('Change to next display mode.')
		nextViewAction.triggered.connect(self.nextDispMode)
		
		startExpAction = QtGui.QAction('Start Experiment',self)
		#startExpAction.setStatusTip('Start an avoidance learning experiment.')
		startExpAction.triggered.connect(self.startExperiment)
		
		self.startTrackAction = QtGui.QAction('Start SaveTrack',self)
		#self.startTrackAction.setStatusTip('Start/Stop saving position tracking only.')
		self.startTrackAction.triggered.connect(self.startstopSavingPosition)
		
		self.startSaveFrameAction = QtGui.QAction('Start SaveFrames',self)
		self.startSaveFrameAction.triggered.connect(self.startstopSavingFrames)
		
		self.startShockAction = QtGui.QAction('Shock Fish', self)
		self.startShockAction.triggered.connect(self.startShocks)
		
		#box to set threshold, nErode and nDilate
		
		
		#button to startExperiment... connect to startExperiment.
		
		#Create the menu bar
		menubar = self.menuBar()
		fileMenu= menubar.addMenu('&File')
		fileMenu.addAction(exitAction)
		fileMenu.addAction(camAction)
		
		#Create a toolbar
		self.toolbar = self.addToolBar('Main')
		self.toolbar.addAction(camAction)
		self.toolbar.addAction(ardAction)
		self.toolbar.addAction(playAction)
		self.toolbar.addAction(backAction)
		self.toolbar.addAction(arenaAction)
		self.toolbar.addAction(fishAction)
		self.toolbar.addAction(prevViewAction)
		self.toolbar.addAction(nextViewAction)
		self.toolbar.addAction(startExpAction)
		self.toolbar.addAction(self.startTrackAction)
		self.toolbar.addAction(self.startShockAction)
		self.toolbar.addAction(self.startSaveFrameAction)
		
		#Create widgets for vertical panel
		debugBox = QtGui.QCheckBox('Use Debug Params')
		debugBox.resize(debugBox.sizeHint())
		debugBox.stateChanged.connect(self.debugMode)
		
		self.threshLabel = QtGui.QLabel('Threshold = %d'%self.nThreshold)
		self.threshUp = QtGui.QPushButton('^')
		self.threshUp.clicked.connect(self.increaseThresh)
		self.threshDown = QtGui.QPushButton('v')
		self.threshDown.clicked.connect(self.decreaseThresh)
		
		self.erodeLabel = QtGui.QLabel('Erode = %d'%self.nErode)
		self.erodeUp = QtGui.QPushButton('^')
		self.erodeUp.clicked.connect(self.increaseErosion)
		self.erodeDown = QtGui.QPushButton('v')
		self.erodeDown.clicked.connect(self.decreaseErosion)
		
		self.dilateLabel = QtGui.QLabel('Dilate = %d'%self.nDilate)
		self.dilateUp = QtGui.QPushButton('^')
		self.dilateUp.clicked.connect(self.increaseDilation)
		self.dilateDown = QtGui.QPushButton('v')
		self.dilateDown.clicked.connect(self.decreaseDilation)
		
		topProjLabel = QtGui.QLabel('Stimuli Top Pos')
		incTopProj = QtGui.QPushButton('>')
		incTopProj.clicked.connect(self.visStimWin.incDivideLineTop)
		decTopProj = QtGui.QPushButton('<')
		decTopProj.clicked.connect(self.visStimWin.decDivideLineTop)
		botProjLabel = QtGui.QLabel('Stimuli Bot Pos')
		incBotProj = QtGui.QPushButton('>')
		incBotProj.clicked.connect(self.visStimWin.incDivideLineBottom)
		decBotProj = QtGui.QPushButton('<')
		decBotProj.clicked.connect(self.visStimWin.decDivideLineBottom)
		
		self.ftDisp = FishTrackingDisplay() #this label will be used to display video
		self.ftDisp.setAlignment(QtCore.Qt.AlignLeft)  
		
		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(debugBox)
		self.vbox.addWidget(self.threshLabel)
		self.vbox.addWidget(self.threshUp)
		self.vbox.addWidget(self.threshDown)
		self.vbox.addWidget(self.erodeLabel)
		self.vbox.addWidget(self.erodeUp)
		self.vbox.addWidget(self.erodeDown)
		self.vbox.addWidget(self.dilateLabel)
		self.vbox.addWidget(self.dilateUp)
		self.vbox.addWidget(self.dilateDown)
		self.vbox.addWidget(topProjLabel)
		self.vbox.addWidget(incTopProj)
		self.vbox.addWidget(decTopProj)
		self.vbox.addWidget(botProjLabel)
		self.vbox.addWidget(incBotProj)
		self.vbox.addWidget(decBotProj)
		self.vbox.addStretch(1)
		self.leftColumn = QtGui.QWidget()
		self.leftColumn.setLayout(self.vbox)
		
		self.hbox = QtGui.QHBoxLayout()
		self.hbox.addWidget(self.leftColumn)
		self.hbox.addWidget(self.ftDisp)
		self.hbox.addStretch(1)
		
		self.centralWidget = QtGui.QWidget()
		self.centralWidget.setLayout(self.hbox)
		self.setCentralWidget(self.centralWidget)
		
		self.setGeometry(100, 100, 1300, 800)
		self.setWindowTitle('Free Swimming Avoidance Learning')
		
		#Init to the status bar
		self.statusBar().showMessage('No camera connected. Click on camera connect.')
		self.show()
			
	def connectToCamera(self):
		cameraId, ok = QtGui.QInputDialog.getInt(self, 'Camera Info', 'Enter a Camera ID (try 0,1,-1, or 2):', value=0)
		if ok:
			self.cam = CameraDevice(cameraId=cameraId, parent=self)
			self.cam.newFrame.connect(self.onNewFrame)
			self.cam.paused = False
			self.statusBar().showMessage('Camera connected.')
	
	def connectToArduino(self):
		portName, ok = QtGui.QInputDialog.getText(self, 'Arduino Port', 'Enter the arduino port:', text='/dev/tty.usbmodemfd121')
		portName = str(portName)
		ser = serial.Serial(port=portName, baudrate=cBaud, bytesize=8, parity='N', stopbits=1, timeout=1)
		#ser.open()
		ser.flushInput()
		ser.flushOutput()
		self.statusBar().showMessage('Restart the arduino to complete the connection.')
		for nAttempt in range(10):
			call = ser.read()
			if(call == cmd_HANDSHAKE):
				ser.write(cmd_HANDSHAKE)
				#add a cmd_END exchange..
				time.sleep(5)
				ser.flushInput()
				ser.flushOutput()
				self.ser = ser
				self.statusBar().showMessage('Arduino connected.')
				return
			time.sleep(1);
		self.ser = None
		self.statusBar().showMessage('Arduino failed to connect.')
	
	def getBackgroundImage(self):
		if self.cam==None:
			self.statusBar().showMessage('Must connecct to camera before getting background image.')
		else:
			self.bcvImg = cv.CloneImage(self.currCvFrame) 
			self.backG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
			cv.CvtColor(self.bcvImg, self.backG, cv.CV_BGR2GRAY)
	
	def getArenaLocation(self):
		self.statusBar().showMessage('Click on the corners of the arena on side 1.')
		self.currArenaClick = 0
		self.arenaCorners = []
		self.ftDisp.clicked.connect(self.handleArenaClicks) 
	
	@QtCore.pyqtSlot(int, int) #not critical but could practice to specify which functions are slots.
	def handleArenaClicks(self, x, y):
		print x, y
		self.currArenaClick+=1
		if self.currArenaClick<5:
			self.arenaCorners.append((x,y))
			if self.currArenaClick==1:
				self.statusBar().showMessage('Click on the other corner of the arena on side 1.')
			elif self.currArenaClick==2:
				self.statusBar().showMessage('Now, click on the corners of the arena on side 2.')
			elif self.currArenaClick==3:
				self.statusBar().showMessage('Click on the other corner of the arena on side 2.')	
			elif self.currArenaClick==4:
				self.ftDisp.clicked.disconnect(self.handleArenaClicks)
				self.statusBar().showMessage('')
				(self.arenaDivideLine, self.side1Sign) = self.processArenaCorners(self.arenaCorners, .5)
				(self.side1EscapeLine, self.side1EscapeSign) = self.processArenaCorners(self.arenaCorners, self.fEscapePosition)
				self.side1EscapeSign *=-1
				(self.side2EscapeLine, self.side2EscapeSign) = self.processArenaCorners(self.arenaCorners, 1-self.fEscapePosition)
				self.getArenaMask()
	
	def getFishSize(self):
		self.statusBar().showMessage('Click on the tip of the fish tail.')
		self.currFishClick = 0
		self.fishSize = []
		self.ftDisp.clicked.connect(self.handleFishClicks) 		
		
	@QtCore.pyqtSlot(int, int) #not critical but could practice to specify which functions are slots.
	def handleFishClicks(self, x, y):
		self.currFishClick+=1
		if self.currFishClick == 1:
			self.fishSize.append((x,y))
			self.statusBar().showMessage('Click on the tip of the fish head.')
		elif self.currFishClick == 2:
			self.ftDisp.clicked.disconnect(self.handleFishClicks)
			self.fishSize.append((x,y))
			self.fishImg = cv.CloneImage(self.currCvFrame)
			self.statusBar().showMessage('')
		
	#return if the fish is on side1 of the arena.   
	def isOnSide(self, point, line, sideSign):
		side = (line[1][0] - line[0][0]) * (point[1] - line[0][1]) - (line[1][1] - line[0][1]) * (point[0] - line[0][0])
		return cmp(side,0)==sideSign  
	
	#return the line dividing the center of the arena, and a definition of side 1.
	def processArenaCorners(self, arenaCorners, linePosition):
		a = 1-linePosition
		b = linePosition
		ac = np.array(arenaCorners)
		#arenaDivideLine = [tuple(np.mean(ac[(0,3),:],axis = 0)),tuple(np.mean(ac[(1,2),:],axis = 0))]
		arenaDivideLine = [(a*ac[0,0]+b*ac[3,0], a*ac[0,1]+b*ac[3,1]),(a*ac[1,0]+b*ac[2,0], a*ac[1,1]+b*ac[2,1])]
		side1Sign = 1
		if not self.isOnSide(arenaCorners[1], arenaDivideLine, side1Sign):
			side1Sign = -1
		return (arenaDivideLine, side1Sign)
		
	#convert the arena corners into a color mask image (arena=255, not=0)    
	def getArenaMask(self): 
		cvImg = self.currCvFrame
		self.arenaCvMask = cv.CreateImage((cvImg.width,cvImg.height), cvImg.depth, cvImg.channels) 
		cv.SetZero(self.arenaCvMask)
		cv.FillConvexPoly(self.arenaCvMask, self.arenaCorners, (255,)*cvImg.channels)	
		self.maskG = cv.CreateImage((self.arenaCvMask.width, self.arenaCvMask.height), cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(self.arenaCvMask, self.maskG, cv.CV_BGR2GRAY)
		
	def playpause(self):
		if not self.cam==None:
			self.cam.paused = not self.cam.paused
	
	def increaseThresh(self):
		self.nThreshold+=1
		self.threshLabel.setText('Threshold = %d'%self.nThreshold)
		
	def decreaseThresh(self):
		self.nThreshold-=1
		if self.nThreshold<1:
			self.nThreshold = 1
		self.threshLabel.setText('Threshold = %d'%self.nThreshold)	

	def increaseErosion(self):
		self.nErode+=1
		self.erodeLabel.setText('Erode = %d'%self.nErode)
		
	def decreaseErosion(self):
		self.nErode-=1
		if self.nErode<0:
			self.nErode = 0
		self.erodeLabel.setText('Erode = %d'%self.nErode)	
		
	def increaseDilation(self):
		self.nDilate+=1
		self.dilateLabel.setText('Dilate = %d'%self.nDilate)
		
	def decreaseDilation(self):
		self.nDilate-=1
		if self.nDilate<0:
			self.nDilate = 0
		self.dilateLabel.setText('Dilate = %d'%self.nDilate)	
		
	def debugMode(self, bState):
		self.bDebug = bState
		
	def updateFishPosition(self):
		if self.bcvImg == None or self.arenaCvMask==None:
			self.foundFish = False
			self.fishPos = (0,0)
		else:		
			#Background subtract, threshold, mask, erode and dilate
			if self.currG == None:
				self.currG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)	
				self.diffG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
				self.thrsG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
				self.thrsMG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
				self.tracEG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
				self.tracDG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
				self.tracG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
			cv.CvtColor(self.currCvFrame, self.currG, cv.CV_BGR2GRAY)
			cv.AbsDiff(self.currG, self.backG, self.diffG) #difference
			cv.Threshold ( self.diffG , self.thrsG , self.nThreshold , 255 , cv.CV_THRESH_BINARY ) #threshold
			cv.And( self.thrsG, self.maskG, self.thrsMG ) #mask
			cv.Erode(self.thrsMG, self.tracEG, erodeKernal, self.nErode) #erode
			cv.Dilate(self.tracEG, self.tracDG, dilateKernal, self.nDilate) #dilate
			cv.Copy(self.tracDG, self.tracG)
			
			#Get List of connected components	
			seq = cv.FindContours(self.tracG, cv.CreateMemStorage(0), cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)		
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
				if (moments[ndx].m00 > self.minFishArea and moments[ndx].m00 < self.maxFishArea):
					self.foundFish = True
					self.fishPos = (moments[ndx].m10/moments[ndx].m00, moments[ndx].m01/moments[ndx].m00)
					if self.isOnSide(self.fishPos,self.arenaDivideLine, self.side1Sign):
						self.currSide = cSide1
					else:
						self.currSide = cSide2
				else:
					self.foundFish = False
					self.fishPos = (0,0)
					
			else:
				self.foundFish = False
				self.fishPos = (0,0)
			del seq
		
	def nextDispMode(self):
		self.nDispMode = (self.nDispMode + 1) % 8
		
	def prevDispMode(self):
		self.nDispMode = (self.nDispMode - 1) % 8	
		
	def onNewFrame(self, frame):
		self.frameTime = time.time()
		self.currCvFrame = cv.CloneImage(frame)
		
		#update fish position
		self.updateFishPosition()
		
		#if saveing position button pressed.
		if self.bTrackRunning:
			self.trackingData['tracking'].append((self.frameTime, self.fishPos[0], self.fishPos[1]))
			
		if self.bSavingFrames:
			frameName = self.frameDir + os.sep + 'frame'+ datetime.datetime.now().strftime("%H-%M-%S-%f") + '.tif'
			cv.SaveImage(frameName, self.currCvFrame)
		
		#update experimental state
		self.updateExperimentalState()
	
		#update display		
		if self.nDispMode<5:  
			#live w/ arena and fishpos
			painter = QtGui.QPainter()
			if self.nDispMode == 1 and self.tracDG!=None:
				dispImg = OpenCVQImage(self.tracDG)
			elif self.nDispMode == 2 and self.tracEG!=None:
				dispImg = OpenCVQImage(self.tracEG)
			elif self.nDispMode == 3 and self.thrsMG!=None:
				dispImg = OpenCVQImage(self.thrsMG)
			elif self.nDispMode == 4 and self.thrsG!=None:
				dispImg = OpenCVQImage(self.thrsG)
			elif self.nDispMode == 5 and self.diffG!=None:
				dispImg = OpenCVQImage(self.diffG)
			else:
				dispImg = OpenCVQImage(self.currCvFrame)
			painter.begin(dispImg)
			
			#draw the arena
			if self.currArenaClick >=1:
				pen = QtGui.QPen(QtCore.Qt.blue)
				pen.setWidth(3)
				painter.setPen(pen)
				#brush = QtGui.QBrush(QtCore.Qt.blue)
				#painter.setBrush(brush)
				poly = QtGui.QPolygonF()
				for p in self.arenaCorners:
					poly.append(QtCore.QPointF(p[0],p[1]))
				painter.drawPolygon(poly)
				
			#draw dividing line
			if self.currArenaClick >=4:
				pen.setColor(QtCore.Qt.red)
				pen.setWidth(1)
				painter.setPen(pen)
				l = self.arenaDivideLine
				painter.drawLine(QtCore.QPointF(l[0][0],l[0][1]), QtCore.QPointF(l[1][0],l[1][1]))
			
			#draw fish location
			if self.foundFish == True:
				fishColor = 'red'
				if not self.isOnSide(self.fishPos,self.arenaDivideLine, self.side1Sign):
					fishColor = 'blue'
				brush = QtGui.QBrush(QtCore.Qt.red)
				painter.setBrush(brush)
				painter.drawEllipse(QtCore.QPointF(self.fishPos[0],self.fishPos[1]), 3,3)
			
			painter.end()
			pixmap = QtGui.QPixmap.fromImage(dispImg)
			self.ftDisp.setPixmap(pixmap)	
		elif self.nDispMode == 6:  
			#live camera view
			pixmap = QtGui.QPixmap.fromImage(OpenCVQImage(self.currCvFrame))
			self.ftDisp.setPixmap(pixmap)		
		elif self.nDispMode == 7:
			#display background image
			if not self.bcvImg == None:
				qimg = OpenCVQImage(self.bcvImg)
				pixmap = QtGui.QPixmap.fromImage(qimg)
				self.ftDisp.setPixmap(pixmap)
        	else:
        		self.statusBar().showMessage('The background image has not been set.')
        		
	def startstopSavingPosition(self):	
		if self.bTrackRunning == False:	
			#get experiment information
			self.trackingFile = QtGui.QFileDialog.getSaveFileName(caption="Select file for saved tracking information:",directory="/User/andalman/Documents/Stanford/Data/AvoidanceLearning")
			if self.trackingFile=='': return
			self.trackingFile = str(self.trackingFile) 	
			self.trackingFile = self.trackingFile + time.strftime('%Y%m%d%H%M%S') + '.json'
			
			#prepare output data structure
			self.trackingData = {}
			self.trackingData['tracking'] = list() #list of tuples (frametime, posx, posy)
			
			self.startTrackAction.setText('Stop SaveTrack')
			self.bTrackRunning = True
		
		else:
			#done tracking save state.
			self.startTrackAction.setText('Start SaveTrack')
			self.bTrackRunning = False
			f = open(name=self.trackingFile, mode='w')
			json.dump(self.trackingData,f)
			f.close()
	
	def startstopSavingFrames(self):	
		if self.bSavingFrames == False:	
			self.frameDir = QtGui.QFileDialog.getExistingDirectory(caption="Select directory to save frames:")
			if self.frameDir=='': return
			self.frameDir = str(self.frameDir)		
			self.startSaveFrameAction.setText('Stop SaveFrames')
			self.bSavingFrames = True
		else:
			self.startSaveFrameAction.setText('Start SaveFrames')
			self.bSavingFrames = False
			
	def startShocks(self):
		self.shockV,ok = QtGui.QInputDialog.getDouble(None, 'Shock Voltage', 'Enter shock voltage (V):', 10,0,50)
		if not ok: 	return
		self.shockDuration,ok = QtGui.QInputDialog.getDouble(None, 'Shock Duration', 'Enter shock duration (s):', 60,0,1000)
		if not ok: 	return
		self.shockPulseLen ,ok = QtGui.QInputDialog.getDouble(None, 'Pulse Length', 'Enter pulse length (ms):', 50,0,1000)
		if not ok: 	return
		self.shockPulseSpacing ,ok = QtGui.QInputDialog.getDouble(None, 'Pulse Spacing', 'Enter pulse lenght (s):', 1,0,100)
		if not ok: 	return
		self.shockFlipPeriod ,ok = QtGui.QInputDialog.getDouble(None, 'Flip Period', 'Enter flip period (s):', 15,0,100)
		if not ok: 	return
		
		self.startShockTime = time.time()
		self.ser.write(cmd_PULSESHOCK_SIDE1+cmd_LED_1_ON+cmd_LED_2_OFF+cmd_END)
		bSuccess = self.confirmUpdate()
		if bSuccess:	
			QtCore.QTimer.singleShot(self.shockDuration*1000, self.stopShocks)
			self.shock_currSide = 1
			self.shockFlipTimer = QtCore.QTimer()
			self.shockFlipTimer.setInterval(self.shockFlipPeriod*1000)
			self.shockFlipTimer.timeout.connect(self.flipShocks)
			self.shockFlipTimer.start()
			if self.bTrackRunning:
				self.trackingData['shockInfo'] = {}
				self.trackingData['shockInfo']['Voltage'] = self.shockV
				self.trackingData['shockInfo']['Duration'] = self.shockDuration
				self.trackingData['shockInfo']['PulseLen'] = self.shockPulseLen
				self.trackingData['shockInfo']['PulseSpacing'] = self.shockPulseSpacing
				self.trackingData['shockInfo']['FlipPeriod'] = self.shockFlipPeriod
				self.trackingData['shockInfo']['ShockStartTime'] = self.startShockTime
		else:
			print 'Arduino did not receive shock command.'
			
	def flipShocks(self):
		if self.shock_currSide == 1:
			self.ser.write(cmd_PULSESHOCK_SIDE2+cmd_LED_1_OFF+cmd_LED_2_ON+cmd_END)
			bSuccess = self.confirmUpdate()
			self.shock_currSide = 2
			#TODO handle error
		else:
			self.ser.write(cmd_PULSESHOCK_SIDE1+cmd_LED_1_ON+cmd_LED_2_OFF+cmd_END)
			bSuccess = self.confirmUpdate()
			self.shock_currSide = 1
			#TODO handle error
    		
	def stopShocks(self):
		self.shockFlipTimer.stop()
		self.ser.write(cmd_SHOCK_OFF+cmd_LED_1_OFF+cmd_LED_2_OFF+cmd_END)
		self.confirmUpdate()
    
	def startExperiment(self):
	
		#Initialize experimental parameters
		if not self.bDebug:
			self.currTrialType = ct_PAIREDTRIAL #this value remains the same for all but last trial 
			self.nNumTrials = 25
			self.fAcclimationTime = 600000 #ms
			self.fMinBetweenTrials = 150000 #ms #180000
			self.fMaxBetweenTrials = 210000 #ms #240000
			self.fMaxLED = 10000 #ms
			self.fMaxShock = 30000 #000 #ms #the maximum duration of the shock.
			self.bPulsed = True #if true the fish is shock at regular intervals rather than continuously.
			self.bLedOnOppositeSide = False #if the True the LED appears on the opposite side of the fish
			self.bDiffuseLED = True #was there diffusion paper in front of the LED.
			self.fEscapePosition = .55 #the percent of the lenght the of the arena the fish must go from the LED
			self.bCanEscape = True #if false, shock can't be avoided (on minimized by moving away from anode)
		else:
			self.currTrialType = ct_PAIREDTRIAL
			self.nNumTrials = 5
			self.fAcclimationTime = 6000 #ms
			self.fMinBetweenTrials = 15000 #ms
			self.fMaxBetweenTrials = 15001 #ms
			self.fMaxLED = 5000 #ms
			self.fMaxShock = 10000 #000 #ms
			self.bPulsed = True
			self.bLedOnOppositeSide = False	
			self.bDiffuseLED = True #was there diffusion paper in front of the LED.
			self.fEscapePosition = .5 #the percent of the lenght the of the arena the fish must go from the LED
			self.bCanEscape = True #if false, shock can't be avoided (on minimized by moving away from anode)

	
		#get experiment information
		self.experDir = QtGui.QFileDialog.getExistingDirectory(caption="Select directory to save experimental data:",directory="/User/andalman/Documents/Stanford/Data/AvoidanceLearning")
		if self.experDir=='': return
		self.experDir = str(self.experDir)
		
		self.experName, ok = QtGui.QInputDialog.getText(None, 'Experiment Name', 'Enter experiment file name: ')
		if not ok: return		
		self.experName = str(self.experName)
		
		self.birthday = obtainDate('Enter fish birthday: ')  
		if self.birthday == None: return
		
		self.fishStrain, ok = QtGui.QInputDialog.getText(None, 'Fish Strain', 'Enter fish strain: ')
		if not ok: return
		
		self.shockV,ok = QtGui.QInputDialog.getDouble(None, 'Shock Voltage', 'Enter shock voltage:', 0,0,50)
		if not ok: 	return
			
		self.jsonFileName = self.experDir + os.sep +  self.experName + time.strftime('%Y%m%d%H%M%S') + '.json'
		
		#prepare output data structure
		self.avoidData = {}
		self.avoidData['fishbirthday'] = str(self.birthday)
		self.avoidData['fishage'] =  (datetime.date.today() - self.birthday).days
		self.avoidData['fishstrain'] = str(self.fishStrain)
		self.avoidData['parameters'] = { 'numtrials':self.nNumTrials,
									'LEDTimeMS':self.fMaxLED,
									'ShockTimeMS':self.fMaxShock,
									'ShockV':self.shockV,
									'AcclimationTime':self.fAcclimationTime,
									'MinTrialInterval':self.fMinBetweenTrials,
									'MaxTrialInterval':self.fMaxBetweenTrials,
									'bPulsedShocks':self.bPulsed,
									'bLedOnOppositeSide': self.bLedOnOppositeSide,
									'bDiffuseLED': self.bDiffuseLED,
									'fEscapePosition': self.fEscapePosition,
									'bCanEscape': self.bCanEscape,
									'CodeVersion':None }
		self.avoidData['trackingParameters'] = {}
		self.avoidData['trials'] = list() #outcome on each trial
		self.avoidData['tracking'] = list() #list of tuples (frametime, posx, posy)
		self.avoidData['video'] = list() #list of tubles (frametime, filename)	
		self.avoidData['trackingParameters']['arenaPoly'] = self.arenaCorners
		self.avoidData['trackingParameters']['arenaDivideLine'] = self.arenaDivideLine
		self.avoidData['trackingParameters']['side1Sign'] = self.side1Sign
		self.avoidData['trackingParameters']['side1EscapeLine'] = self.side1EscapeLine
		self.avoidData['trackingParameters']['side1EscapeSign'] = self.side1EscapeSign
		self.avoidData['trackingParameters']['side2EscapeLine'] = self.side2EscapeLine
		self.avoidData['trackingParameters']['side2EscapeSign'] = self.side2EscapeSign	
		self.avoidData['trackingParameters']['nDiffThreshold'] = self.nThreshold
		self.avoidData['trackingParameters']['nErode'] = self.nErode
		self.avoidData['trackingParameters']['nDilate'] = self.nDilate
		self.avoidData['fishsize'] = self.fishSize	
		self.bcvImgFileName = self.experDir + os.sep +  self.experName + '_BackImg.tiff'
		cv.SaveImage(self.bcvImgFileName, self.bcvImg)	
		self.fishImgFileName = self.experDir + os.sep +  self.experName + '_FishImg.tiff'
		cv.SaveImage(self.fishImgFileName, self.fishImg)
		
		#initialize experiment state
		self.currTrialType = ct_PAIREDTRIAL #this value remains the same for all but last trial 
		self.nTrial = -1
		self.currState = cs_BETWEEN
		self.timeState = time.time() #time the current state was entered
		self.timeOfNextTrial = self.timeState + self.fAcclimationTime/1000.0	
		self.trialSide = cSide1 #the side the fish was on when the trial started.
		self.updateFishStimulus()
		
		#start timer to update experiment state
		self.bExperRunning = True

	def updateExperimentalState(self):
		bError = False
	
		if self.bExperRunning:
			try:
				if self.nTrial < self.nNumTrials:
					if self.nTrial>=0:
						self.statusBar().showMessage('NextTrial# %d TimeTilNextTrial %f TrialTime %f' % (self.nTrial+1, self.timeOfNextTrial - time.time(), time.time() - self.avoidData['trials'][self.nTrial]['startT']))
					else:
						self.statusBar().showMessage('NextTrial# %d TimeTilNextTrial %f' % (self.nTrial+1, self.timeOfNextTrial - time.time()))
				 
					self.avoidData['video'].append((self.frameTime, None)) 
					self.avoidData['tracking'].append((self.frameTime, self.fishPos[0], self.fishPos[1]))
							
					#determine if the fish has escaped a shock event
					escapeLine = self.arenaDivideLine
					bDidEscape = False
					if self.bCanEscape and (self.currState == cs_LED or self.currState == cs_SHOCK):
						if self.trialSide == cSide1:
							escapeLine = self.side1EscapeLine
							escapeSideSign = self.side1EscapeSign
						else:
							escapeLine = self.side2EscapeLine
							escapeSideSign = self.side2EscapeSign
						bDidEscape = self.isOnSide(self.fishPos, escapeLine, escapeSideSign)
												 
					#manage State Changes
					if(self.currState==cs_BETWEEN):
						if(time.time() >= self.timeOfNextTrial): 
							self.nTrial+=1
							#check if there are any trials remaining...
							if self.nTrial < self.nNumTrials:
								if self.nTrial == self.nNumTrials-1:
									#if last trial, then switch to test trial...
									self.currTrialType = ct_TESTTRIAL
								self.timeOfNextTrial = self.timeOfNextTrial + random.randint(self.fMinBetweenTrials,self.fMaxBetweenTrials)/1000.0
								self.currState = cs_LED;
								self.trialSide = self.currSide;
								self.timeState = time.time();
								self.bDidEscape = False
								bSuccess = self.updateFishStimulus()
								if not bSuccess: raise NameError('Fish stimulus failed to update.')
								self.avoidData['trials'].append({'trialNum':self.nTrial,
															'trialType':self.currTrialType,
															'startT':self.timeState,
															'side':self.currSide,
															'endT':-1})
					elif(self.currState==cs_LED):  
						if bDidEscape: 
							self.currState=cs_BETWEEN;
							self.timeState = time.time();
							bSuccess = self.updateFishStimulus()
							if not bSuccess: raise NameError('Fish stimulus failed to update.')
							self.avoidData['trials'][self.nTrial]['endT'] = self.timeState
							self.avoidData['trials'][self.nTrial]['bAvoidedShock'] = True
							self.outputExperimentUpdate()
						elif((time.time() - self.timeState) > self.fMaxLED/1000.0):   
							self.currState= cs_SHOCK;
							self.timeState = time.time();
							bSuccess = self.updateFishStimulus()
							if not bSuccess: raise NameError('Fish stimulus failed to update.')
							self.avoidData['trials'][self.nTrial]['bAvoidedShock'] = False
					elif(self.currState==cs_SHOCK):
						#End shock state when fish switchs sides or when has elapsed.
						if bDidEscape or time.time() - self.timeState > self.fMaxShock/1000.0:
							self.currState=cs_BETWEEN;
							self.timeState = time.time();
							bSuccess = self.updateFishStimulus()
							if not bSuccess: raise NameError('Fish stimulus failed to update.')
							self.avoidData['trials'][self.nTrial]['endT'] = self.timeState
							self.outputExperimentUpdate()
				else:
					#write the experimental data to disk
					f = open(name=self.jsonFileName, mode='w')
					json.dump(self.avoidData,f)
					f.close()
					self.bExperRunning = False
					#Clean up	
			except:
				#Clean up
				
				#write the experimental data to disk
				f = open(name=self.jsonFileName, mode='w')
				json.dump(self.avoidData,f)
				f.close()
				self.bExperRunning = False
				print 'Exception during experiment.  Saved and ended experiment prematurely.'
				print "Unexpected error:", sys.exc_info()[0]
				raise
		
	def updateFishStimulus(self):
		#Set up Pulsed Shock
		if not self.bPulsed:
			shockSide1 = cmd_SHOCK_SIDE1
			shockSide2 = cmd_SHOCK_SIDE2
		else:
			shockSide1 = cmd_PULSESHOCK_SIDE1
			shockSide2 = cmd_PULSESHOCK_SIDE2
		
		#Set up cue on Opposite Side if necessary
		led1On = cmd_LED_1_ON
		led1Off = cmd_LED_1_OFF
		led2On = cmd_LED_2_ON
		led2Off = cmd_LED_2_OFF
		if self.bLedOnOppositeSide:
			led1On = cmd_LED_2_ON
			led1Off = cmd_LED_2_OFF
			led2On = cmd_LED_1_ON
			led2Off = cmd_LED_1_OFF	
			
		#Set up shock only trials	
		if self.currTrialType == ct_SHOCK_ONLY:
			led1On = cmd_LED_1_OFF
			led1Off = cmd_LED_1_OFF
			led2On = cmd_LED_2_OFF
			led2Off = cmd_LED_2_OFF							
		 
		neurtralStimulus = AvoidanceStimuli.cWHITE
		fearStimulus = AvoidanceStimuli.cRED
		
		if self.currState==cs_BETWEEN:
			#ser.write(led1Off+led2Off+cmd_SHOCK_OFF+cmd_END)
			self.visStimWin.updateTankDisplay(neurtralStimulus,neurtralStimulus)
			self.ser.write(cmd_SHOCK_OFF+cmd_END)
			return self.confirmUpdate()
		elif self.currState==cs_LED or (self.currState==cs_SHOCK and (self.currTrialType == ct_TESTTRIAL or self.currTrialType == ct_UNPAIREDTRIAL)):  
			if(self.trialSide == cSide1): 
				#self.ser.write(led1On+led2Off+cmd_SHOCK_OFF+cmd_END)
				self.visStimWin.updateTankDisplay(fearStimulus,neurtralStimulus)
				self.ser.write(cmd_SHOCK_OFF+cmd_END)
				return self.confirmUpdate()
			elif(self.trialSide == cSide2):
				#ser.write(led2On+led1Off+cmd_SHOCK_OFF+cmd_END)
				self.visStimWin.updateTankDisplay(neurtralStimulus,fearStimulus)
				self.ser.write(cmd_SHOCK_OFF+cmd_END)
				return self.confirmUpdate()
		elif self.currState==cs_SHOCK and self.currTrialType == ct_PAIREDTRIAL:
			if(self.trialSide == cSide1): 
				#ser.write(led1On+led2Off+shockSide1+cmd_END)
				self.visStimWin.updateTankDisplay(fearStimulus,neurtralStimulus)
				self.ser.write(shockSide1+cmd_END)
				return self.confirmUpdate()
			elif(self.trialSide == cSide2): 
				#ser.write(led2On+led1Off+shockSide2+cmd_END)
				self.visStimWin.updateTankDisplay(neurtralStimulus,fearStimulus)
				self.ser.write(shockSide2+cmd_END)
				return self.confirmUpdate()
		return False
	
	#verify that the arduino is recieving the commands we send
	def confirmUpdate(self):
		startT = time.time();
		while time.time() - startT < .25:
			if(self.ser.inWaiting() > 0):
				if(self.ser.read() == cmd_END):
					return True
		return False    
	   
	def outputExperimentUpdate(self):
		ctNum = len(self.avoidData['trials'])-1
		#aa.plotTrialTimeByDistFromLED(avoidData,ctNum)
		print 'Trial Num %d Duration %f Side# %d' % (ctNum, self.avoidData['trials'][ctNum]['endT'] - self.avoidData['trials'][ctNum]['startT'], self.avoidData['trials'][ctNum]['side'])
					
def main(): 
    app = QtGui.QApplication(sys.argv)
    ex = AvoidanceLearningController()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()