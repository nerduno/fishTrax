# Avoidance Learning Free Manager
"""
AA 2011.08.05
Summary:
Run the free swimming avoidance learning protocol.

Summary:
1. Establishes a serial port connection with the Arduino sketch 'AvoidanceLearningFree' to control shocks.
2. Establishes connection with AVT camera via OpenCV highgui (a slow but easy method)
3. Displays GUI for running avoidance learning using PyQt4
4. Creates second window to be placed on projector for fish visual stimulus.
5. Save experimental data in JSON format.

Each experiment consists of a series of randomly spaced trials.  A trials involves:
1. Turning on a visual cue on the same side of the fish.
2. Leaving the cue on for N seconds or until the fish swims to the opposite side of the tank.
3. If the LED remains on for N seconds, a shock begins on the side where the fish is.
4. The shock persists for M seconds, or until the fish swims to the opposite side of the tank.
"""

#IMPORTANT NOTE cvImg are pointers and can be modifed even if passed to a function.
#IMPORTANT NOTE cv.QueryImage returns a pointer to the same memory on every call (thus clone)

#TODO Factorize fish tracking
#TODO track multiple fish for social behavior - average proximity (or
#three chamber) 
#TODO switch to Cython around PvAVT and optimize image processing for higher frame rate
#TODO Optimize cvImages, cvMats, or maybe just switch to NumPy arrays.
#TODO Try averaging frames to get background image?

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
#import matplotlib as mpl
#import matplotlib.pyplot as pyp
from PyQt4 import QtGui
from PyQt4 import QtCore
import pdb
import AvoidanceArduinoController as aac
from AvoidanceStimuli import AvoidanceStimuli
from AvoidanceCameraManagement import CameraDevice
from OpenCVQImage import OpenCVQImage

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

