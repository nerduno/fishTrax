# Learned Helplessness Free Manager
"""
AA 2012.07.25
Summary:
Run the free swimming protocol to induce learned helplessness.

Summary:
1. Establishes a serial port connection with the Arduino sketch 'AvoidanceLearningFree' to control shocks.
2. Establishes connection with AVT camera via OpenCV highgui (a slow but easy method)
3. Displays GUI for running avoidance learning using PyQt4
4. Creates second window to be placed on projector for fish visual stimulus.
5. Save experimental data in JSON format.

The protocol consists of delivering a series of shock at random unpredictable intervals.
"""

#IMPORTANT NOTE cvImg are pointers and can be modifed even if passed to a function.
#IMPORTANT NOTE cv.QueryImage returns a pointer to the same memory on every call (thus clone)

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
import AvoidanceArduinoController as aac
from AvoidanceStimuli import AvoidanceStimuli
from AvoidanceCameraManagement import CameraDevice
from OpenCVQImage import OpenCVQImage

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

class FishTrackingDisplay(QtGui.QLabel):
	clicked = QtCore.pyqtSignal(int, int)

	def __init__(self, parent=None):
		super(FishTrackingDisplay, self).__init__(parent)
		print 't'	
		
	def mousePressEvent(self, ev):
		self.clicked.emit(ev.x(), ev.y())

class LearnedHelplessnessController(QtGui.QMainWindow):
	dilateKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)
	erodeKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)

	# Constants for managing avoidance task state
	cs_BETWEEN = 0
	cs_LED = 1
	cs_SHOCK = 2
	cs_POST = 3
	cs_END = 4
	cSide1 = 0
	cSide2 = 1


	def __init__(self):
		super(LearnedHelplessnessController, self).__init__()

		self.cam = None
		self.ard = None
		self.nDispMode = 0
		self.currCvFrame = None
		self.bcvImg = None
		self.fishImg = None
		self.currG = None
		self.tracG = None
		self.debugG = None
		self.currArenaClick = 0
		self.bProtocolRunning = False

		#arena
		self.arenaCorners = []
		self.arenaCvMask = None

		#fish info
		self.fishSize = None

		#fish tracking parameters
		self.nThreshold = 5
		self.nDilate = 0
		self.nErode = 0
		self.minFishArea = 0 #the minimum blob size
		self.maxFishArea = 600000 #the maximum blob size

		#experiment parameters ##ms
		self.user_nNumShockBouts = 10
		self.user_nBoutDuration = 1000 #ms
		self.user_acclimationtime = 30000 #ms
		self.user_minBetweenBouts = 5000 #ms
		self.user_maxBetweenBouts = 10000 #ms

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

		self.startProtocolAction = QtGui.QAction('Start LH Protocol',self)
		#startExpAction.setStatusTip('Start an avoidance learning experiment.')
		self.startProtocolAction.triggered.connect(self.startLHProtocol)

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
		self.toolbar.addAction(self.startProtocolAction)

		self.acclimationtime_hbox = QtGui.QHBoxLayout()
		self.acclimationtime_label = QtGui.QLabel('Acclimation Time: ')
		self.acclimationtime_editbox = QtGui.QLineEdit()
		self.acclimationtime_editbox.setText(str(self.user_acclimationtime))
		self.acclimationtime_editbox.editingFinished.connect(self.updateAccTime)
		self.acclimationtime_hbox.addWidget(self.acclimationtime_label)
		self.acclimationtime_hbox.addWidget(self.acclimationtime_editbox)
		self.acclimationtime_widget = QtGui.QWidget()
		self.acclimationtime_widget.setLayout(self.acclimationtime_hbox)

		self.numbouts_hbox = QtGui.QHBoxLayout()
		self.numbouts_label = QtGui.QLabel('Number of Shock Bouts: ')
		self.numbouts_editbox = QtGui.QLineEdit()
		self.numbouts_editbox.setText(str(self.user_nNumShockBouts))
		self.numbouts_editbox.editingFinished.connect(self.updateNumBouts)
		self.numbouts_hbox.addWidget(self.numbouts_label)
		self.numbouts_hbox.addWidget(self.numbouts_editbox)
		self.numbouts_widget = QtGui.QWidget()
		self.numbouts_widget.setLayout(self.numbouts_hbox)

		self.boutduration_hbox = QtGui.QHBoxLayout()
		self.boutduration_label = QtGui.QLabel('Shock Bout Duration: ')
		self.boutduration_editbox = QtGui.QLineEdit()
		self.boutduration_editbox.setText(str(self.user_nBoutDuration))
		self.boutduration_editbox.editingFinished.connect(self.updateBoutDuration)
		self.boutduration_hbox.addWidget(self.boutduration_label)
		self.boutduration_hbox.addWidget(self.boutduration_editbox)
		self.boutduration_widget = QtGui.QWidget()
		self.boutduration_widget.setLayout(self.boutduration_hbox)

		self.maxBetweenBouts_hbox = QtGui.QHBoxLayout()
		self.maxBetweenBouts_label = QtGui.QLabel('Max Between Bouts: ')
		self.maxBetweenBouts_editbox = QtGui.QLineEdit()
		self.maxBetweenBouts_editbox.setText(str(self.user_maxBetweenBouts))
		self.maxBetweenBouts_editbox.editingFinished.connect(self.updateMaxBetweenBouts)
		self.maxBetweenBouts_hbox.addWidget(self.maxBetweenBouts_label)
		self.maxBetweenBouts_hbox.addWidget(self.maxBetweenBouts_editbox)
		self.maxBetweenBouts_widget = QtGui.QWidget()
		self.maxBetweenBouts_widget.setLayout(self.maxBetweenBouts_hbox)

		self.minBetweenBouts_hbox = QtGui.QHBoxLayout()
		self.minBetweenBouts_label = QtGui.QLabel('Min Between Bouts: ')
		self.minBetweenBouts_editbox = QtGui.QLineEdit()
		self.minBetweenBouts_editbox.setText(str(self.user_minBetweenBouts))
		self.minBetweenBouts_editbox.editingFinished.connect(self.updateMinBetweenBouts)
		self.minBetweenBouts_hbox.addWidget(self.minBetweenBouts_label)
		self.minBetweenBouts_hbox.addWidget(self.minBetweenBouts_editbox)
		self.minBetweenBouts_widget = QtGui.QWidget()
		self.minBetweenBouts_widget.setLayout(self.minBetweenBouts_hbox)

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

		self.ftDisp = FishTrackingDisplay() #this label will be used to display video
		self.ftDisp.setAlignment(QtCore.Qt.AlignLeft)  

		self.vbox = QtGui.QVBoxLayout()
		self.vbox.addWidget(self.acclimationtime_widget)
		self.vbox.addWidget(self.numbouts_widget)
		self.vbox.addWidget(self.boutduration_widget)
		self.vbox.addWidget(self.minBetweenBouts_widget)
		self.vbox.addWidget(self.maxBetweenBouts_widget)
		self.vbox.addWidget(self.threshLabel)
		self.vbox.addWidget(self.threshUp)
		self.vbox.addWidget(self.threshDown)
		self.vbox.addWidget(self.erodeLabel)
		self.vbox.addWidget(self.erodeUp)
		self.vbox.addWidget(self.erodeDown)
		self.vbox.addWidget(self.dilateLabel)
		self.vbox.addWidget(self.dilateUp)
		self.vbox.addWidget(self.dilateDown)
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
		self.setWindowTitle('Free Swimming Learned Helplessness')

		#Init to the status bar
		self.statusBar().showMessage('No camera connected. Click on camera connect.')
		self.show()

	def closeEvent(self, event):
		if self.visStimWin: 
			self.visStimWin.close()

	def connectToCamera(self):
		cameraId, ok = QtGui.QInputDialog.getInt(self, 'Camera Info', 'Enter a Camera ID (try 0,1,-1, or 2):', value=0)
		if ok:
			self.cam = CameraDevice(cameraId=cameraId, parent=self)
			self.cam.newFrame.connect(self.onNewFrame)
			self.cam.paused = False
			self.statusBar().showMessage('Camera connected.')

	def connectToArduino(self):
		portName, ok = QtGui.QInputDialog.getText(self, 'Arduino Port', 'Enter the arduino port:', text=aac.AvoidanceArduinoController.static_getDefaultPortName())
		portName = str(portName)
		self.statusBar().showMessage('Restart the arduino to complete the connection.')
		if self.ard == None:
			self.ard = aac.AvoidanceArduinoController(portName=portName) 
		else:
			self.ard.connect(portName=portName)
		
		if self.ard.isConnected():
			self.statusBar().showMessage('Arduino connected.')
		else:
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
				self.getArenaMask()

	#convert the arena corners into a color mask image (arena=255, not=0)    
	def getArenaMask(self): 
		cvImg = self.currCvFrame
		self.arenaCvMask = cv.CreateImage((cvImg.width,cvImg.height), cvImg.depth, cvImg.channels) 
		cv.SetZero(self.arenaCvMask)
		cv.FillConvexPoly(self.arenaCvMask, self.arenaCorners, (255,)*cvImg.channels)	
		self.maskG = cv.CreateImage((self.arenaCvMask.width, self.arenaCvMask.height), cv.IPL_DEPTH_8U, 1)
		cv.CvtColor(self.arenaCvMask, self.maskG, cv.CV_BGR2GRAY)

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

	def playpause(self):
		if not self.cam==None:
			self.cam.paused = not self.cam.paused

	def nextDispMode(self):
		self.nDispMode = (self.nDispMode + 1) % 8
		
	def prevDispMode(self):
		self.nDispMode = (self.nDispMode - 1) % 8	

	def updateAccTime(self):
		tmp = self.acclimationtime_editbox.text()
		tmp = str(tmp)
		try:
			nAcclimationTime = int(tmp)		
			self.user_acclimationtime = nAcclimationTime
		except:
			self.acclimationtime_editbox.setText(str(self.user_acclimationtime))

	def updateNumBouts(self):
		tmp = self.numbouts_editbox.text()
		tmp = str(tmp) 	
		try:
			nNumShockBouts = int(tmp)		
			self.user_nNumShockBouts = nNumShockBouts
		except:
			self.numbouts_editbox.setText(str(self.user_nNumShockBouts))
			QtGui.QApplication.beep()

	def updateBoutDuration(self):
		tmp = self.boutduration_editbox.text()
		tmp = str(tmp)
		try:
			nBoutDuration = int(tmp)		
			self.user_nBoutDuration = nBoutDuration
		except:
			self.boutduration_editbox.setText(str(self.user_nBoutDuration))

	def updateMinBetweenBouts(self):
		tmp = self.minBetweenBouts_editbox.text()
		tmp = str(tmp)
		try:
			minBetweenBouts = int(tmp)		
			self.user_minBetweenBouts = minBetweenBouts
		except:
			self._editbox.setText(str(self.user_minBetweenBouts))

	def updateMaxBetweenBouts(self):
		tmp = self.maxBetweenBouts_editbox.text()
		tmp = str(tmp)
		try:
			maxBetweenBouts = int(tmp)		
			self.user_maxBetweenBouts = maxBetweenBouts
		except:
			self._editbox.setText(str(self.user_maxBetweenBouts))

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

	def startLHProtocol(self):
		if not self.bProtocolRunning:
			#Initialize experimental parameters
			self.fAcclimationTime = self.user_acclimationtime #ms
			self.nNumShockBouts = self.user_nNumShockBouts #ms
			self.nBoutDuration = self.user_nBoutDuration #ms
			self.minBetweenBouts = self.user_minBetweenBouts #ms
			self.maxBetweenBouts = self.user_maxBetweenBouts #ms
		
			#get experiment information	
			bSuccess = self.getExperimentInfo()
			if not bSuccess: return

			#initialize experimental output
			self.initExperimentalOutput()

			#initialize fish context
			self.visStimWin.updateTankDisplay(AvoidanceStimuli.cBLUE, AvoidanceStimuli.cBLUE)
			
			#initialize experiment state
			self.nShockBout = 0
			self.currState = self.cs_BETWEEN
			self.timeState = time.time() #time the current state was entered
			self.timeOfNextState = self.timeState + self.fAcclimationTime/1000.0	
			
			#start timer to update experiment state
			self.startProtocolAction.setText('Stop LH Protocol')
			self.bProtocolRunning = True
		else:
			self.startExpAction.setText('Start LH Protocol')
			self.bProtocolRunning = False

	def getExperimentInfo(self):
		if self.fishImg == None:
			Self.statusBar().showMessage('Please collect image of fish.')
			return False

		self.experDir = QtGui.QFileDialog.getExistingDirectory(caption="Select directory to save experimental data:",directory="/User/andalman/Documents/Stanford/Data/AvoidanceLearning")
		if self.experDir=='': return False
		self.experDir = str(self.experDir)
		
		self.experName, ok = QtGui.QInputDialog.getText(None, 'Experiment Name', 'Enter experiment file name: ')
		if not ok: return False		
		self.experName = str(self.experName)
		
		self.birthday = obtainDate('Enter fish birthday: ')  
		if self.birthday == None: return False
		
		self.fishStrain, ok = QtGui.QInputDialog.getText(None, 'Fish Strain', 'Enter fish strain: ')
		if not ok: return False
		
		self.shockV,ok = QtGui.QInputDialog.getDouble(None, 'Shock Voltage', 'Enter shock voltage:', 0,0,50)
		if not ok: return False
				
		self.jsonFileName = self.experDir + os.sep +  self.experName + '_lh_' + time.strftime('%Y%m%d%H%M%S') + '.json'
		return True

	def initExperimentalOutput(self):
		#prepare output data structure
		self.lhData = {}
		self.lhData['fishbirthday'] = str(self.birthday)
		self.lhData['fishage'] =  (datetime.date.today() - self.birthday).days
		self.lhData['fishstrain'] = str(self.fishStrain)
		self.lhData['parameters'] = { 'nNumShockBouts':self.nNumShockBouts,
									'nBoutDuration':self.nBoutDuration,
									'minBetweenBouts':self.minBetweenBouts,
									'maxBetweenBouts':self.maxBetweenBouts,
									'AcclimationTime':self.fAcclimationTime,
									'CodeVersion':None }
		self.lhData['trackingParameters'] = {}
		self.lhData['shockWindows'] = list() #list of tuples (startShockTime, startShockTime)
		self.lhData['tracking'] = list() #list of tuples (frametime, posx, posy)
		self.lhData['video'] = list() #list of tubles (frametime, filename)	
		self.lhData['trackingParameters']['arenaPoly'] = self.arenaCorners
		self.lhData['trackingParameters']['nDiffThreshold'] = self.nThreshold
		self.lhData['trackingParameters']['nErode'] = self.nErode
		self.lhData['trackingParameters']['nDilate'] = self.nDilate
		self.lhData['fishsize'] = self.fishSize	
		self.bcvImgFileName = self.experDir + os.sep +  self.experName + '_BackImg.tiff'
		cv.SaveImage(self.bcvImgFileName, self.bcvImg)	
		self.fishImgFileName = self.experDir + os.sep +  self.experName + '_FishImg.tiff'
		cv.SaveImage(self.fishImgFileName, self.fishImg)

	def onNewFrame(self, frame):
		self.frameTime = time.time()
		self.currCvFrame = cv.CloneImage(frame)
		
		#update fish position
		self.updateFishPosition()
		
		#update experimental state
		if self.bProtocolRunning:
			self.updateProtocolState()
	
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
							
			#draw fish location
			if self.foundFish == True:
				fishColor = 'red'
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
			cv.Erode(self.thrsMG, self.tracEG, self.erodeKernal, self.nErode) #erode
			cv.Dilate(self.tracEG, self.tracDG, self.dilateKernal, self.nDilate) #dilate
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
				else:
					self.foundFish = False
					self.fishPos = (0,0)
					
			else:
				self.foundFish = False
				self.fishPos = (0,0)
			del seq
	
	def updateProtocolState(self):
		bSuccess = True
		try:
			if not self.currState == self.cs_END:
				self.statusBar().showMessage('nShockBout %d / %d' % (self.nShockBout, self.nNumShockBouts))

				self.lhData['video'].append((self.frameTime, None)) 
				self.lhData['tracking'].append((self.frameTime, self.fishPos[0], self.fishPos[1]))

				#manage State Changes
				if(time.time() >= self.timeOfNextState): 
					self.timeState = time.time()
					if(self.currState==self.cs_BETWEEN):
						bSuccess = self.ard.sendMessage(aac.cmd_PULSESHOCK_SIDE1)
						self.nShockBout+=1
	   					self.currState = self.cs_SHOCK
						self.timeOfNextState = self.timeState + self.nBoutDuration/1000.0
						self.lhData['shockWindows'].append({'startT':self.timeState,
															   'endT':-1})
					elif(self.currState==self.cs_SHOCK):  
						bSuccess = self.ard.sendMessage(aac.cmd_SHOCK_OFF)
						self.lhData['shockWindows'][self.nShockBout-1]['endT'] = self.timeState
						#write the experimental data to disk
						f = open(name=self.jsonFileName, mode='w')
						json.dump(self.lhData,f)
						f.close()
						if self.nShockBout < self.nNumShockBouts:
							self.timeOfNextState = self.timeState + random.randint(self.minBetweenBouts,self.maxBetweenBouts)/1000.0
							self.currState=self.cs_BETWEEN
						else:
							self.timeOfNextState = self.timeState + 120
							self.currState=self.cs_POST
					elif(self.currState==self.cs_POST):
						self.currState=self.cs_END

					if not bSuccess:
						1/0
   			else:
				#write the experimental data to disk
				f = open(name=self.jsonFileName, mode='w')
				json.dump(self.lhData,f)
				f.close()
				self.bProtocolRunning = False
				self.startProtocolAction.setText('Start LH Protocol')
				print 'Protocol completed successfully.  Saved experimental data.'
				#Clean up	
		except:
			#Clean up
			#write the experimental data to disk
			f = open(name=self.jsonFileName, mode='w')
			json.dump(self.lhData,f)
			f.close()
			self.bProtocolRunning = False
			self.startProtocolAction.setText('Start LH Protocol')
			print 'Exception during experiment.  Saved and ended experiment prematurely.'
			print "Unexpected error:", sys.exc_info()[0]
			raise

def main(): 
    app = QtGui.QApplication(sys.argv)
    ex = LearnedHelplessnessController()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