class AvoidanceLearningController(QtGui.QMainWindow):

    def __init__(self):
        super(AvoidanceLearningController, self).__init__()

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

        #experiment parameters ##ms
        self.user_nNumTrials = 30
        self.user_acclimationtime = 300000
        self.user_maxLED = 10000
        self.user_maxShock = 20000 
        self.user_minbetweentrials = 20000
        self.user_maxbetweentrials = 45000

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

        self.startExpAction = QtGui.QAction('Start Experiment',self)
        #startExpAction.setStatusTip('Start an avoidance learning experiment.')
        self.startExpAction.triggered.connect(self.startExperiment)

        self.startYokeAction = QtGui.QAction('Start Yoked Control',self)
        self.startYokeAction.triggered.connect(self.startYokedControl)

        self.startTrackAction = QtGui.QAction('Start SaveTrack',self)
        #self.startTrackAction.setStatusTip('Start/Stop saving position tracking only.')
        self.startTrackAction.triggered.connect(self.startstopSavingPosition)

        self.startSaveFrameAction = QtGui.QAction('Start SaveFrames',self)
        self.startSaveFrameAction.triggered.connect(self.startstopSavingFrames)

        self.startShockAction = QtGui.QAction('Shock Fish', self)
        self.startShockAction.triggered.connect(self.startShocks)

        self.setMinAction = QtGui.QAction('Set Minimum Time Between Trials', self)
        self.setMinAction.triggered.connect(self.setMinMethod)

        self.setMaxAction = QtGui.QAction('Set Maximum Time Between Trials', self)
        self.setMaxAction.triggered.connect(self.setMaxMethod)

        #box to set threshold, nErode and nDilate


        #button to startExperiment... connect to startExperiment.

        #Create the menu bar
        menubar = self.menuBar()
        fileMenu= menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(camAction)
        paramMenu= menubar.addMenu('&Parameters')
        paramMenu.addAction(self.setMinAction)
        paramMenu.addAction(self.setMaxAction)

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
        self.toolbar.addAction(self.startExpAction)
        self.toolbar.addAction(self.startYokeAction)
        self.toolbar.addAction(self.startTrackAction)
        self.toolbar.addAction(self.startShockAction)
        self.toolbar.addAction(self.startSaveFrameAction)

        #Create widgets for vertical panel
        debugBox = QtGui.QCheckBox('Use Debug Params')
        debugBox.resize(debugBox.sizeHint())
        debugBox.stateChanged.connect(self.debugMode)

        self.numtrials_hbox = QtGui.QHBoxLayout()
        self.numtrials_label = QtGui.QLabel('Number of Trials: ')
        self.numtrials_editbox = QtGui.QLineEdit()
        self.numtrials_editbox.editingFinished.connect(self.updateNumTrials)
        self.numtrials_hbox.addWidget(self.numtrials_label)
        self.numtrials_hbox.addWidget(self.numtrials_editbox)
        self.numtrials_widget = QtGui.QWidget()
        self.numtrials_widget.setLayout(self.numtrials_hbox)


        self.acclimationtime_hbox = QtGui.QHBoxLayout()
        self.acclimationtime_label = QtGui.QLabel('Acclimation Time: ')
        self.acclimationtime_editbox = QtGui.QLineEdit()
        self.acclimationtime_editbox.editingFinished.connect(self.updateAccTime)
        self.acclimationtime_hbox.addWidget(self.acclimationtime_label)
        self.acclimationtime_hbox.addWidget(self.acclimationtime_editbox)
        self.acclimationtime_widget = QtGui.QWidget()
        self.acclimationtime_widget.setLayout(self.acclimationtime_hbox)

        self.maxLED_hbox = QtGui.QHBoxLayout()
        self.maxLED_label = QtGui.QLabel('LED Time: ')
        self.maxLED_editbox = QtGui.QLineEdit()
        self.maxLED_editbox.editingFinished.connect(self.updatemaxLED)
        self.maxLED_hbox.addWidget(self.maxLED_label)
        self.maxLED_hbox.addWidget(self.maxLED_editbox)
        self.maxLED_widget = QtGui.QWidget()
        self.maxLED_widget.setLayout(self.maxLED_hbox)

        self.maxShock_hbox = QtGui.QHBoxLayout()
        self.maxShock_label = QtGui.QLabel('Max Shock Duration: ')
        self.maxShock_editbox = QtGui.QLineEdit()
        self.maxShock_editbox.editingFinished.connect(self.updatemaxShock)
        self.maxShock_hbox.addWidget(self.maxShock_label)
        self.maxShock_hbox.addWidget(self.maxShock_editbox)
        self.maxShock_widget = QtGui.QWidget()
        self.maxShock_widget.setLayout(self.maxShock_hbox)

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
        self.vbox.addWidget(self.numtrials_widget)
        self.vbox.addWidget(self.acclimationtime_widget)
        self.vbox.addWidget(self.maxLED_widget)
        self.vbox.addWidget(self.maxShock_widget)
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

    def closeEvent(self, event):
        if self.visStimWin: 
            self.visStimWin.close()

    def setMinMethod(self):
        nMinTime, ok = QtGui.QInputDialog.getInt(self, 'Minimum Time Between Trials', 'Set minimum time value (ms):', value=0, min = 0)
        if ok:
            self.user_minbetweentrials = nMinTime

    def setMaxMethod(self):
        nMaxTime, ok = QtGui.QInputDialog.getInt(self, 'Maximum Time Between Trials', 'Set maximum time value (ms):', value=0, min = 0)
        if ok:
            self.user_maxbetweentrials = nMaxTime

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

    def updateNumTrials(self):
        tmp = self.numtrials_editbox.text()
        tmp = str(tmp) 	
        try:
            nNumTrials = int(tmp)		
            self.user_nNumTrials = nNumTrials
        except:
            self.numtrials_editbox.setText(str(self.user_nNumTrials))
            QtGui.QApplication.beep()

    def updateAccTime(self):
        AccTime = self.acclimationtime_editbox.text()
        AccTime = str(AccTime)
        try:
            nAcclimationTime = int(AccTime)		
            self.user_acclimationtime = nAcclimationTime
        except:
            self.acclimationtime_editbox.setText(str(self.user_acclimationtime))

    def updatemaxLED(self):
        LEDTime = self.maxLED_editbox.text()
        LEDTime = str(LEDTime)
        try:
            nLEDTime = int(LEDTime)		
            self.user_maxLED = nLEDTime
        except:
            self.maxLED_editbox.setText(str(self.user_maxLED))

    def updatemaxShock(self):
        ShockTime = self.maxShock_editbox.text()
        ShockTime = str(ShockTime)
        try:
            nShockTime = int(ShockTime)		
            self.user_maxShock = nShockTime
        except:
            self.maxShock_editbox.setText(str(self.user_maxShock))

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
            print '1'
            self.frameDir = QtGui.QFileDialog.getExistingDirectory(caption="Select directory to save frames:")
            print '2'			
            if self.frameDir=='': return
            print '3'
            self.frameDir = str(self.frameDir)		
            self.startSaveFrameAction.setText('Stop SaveFrames')
            self.bSavingFrames = True
        else:
            self.startSaveFrameAction.setText('Start SaveFrames')
            self.bSavingFrames = False

    ## def stopExperiment(self):
        ## self.bExperRunning = False
        ## self.statusBar().showMessage('Experiment prematurely stopped.')



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
        bSuccess = self.ard.sendMessage(aac.cmd_PULSESHOCK_SIDE1+aac.cmd_LED_1_ON+aac.cmd_LED_2_OFF)
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
            bSuccess = self.ard.sendMessage(aac.cmd_PULSESHOCK_SIDE2+aac.cmd_LED_1_OFF+aac.cmd_LED_2_ON)
            self.shock_currSide = 2
            #TODO handle error
        else:
            bSuccess = self.ard.sendMessage(aac.cmd_PULSESHOCK_SIDE1+aac.cmd_LED_1_ON+aac.cmd_LED_2_OFF)
            self.shock_currSide = 1
            #TODO handle error

    def stopShocks(self):
        self.shockFlipTimer.stop()
        bSuccess = self.ard.sendMessage(aac.cmd_SHOCK_OFF+aac.cmd_LED_1_OFF+aac.cmd_LED_2_OFF)
        #TODO handle error

    def startYokedControl(self):
        if not self.bYokeRunning:
            #Request json file of experiment we are yokeing:
            self.yokeJsonFileName = self.experDir = QtGui.QFileDialog.getOpenFileName(caption="Select json file of experiment to be yoked:")
            if not self.yokeJsonFileName: return
            self.yokeJsonFileName = str(self.yokeJsonFileName)

            bSuccess = self.getExperimentInfo()
            if not bSuccess: return

                #Parse the json file...
            f = open(self.yokeJsonFileName)
            yokeJsonData = json.load(f)
            f.close()
            # need to turn trials information
            # into durations of each state: Between, LED, and shock...
            # need to turn shocks of somehow
            # set experimental parameters:

            #initialize experimental output
            self.initExperimentalOutput()
            # overwrite experimental output that is special for yoked control.

            #Initialize json output structure:

            self.statusBar().showMessage('Yoked control is not yet implemented.')

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

        self.jsonFileName = self.experDir + os.sep +  self.experName + time.strftime('%Y%m%d%H%M%S') + '.json'
        return True

    def initExperimentalOutput(self):
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

    def startExperiment(self):
        if not self.bExperRunning:
            #Initialize experimental parameters
            if not self.bDebug:
                self.currTrialType = ct_PAIREDTRIAL #this value remains the same for all but last trial 
                self.nNumTrials = self.user_nNumTrials
                self.fAcclimationTime = self.user_acclimationtime #ms
                self.fMinBetweenTrials = self.user_minbetweentrials #ms #180000
                self.fMaxBetweenTrials = self.user_maxbetweentrials #ms #240000
                self.fMaxLED = self.user_maxLED #ms
                self.fMaxShock = self.user_maxShock #000 #ms #the maximum duration of the shock.
                self.bPulsed = True #if true the fish is shock at regular intervals rather than continuously.
                self.bLedOnOppositeSide = False #if the True the LED appears on the opposite side of the fish
                self.bDiffuseLED = True #was there diffusion paper in front of the LED.
                self.fEscapePosition = .5 #the percent of the lenght the of the arena the fish must go from the LED
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
            bSuccess = self.getExperimentInfo()
            if not bSuccess: return

            #initialize experimental output
            self.initExperimentalOutput()

            #initialize experiment state
            self.currTrialType = ct_PAIREDTRIAL #this value remains the same for all but last trial 
            self.nTrial = -1
            self.currState = cs_BETWEEN
            self.timeState = time.time() #time the current state was entered
            self.timeOfNextTrial = self.timeState + self.fAcclimationTime/1000.0	
            self.trialSide = cSide1 #the side the fish was on when the trial started.
            self.updateFishStimulus()

            #start timer to update experiment state
            self.startExpAction.setText('Stop Experiment')
            self.bExperRunning = True
        else:
            self.startExpAction.setText('Start Experiment')
            self.bExperRunning = False


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
                            self.timeOfNextTrial = self.timeState + random.randint(self.fMinBetweenTrials,self.fMaxBetweenTrials)/1000.0
                            bSuccess = self.updateFishStimulus()
                            if not bSuccess: raise NameError('Fish stimulus failed to update.')
                            self.avoidData['trials'][self.nTrial]['endT'] = self.timeState
                            self.avoidData['trials'][self.nTrial]['bAvoidedShock'] = True
                            self.outputExperimentUpdate()
                            #write the experimental data to disk
                            f = open(name=self.jsonFileName, mode='w')
                            json.dump(self.avoidData,f)
                            f.close()
                        elif((time.time() - self.timeState) > self.fMaxLED/1000.0):   
                            self.currState= cs_SHOCK;
                            self.timeState = time.time();
                            bSuccess = self.updateFishStimulus()
                            if not bSuccess: raise NameError('Fish stimulus failed to update.')
                            self.avoidData['trials'][self.nTrial]['bAvoidedShock'] = False
                    elif(self.currState==cs_SHOCK):
                        #End shock state when fish switchs sides or when has elapsed.
                        if bDidEscape or time.time() - self.timeState > self.fMaxShock/1000.0:
                            self.currState=cs_BETWEEN
                            self.timeOfNextTrial = self.timeState + random.randint(self.fMinBetweenTrials,self.fMaxBetweenTrials)/1000.0
                            self.timeState = time.time();
                            bSuccess = self.updateFishStimulus()
                            if not bSuccess: raise NameError('Fish stimulus failed to update.')
                            self.avoidData['trials'][self.nTrial]['endT'] = self.timeState
                            self.outputExperimentUpdate()
                            #write the experimental data to disk
                            f = open(name=self.jsonFileName, mode='w')
                            json.dump(self.avoidData,f)
                            f.close()
                else:
                    #write the experimental data to disk
                    f = open(name=self.jsonFileName, mode='w')
                    json.dump(self.avoidData,f)
                    f.close()
                    self.bExperRunning = False
                    print 'Experiment completed successfully.  Saved experimental data.'
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
            shockSide1 = aac.cmd_SHOCK_SIDE1
            shockSide2 = aac.cmd_SHOCK_SIDE2
        else:
            shockSide1 = aac.cmd_PULSESHOCK_SIDE1
            shockSide2 = aac.cmd_PULSESHOCK_SIDE2

        #Set up cue on Opposite Side if necessary
        led1On = aac.cmd_LED_1_ON
        led1Off = aac.cmd_LED_1_OFF
        led2On = aac.cmd_LED_2_ON
        led2Off = aac.cmd_LED_2_OFF
        if self.bLedOnOppositeSide:
            led1On = aac.cmd_LED_2_ON
            led1Off = aac.cmd_LED_2_OFF
            led2On = aac.cmd_LED_1_ON
            led2Off = aac.cmd_LED_1_OFF	

        #Set up shock only trials	
        if self.currTrialType == ct_SHOCK_ONLY:
            led1On = aac.cmd_LED_1_OFF
            led1Off = aac.cmd_LED_1_OFF
            led2On = aac.cmd_LED_2_OFF
            led2Off = aac.cmd_LED_2_OFF							

        whiteStimulus = AvoidanceStimuli.cWHITE
        grayStimulus =  AvoidanceStimuli.cGRAY
        neurtralStimulus = AvoidanceStimuli.cBLUE
        redStimulus = AvoidanceStimuli.cRED
        pattern1Stimulus = AvoidanceStimuli.cLines
        pattern2Stimulus = AvoidanceStimuli.cCheckerboard

        if self.currState==cs_BETWEEN:
            #ser.write(led1Off+led2Off+aac.cmd_SHOCK_OFF+aac.cmd_END)
            self.visStimWin.updateTankDisplay(redStimulus,redStimulus)
            return self.ard.sendMessage(aac.cmd_SHOCK_OFF)
        elif self.currState==cs_LED or (self.currState==cs_SHOCK and (self.currTrialType == ct_TESTTRIAL or self.currTrialType == ct_UNPAIREDTRIAL)):  
            if(self.trialSide == cSide1): 
                #ser.write(led1On+led2Off+aac.cmd_SHOCK_OFF+aac.cmd_END)
                self.visStimWin.updateTankDisplay(whiteStimulus,redStimulus)
                return self.ard.sendMessage(aac.cmd_SHOCK_OFF)
            elif(self.trialSide == cSide2):
                #ser.write(led2On+led1Off+aac.cmd_SHOCK_OFF+aac.cmd_END)
                self.visStimWin.updateTankDisplay(redStimulus,whiteStimulus)
                return self.ard.sendMessage(aac.cmd_SHOCK_OFF)
        elif self.currState==cs_SHOCK and self.currTrialType == ct_PAIREDTRIAL:
            if(self.trialSide == cSide1): 
                #ser.write(led1On+led2Off+shockSide1+aac.cmd_END)
                self.visStimWin.updateTankDisplay(whiteStimulus,redStimulus)
                return self.ard.sendMessage(shockSide1)
            elif(self.trialSide == cSide2): 
                #ser.write(led2On+led1Off+shockSide2+aac.cmd_END)
                self.visStimWin.updateTankDisplay(redStimulus,whiteStimulus)
                self.ard.sendMessage(shockSide2)
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
