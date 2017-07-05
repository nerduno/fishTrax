#----------------------------------------------------------------------------#
#  Imports
#----------------------------------------------------------------------------#
import sys
import os
import os.path 
import math
from math import cos, sin, radians, degrees, atan2
from threading import Lock #also could use semaphore or RLock or Condition or Event Queue
import random; random.seed()
import time
import serial
import logging
import datetime
import json
import cv
import numpy as np
from PyQt4 import QtGui
from PyQt4 import QtCore
import ipdb
import traceback
import ArenaController
from FishTrackerWidget import FishTrackerWidget
from utility_widgets import PathSelectorWidget
from utility_widgets import LabeledSpinBox

#----------------------------------------------------------------------------#
#  Constants
#----------------------------------------------------------------------------#

# Constants for managing avoidance task state
class State:
    OFF = 0
    ACCLIMATE = 1
    #PREINIT = 2 #shock reminder
    PRETEST = 3
    PREDONE = 4
    TRAIN = 5
    TRAINDONE = 6
    #POSTINIT = 7 #shock reminder
    POSTTEST = 8

class ContextualHelplessnessController(ArenaController.ArenaController):
    def __init__(self, parent, arenaMain):        
        super(ContextualHelplessnessController, self).__init__(parent, arenaMain)

        #calibration
        self.arenaCamCorners = []
        self.arenaMidLine = []
        self.arenaSide1Sign = 1
        self.arenaProjCorners = []
        self.fishImg = None #image of fish

        #tracking
        self.arenaCvMask = None   

        #state
        self.mutex = Lock()
        self.arenaData = None
        self.currState = State.OFF
        self.fishPosUpdate = False
        self.fishPos = (0,0)
        self.allFish = []
        self.fishSize = None

        #tracking related images
        self.currCvFrame = None

        #init UI
        #arena info group box
        self.arenaGroup = QtGui.QGroupBox(self)
        self.arenaGroup.setTitle('Arena Info')
        self.arenaLayout = QtGui.QGridLayout()
        self.arenaLayout.setHorizontalSpacing(3)
        self.arenaLayout.setVerticalSpacing(3)
        self.camCalibButton = QtGui.QPushButton('Set Cam Position')
        self.camCalibButton.setMaximumWidth(150)
        self.camCalibButton.clicked.connect(self.getArenaCameraPosition)      
        self.projGroup = QtGui.QGroupBox(self.arenaGroup)
        self.projGroup.setTitle('Projector Position')
        self.projLayout = QtGui.QGridLayout(self.projGroup)
        self.projLayout.setHorizontalSpacing(3)
        self.projLayout.setVerticalSpacing(3)
        self.projCalibButton = QtGui.QPushButton('Calibrate Projector Position')
        self.projCalibButton.setCheckable(True)
        self.projCalibButton.clicked.connect(self.projectorPositionChanged)
        self.projLayout.addWidget(self.projCalibButton,0,0,1,6)
        self.projPosL = QtGui.QLabel('Pos')
        self.projX = QtGui.QSpinBox()
        self.projX.setRange(0,1000)
        self.projX.setValue(250)
        self.projX.setMaximumWidth(50)
        self.projY = QtGui.QSpinBox()
        self.projY.setRange(0,1000)
        self.projY.setValue(250)
        self.projY.setMaximumWidth(50)
        self.projLayout.addWidget(self.projPosL,1,0)
        self.projLayout.addWidget(self.projX,1,1)
        self.projLayout.addWidget(self.projY,1,2)
        self.projX.valueChanged.connect(self.projectorPositionChanged)
        self.projY.valueChanged.connect(self.projectorPositionChanged)
        self.projSizeL = QtGui.QLabel('Size L,W')
        self.projLen = QtGui.QSpinBox()
        self.projLen.setRange(0,1000)
        self.projLen.setValue(220)
        self.projLen.setMaximumWidth(50)
        self.projWid = QtGui.QSpinBox()
        self.projWid.setRange(0,1000)
        self.projWid.setValue(115)
        self.projWid.setMaximumWidth(50)
        self.projLen.valueChanged.connect(self.projectorPositionChanged)
        self.projWid.valueChanged.connect(self.projectorPositionChanged)
        self.projLayout.addWidget(self.projSizeL,2,0)
        self.projLayout.addWidget(self.projLen,2,1)
        self.projLayout.addWidget(self.projWid,2,2)
        self.projRotL = QtGui.QLabel('Rotation')
        self.projRot = QtGui.QSpinBox()
        self.projRot.setRange(0,360)
        self.projRot.setValue(270)
        self.projRot.setMaximumWidth(50)
        self.projLayout.addWidget(self.projRotL,2,3)
        self.projLayout.addWidget(self.projRot,2,4)
        self.projRot.valueChanged.connect(self.projectorPositionChanged)
        
        self.tankLength = LabeledSpinBox(None, 'Tank Len (mm)', 0,100,46,60)
        self.projLayout.addWidget(self.tankLength, 3,0,1,2)
        self.tankWidth = LabeledSpinBox(None, 'Tank Wid (mm)', 0,100,21,60)
        self.projLayout.addWidget(self.tankWidth, 3,2,1,2)

        self.projLayout.setColumnStretch(6,1)
        self.projGroup.setLayout(self.projLayout)
        self.arenaLayout.addWidget(self.camCalibButton, 0,0)
        self.arenaLayout.addWidget(self.projGroup,1,0)
        self.arenaLayout.setColumnStretch(1,1)
        self.arenaGroup.setLayout(self.arenaLayout)

        #tracking group box
        self.trackWidget = FishTrackerWidget(self, self.arenaMain.ftDisp)

        self.startButton = QtGui.QPushButton('Start Switches')
        self.startButton.setMaximumWidth(150)
        self.startButton.setCheckable(True)
        self.startButton.clicked.connect(self.startSwitches)
      
        self.pauseButton = QtGui.QPushButton('Pause')
        self.pauseButton.setMaximumWidth(150)
        self.pauseButton.setCheckable(True)
        self.pauseButton.setDisabled(True)
        self.pauseButton.clicked.connect(self.pause)

        self.autoPauseCheckBox = QtGui.QCheckBox('AutoPause')

        #experimental parameters groupbox
        self.paramGroup = QtGui.QGroupBox()
        self.paramGroup.setTitle('Exprimental Parameters')
        self.paramLayout = QtGui.QGridLayout()
        self.paramLayout.setHorizontalSpacing(2)
        self.paramLayout.setVerticalSpacing(2)

        #high level flow - acclimate -> pretest -> [b/t] -> train -> [b/t] -> posttest 
        self.paramAcclimate = LabeledSpinBox(None, 'Acclimate (m)', 0, 240, 0, 60)
        self.paramLayout.addWidget(self.paramAcclimate, 0,0,1,2)
        self.paramBetweenTime = LabeledSpinBox(None,'BetweenTime (m)',0, 1440, 0, 60) #time between pre , train and post periods
        self.paramLayout.addWidget(self.paramBetweenTime,0,2,1,2)
        self.paramPreDuration = LabeledSpinBox(None,'PreTest (m)',0,120,15,60) #number of side switches pre test
        self.paramLayout.addWidget(self.paramPreDuration,1,0,1,2)
        self.paramPreOMR = QtGui.QCheckBox('PreOMR')
        self.paramPreOMR.setCheckState(2)
        self.paramLayout.addWidget(self.paramPreOMR,1,2,1,2)
        self.paramNumTrain = LabeledSpinBox(None,'NumTrain',0,500,30,60)
        self.paramLayout.addWidget(self.paramNumTrain,2,0,1,2)
        self.paramTrainOMR = QtGui.QCheckBox('TrainOMR')
        self.paramTrainOMR.setCheckState(2)
        self.paramLayout.addWidget(self.paramTrainOMR,2,2,1,2)
        self.paramPostDuration = LabeledSpinBox(None,'PostTest (m)',0,120,5,60) #number of side switches post teset
        self.paramLayout.addWidget(self.paramPostDuration,3,0,1,2)
        self.paramPostOMR = QtGui.QCheckBox('PostOMR')
        self.paramPostOMR.setCheckState(2)
        self.paramLayout.addWidget(self.paramPostOMR,3,2,1,2)

        #omr parameters  
        self.paramOMRInterval = LabeledSpinBox(None,'OMR Interval (s)',0,600,48,60) #time between OMR tests
        self.paramOMRDuration = LabeledSpinBox(None,'OMR Duration (s)',0,600,12,60) #duration of OMR tests
        self.paramOMRPeriod = LabeledSpinBox(None,'OMR Grating Period (mm)',0,50,5,60) #spacing between grating bars
        self.paramOMRDutyCycle = LabeledSpinBox(None, 'OMR DutyCycle %',0,100,50,60) #width of grating bars
        self.paramOMRVelocity = LabeledSpinBox(None, 'OMR Speed (mm/s)',0,50,5,60) #velocity of moving gratings.
        self.paramLayout.addWidget(self.paramOMRInterval,4,0,1,2)
        self.paramLayout.addWidget(self.paramOMRDuration,4,2,1,2)        
        self.paramLayout.addWidget(self.paramOMRPeriod,5,0,1,2) 
        self.paramLayout.addWidget(self.paramOMRDutyCycle,5,2,1,2)
        self.paramLayout.addWidget(self.paramOMRVelocity,6,0,1,2)

        #training parameters
        self.paramUSTime = LabeledSpinBox(None, 'US Time (s)', 1,3600,60,60)
        self.paramLayout.addWidget(self.paramUSTime,7,0,1,2)
        self.paramNeutralMinTime = LabeledSpinBox(None, 'Neutral Min (s)',1,3600,2,60)
        self.paramLayout.addWidget(self.paramNeutralMinTime, 8,0,1,2)
        self.paramNeutralMaxTime = LabeledSpinBox(None, 'Neutral Max (s)',1,3600,5,60)
        self.paramLayout.addWidget(self.paramNeutralMaxTime, 8,2,1,2)
        self.paramShockPeriod = LabeledSpinBox(None, 'Shock Period (ms)', 0,5000,1000,60)
        self.paramLayout.addWidget(self.paramShockPeriod, 9,0,1,2)
        self.paramShockDuration = LabeledSpinBox(None, 'ShockDuration (ms)', 0,1000,50,60)
        self.paramLayout.addWidget(self.paramShockDuration, 9,2,1,2)
        self.paramShockChan1 = LabeledSpinBox(None, 'ShockChan1', 0,10000,53,60)
        self.paramLayout.addWidget(self.paramShockChan1, 10,0,1,2)
        self.paramShockChan2 = LabeledSpinBox(None, 'ShockChan2', 0,10000,52,60)
        self.paramLayout.addWidget(self.paramShockChan2, 10,2,1,2)
        self.paramCurrChan1 = LabeledSpinBox(None, 'CurrChan Side 1', 0,16,15,60)
        self.paramLayout.addWidget(self.paramCurrChan1,11,0,1,2)
        self.paramCurrChan2 = LabeledSpinBox(None, 'CurrChan Side 2', 0,16,14,60)
        self.paramLayout.addWidget(self.paramCurrChan2,11,2,1,2)
        self.paramShockV = LabeledSpinBox(None, 'ShockV', 0,100, 5,60)
        self.paramLayout.addWidget(self.paramShockV, 12,0,1,2)

        #Colors
        (self.paramColorAcclimate,self.labelColorAcclimate) = self.getColorComboBox('AcclimateColor', 0)
        self.paramLayout.addWidget(self.paramColorAcclimate,13,0)
        self.paramLayout.addWidget(self.labelColorAcclimate,13,1)

        (self.paramColorPreTest,self.labelColorPreTest) = self.getColorComboBox('PreTestColor', 0)
        self.paramLayout.addWidget(self.paramColorPreTest,13,2)
        self.paramLayout.addWidget(self.labelColorPreTest,13,3)

        (self.paramColorTrain,self.labelColorTrain) = self.getColorComboBox('TrainColor', 0)
        self.paramLayout.addWidget(self.paramColorTrain,14,0)
        self.paramLayout.addWidget(self.labelColorTrain,14,1)

        (self.paramColorPostTest,self.labelColorPostTest) = self.getColorComboBox('PostTestColor', 0)
        self.paramLayout.addWidget(self.paramColorPostTest,14,2)
        self.paramLayout.addWidget(self.labelColorPostTest,14,3)

        (self.paramColorBetween,self.labelColorBetween) = self.getColorComboBox('BetweenColor', 0)
        self.paramLayout.addWidget(self.paramColorBetween,15,0)
        self.paramLayout.addWidget(self.labelColorBetween,15,1)

        (self.paramColorOMR,self.labelColorOMR) = self.getColorComboBox('OMRColor', 5)
        self.paramLayout.addWidget(self.paramColorOMR,15,2)
        self.paramLayout.addWidget(self.labelColorOMR,15,3)

        self.paramNumFish = LabeledSpinBox(None,'NumFish',1,10,1,60)
        self.paramLayout.addWidget(self.paramNumFish,16,0,1,2)

        self.paramGroup.setLayout(self.paramLayout)

        #Experimental info group
        self.infoGroup = QtGui.QGroupBox()
        self.infoGroup.setTitle('Experiment Info')
        self.infoLayout = QtGui.QGridLayout()
        self.infoLayout.setHorizontalSpacing(3)
        self.infoLayout.setVerticalSpacing(3)

        self.labelDir = QtGui.QLabel('Dir: ')
        self.infoDir = PathSelectorWidget(browseCaption='Experimental Data Directory')
        self.infoLayout.addWidget(self.labelDir,0,0)
        self.infoLayout.addWidget(self.infoDir,0,1)

        self.labelDOB = QtGui.QLabel('DOB: ')
        self.infoDOB = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.infoLayout.addWidget(self.labelDOB,1,0)
        self.infoLayout.addWidget(self.infoDOB,1,1)

        self.labelType = QtGui.QLabel('Line: ')
        self.infoType = QtGui.QLineEdit('Nacre')
        self.infoLayout.addWidget(self.labelType,2,0)
        self.infoLayout.addWidget(self.infoType,2,1)     

        self.infoFish = QtGui.QPushButton('Snap Fish Image')
        self.infoFish.clicked.connect(self.getFishSize)
        self.infoLayout.addWidget(self.infoFish,3,0,1,2)

        self.infoGroup.setLayout(self.infoLayout)

        self.settingsLayout = QtGui.QGridLayout()
        self.settingsLayout.addWidget(self.arenaGroup,0,0,1,2)
        self.settingsLayout.addWidget(self.trackWidget,1,0,1,2)
        self.settingsLayout.addWidget(self.infoGroup,3,0,1,2)
        self.settingsLayout.addWidget(self.startButton,4,0,1,1)
        self.settingsLayout.addWidget(self.pauseButton,5,0,1,1)
        self.settingsLayout.addWidget(self.autoPauseCheckBox,5,1,1,1)
        self.settingsLayout.addWidget(self.paramGroup,6,0,1,2)
        self.setLayout(self.settingsLayout)

        self.projectorPositionChanged()
        self.t = 0
#        self.omrPhase = 0
#        self.omrDirection = [1,0]

    def getColorComboBox(self, labelName, defaultNdx=1):
        colorBox = QtGui.QComboBox()
        colorBox.addItem('White')
        colorBox.addItem('Red')
        colorBox.addItem('Blue')
        colorBox.addItem('Gray')
        colorBox.addItem('Magenta')
        colorBox.addItem('Black')
        colorBox.setCurrentIndex(defaultNdx)
        colorLabel = QtGui.QLabel(labelName)
        return (colorBox,colorLabel)
    

    #---------------------------------------------------
    # OVERLOADED METHODS
    #---------------------------------------------------

    #update to overload an return image based on dispmode.
    #def getArenaView(self):
    #    return self.arenaView

    def onNewFrame(self, frame, time):
        self.mutex.acquire()
        try:
            self.frameTime = time
            self.currCvFrame = frame # may need to make a deep copy

            (found, pos, view, allFish) = self.trackWidget.findFish(self.currCvFrame)

            if found:
                self.fishPosUpdate = found
                self.fishPos = pos
                self.allFish = allFish

            if not self.currState == State.OFF:
                self.arenaData['video'].append((self.frameTime, None)) 
                d = [self.frameTime, pos[0], pos[1]]
                for nFish in range(1, min(self.paramNumFish.value(),len(allFish))):
                    d.append(allFish[nFish][0])
                    d.append(allFish[nFish][1])
                self.arenaData['tracking'].append(tuple(d))

            self.arenaView = view
        except:
            print 'ClassicalConditioningController:onNewFrame failed'
            traceback.print_exc()
            QtCore.pyqtRemoveInputHook() 
            ipdb.set_trace()
        finally:
            self.mutex.release()

  
    def updateState(self):
        self.updateExperimentalState()

    def startOMR(self):
        self.nextOMRTime = self.t + self.paramOMRInterval.value()
        self.bOMR = False
        self.omrDirection = (0,0)
        self.arenaData['OMRinfo'].append((self.t, self.bOMR, self.omrDirection))

    def updateOMR(self):
        if self.t > self.nextOMRTime :
            if self.bOMR:
                self.nextOMRTime = self.t + self.paramOMRInterval.value()
                self.bOMR = False
                self.omrDirection = (0,0)
            else:
                self.nextOMRTime = self.t + self.paramOMRDuration.value()
                self.bOMR = True
                self.omrPhase = 0
                self.omrLastUpdate = self.t
                if self.isOnSide(self.fishPos, self.arenaMidLine, self.arenaSide1Sign):
                    self.omrDirection = (1,0)
                else:
                    self.omrDirection = (-1,0)
            self.arenaData['OMRinfo'].append((self.t, self.bOMR, self.omrDirection))
            self.updateProjectorDisplay()

    def stopOMR(self):
        self.nextOMRTime = float('inf')
        self.bOMR = False
        self.omrDirection = (0,0)
        self.arenaData['OMRinfo'].append((self.t, self.bOMR, self.omrDirection))

    def updateExperimentalState(self):
#        if self.paramPreOMR.isChecked():
#            t = time.time()
#            self.lt = self.t
#            self.t = t
#            print self.t - self.lt
#            self.omrPhase += self.omrDirection[0] * (float(self.paramOMRVelocity.value())/float(self.paramOMRPeriod.value())) * 360.0 * (self.t-self.lt)
#            print self.omrPhase
#            if t - self.omrLastUpdate > 0.010:
#                #print t - self.omrLastUpdate
#                self.updateProjectorDisplay()


        if not self.currState == State.OFF:
            self.mutex.acquire()
            try:
                t = time.time()
                self.lt = self.t
                self.t = t

                #only update status bar if arena is selected.
                if self.isCurrent():
                    self.arenaMain.statusBar().showMessage('State %d'%(self.currState))

                if t > self.nextStateTime:
                    self.setShockState(False, False)
                    self.stopOMR()
                    self.bInShockBout = False
                    self.nextShockBoutTime = float('inf')
                    self.pauseButton.setDisabled(True)
                    if (self.currState <= State.ACCLIMATE
                        and self.paramPreDuration.value() > 0):
                        self.currState = State.PRETEST
                        self.nextStateTime = t + (self.paramPreDuration.value()*60)
                        if self.paramPreOMR.isChecked():
                            self.startOMR()                            
                    elif (self.currState <= State.PRETEST
                        and self.paramBetweenTime.value() > 0):
                        self.currState = State.PREDONE
                        self.nextStateTime = t + self.paramBetweenTime.value()*60
                        self.pauseButton.setDisabled(False)
                        if self.autoPauseCheckBox.isChecked():
                            self.pauseButton.setChecked(True)
                            self.doPause()
                    elif (self.currState <= State.PREDONE
                        and self.paramNumTrain.value() > 0):
                        self.currState = State.TRAIN
                        self.nextStateTime = float("inf")
                        self.numShock = 0; 
                        self.bInShockBout = False
                        self.nextShockBoutTime = t + random.uniform(self.paramNeutralMinTime.value(), self.paramNeutralMaxTime.value())                        
                        if self.paramTrainOMR.isChecked():
                            self.startOMR()                            
                    elif (self.currState <= State.TRAIN
                          and self.paramBetweenTime.value() > 0):
                        self.currState = State.TRAINDONE
                        self.nextStateTime = t + self.paramBetweenTime.value()*60
                        self.pauseButton.setDisabled(False)
                        if self.autoPauseCheckBox.isChecked():
                            self.pauseButton.setChecked(True)
                            self.doPause()
                    elif (self.currState <= State.TRAINDONE
                        and self.paramPostDuration.value() > 0):
                        self.currState = State.POSTTEST
                        self.nextStateTime = t + (self.paramPostDuration.value()*60) 
                        if self.paramPostOMR.isChecked():
                            self.startOMR()                            
                    elif self.currState <= State.POSTTEST:
                        self.currState = State.OFF
                        self.startButton.setText('Start Switches')
                        self.startButton.setChecked(False)
                        self.paramGroup.setDisabled(False)
                        self.infoGroup.setDisabled(False)
                        self.saveResults()
                    self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
                    self.updateProjectorDisplay()
                    self.saveResults()


                #handle omr state changes and projector updates
                self.updateOMR()
                if self.bOMR:
                    self.omrPhase += self.omrDirection[0] * (float(self.paramOMRVelocity.value())/float(self.paramOMRPeriod.value())) * 360.0 * (self.t-self.lt)
                    self.omrPhase = self.omrPhase%360.0
                    if t - self.omrLastUpdate > 0.010:
                        #if t - self.omrLastUpdate > 0.040:
                        #    print 'WARNING: projector slow to update', t - self.omrLastUpdate
                        self.updateProjectorDisplay()
               
                #handle training shock bout state changes
                if t > self.nextShockBoutTime:
                    if self.bInShockBout:
                        self.bInShockBout = False
                        self.setShockState(False,False)
                        self.numShock += 1                        
                        self.nextShockBoutTime = t + random.uniform(self.paramNeutralMinTime.value(),
                                                                    self.paramNeutralMaxTime.value())
                        if self.numShock >= self.paramNumTrain.value():
                            self.nextStateTime = t 
                    else:
                        self.bInShockBout = True
                        self.setShockState(True,True)
                        self.nextShockBoutTime = t + self.paramUSTime.value()
                    self.updateProjectorDisplay()
                    self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
            
            except:
                print 'ContextualHelplessnessController:updateState failed'
                traceback.print_exc()
                QtCore.pyqtRemoveInputHook() 
                ipdb.set_trace()
            finally:
                self.mutex.release()

    def isReadyToStart(self):
        return os.path.exists(self.infoDir.text()) and self.trackWidget.getBackgroundImage() and self.fishImg and self.arenaCamCorners

    def projectorPositionChanged(self):
        #the point defining the tank are such that:
        #points 1 and 2 define side1
        #points 2 and 3 define the 'near' connecting edge
        #points 3 and 4 define side2
        #points 4 and 1 define the 'far' connecting edge.
 
        #move this code elsewhere to avoid redundant computation...
        self.pts = np.array([[0                   , 0],
                             [0                   , self.projWid.value()],
                             [self.projLen.value(), self.projWid.value()],
                             [self.projLen.value(), 0]])
        theta = self.projRot.value()
        self.tankRotM = np.array([[cos(radians(theta)), -sin(radians(theta))],
                         [sin(radians(theta)),  cos(radians(theta))]]);
        self.pts = np.dot(self.tankRotM,self.pts.T).T
        self.pts += [self.projX.value(), self.projY.value()]
        self.updateProjectorDisplay()

    def drawProjectorDisplay(self, painter):
        if self.currState == State.OFF and self.projCalibButton.isChecked() and self.isCurrent():
            #DRAW A CALIBRATION IMAGE THAT INDICATES THE PROJECTOR LOCATION AND SIDE1
            side1Color = QtCore.Qt.red
            side2Color = QtCore.Qt.blue
            a = .5
            b = 1-a
            #Draw side one
            pen = QtGui.QPen(QtCore.Qt.NoPen)
            brush = QtGui.QBrush(side1Color)
            painter.setBrush(brush)
            painter.setPen(pen)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(self.pts[0,0], self.pts[0,1]))
            poly.append(QtCore.QPointF(self.pts[1,0], self.pts[1,1]))
            poly.append(QtCore.QPointF(a*self.pts[1,0] + b*self.pts[2,0], a*self.pts[1,1] + b*self.pts[2,1]))
            poly.append(QtCore.QPointF(a*self.pts[0,0] + b*self.pts[3,0], a*self.pts[0,1] + b*self.pts[3,1]))
            painter.drawPolygon(poly)
            painter.setPen(QtGui.QColor(168, 34, 3))
            painter.setFont(QtGui.QFont('Decorative',24))
            painter.drawText(self.pts[0,0],self.pts[0,1],'1')
            painter.drawText(self.pts[1,0],self.pts[1,1],'2')
            painter.drawText(self.pts[2,0],self.pts[2,1],'3')
            painter.drawText(self.pts[3,0],self.pts[3,1],'4')
            #Draw side two
            pen = QtGui.QPen(QtCore.Qt.NoPen)
            brush = QtGui.QBrush(side2Color)
            painter.setBrush(brush)
            painter.setPen(pen)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(a*self.pts[0,0] + b*self.pts[3,0], a*self.pts[0,1] + b*self.pts[3,1]))
            poly.append(QtCore.QPointF(a*self.pts[1,0] + b*self.pts[2,0], a*self.pts[1,1] + b*self.pts[2,1]))
            poly.append(QtCore.QPointF(self.pts[2,0], self.pts[2,1]))
            poly.append(QtCore.QPointF(self.pts[3,0], self.pts[3,1]))
            painter.drawPolygon(poly)
        else:
            if self.currState == State.OFF:
                #Draw whole tank
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                brush = QtGui.QBrush(QtCore.Qt.white)
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(self.pts[0,0], self.pts[0,1]))
                poly.append(QtCore.QPointF(self.pts[1,0], self.pts[1,1]))
                poly.append(QtCore.QPointF(self.pts[2,0], self.pts[2,1]))
                poly.append(QtCore.QPointF(self.pts[3,0], self.pts[3,1]))
                painter.drawPolygon(poly)
            else:
                side1Color = self.getSide1ColorNdx()
                side2Color = self.getSide2ColorNdx()
                a = .5
                b = 1-a
                #Draw side one
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                brush = self.getBrush(side1Color)
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(self.pts[0,0], self.pts[0,1]))
                poly.append(QtCore.QPointF(self.pts[1,0], self.pts[1,1]))
                poly.append(QtCore.QPointF(a*self.pts[1,0] + b*self.pts[2,0], a*self.pts[1,1] + b*self.pts[2,1]))
                poly.append(QtCore.QPointF(a*self.pts[0,0] + b*self.pts[3,0], a*self.pts[0,1] + b*self.pts[3,1]))
                painter.drawPolygon(poly)
                #Draw side two
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                brush = self.getBrush(side2Color)
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(a*self.pts[0,0] + b*self.pts[3,0], a*self.pts[0,1] + b*self.pts[3,1]))
                poly.append(QtCore.QPointF(a*self.pts[1,0] + b*self.pts[2,0], a*self.pts[1,1] + b*self.pts[2,1]))
                poly.append(QtCore.QPointF(self.pts[2,0], self.pts[2,1]))
                poly.append(QtCore.QPointF(self.pts[3,0], self.pts[3,1]))
                painter.drawPolygon(poly)
                #Draw OMR grating
                if self.bOMR:
                    self.omrLastUpdate = self.t                    
                    #This stuff doesn't need to computed on every frame
                    mm2pix = math.hypot(self.pts[2,0]-self.pts[1,0], self.pts[2,1] - self.pts[1,1]) / self.tankLength.value()
                    period = self.paramOMRPeriod.value() * mm2pix
                    numBars = int(math.ceil(math.hypot(self.pts[2,0]-self.pts[1,0], self.pts[2,1] - self.pts[1,1]) / period))
                    barWidth = period * (self.paramOMRDutyCycle.value()/100.0)
                    
                    #Draw the bar
                    phaseShift = self.omrPhase/360.0 * period  
                    pen = QtGui.QPen(QtCore.Qt.NoPen)
                    brush = self.getBrush(self.paramColorOMR.currentIndex())
                    painter.setBrush(brush)
                    painter.setPen(pen)
                    for nBar in range(-1,numBars+1):
                        #define bar in unrotated untranslated space.
                        bl = min(max(phaseShift + nBar * period, 0), self.projLen.value()) 
                        br = min(max(phaseShift + nBar * period + barWidth, 0), self.projLen.value()) 
                        bar = np.array([[br,0],
                                        [bl,0],
                                        [bl,self.projWid.value()],
                                        [br,self.projWid.value()]])
                        #rotate and tranlate.
                        bar = np.dot(self.tankRotM, bar.T).T + [self.projX.value(), self.projY.value()]
                        #draw
                        poly = QtGui.QPolygonF()
                        poly.append(QtCore.QPointF(bar[0,0],bar[0,1]))
                        poly.append(QtCore.QPointF(bar[1,0],bar[1,1]))
                        poly.append(QtCore.QPointF(bar[2,0],bar[2,1]))
                        poly.append(QtCore.QPointF(bar[3,0],bar[3,1]))
                        painter.drawPolygon(poly)

    def drawDisplayOverlay(self, painter):
        #draw the fish position
        if self.fishPos and self.fishPos[0] > 0:
            brush = QtGui.QBrush(QtCore.Qt.red)
            painter.setBrush(brush)
            painter.setPen(QtCore.Qt.NoPen)
            for nFish in range(min(len(self.allFish),self.paramNumFish.value())):
                painter.drawEllipse(QtCore.QPointF(self.allFish[nFish][0],self.allFish[nFish][1]), 3,3)

        #draw the arena overlay
        if self.arenaCamCorners:
            painter.setBrush(QtCore.Qt.NoBrush)
            if self.bIsCurrentArena:
                pen = QtGui.QPen(QtCore.Qt.green)
            else:
                pen = QtGui.QPen(QtCore.Qt.blue)
            pen.setWidth(3)
            painter.setPen(pen)
            poly = QtGui.QPolygonF()
            for p in self.arenaCamCorners:
                poly.append(QtCore.QPointF(p[0],p[1]))
            painter.drawPolygon(poly)
            if len(self.arenaCamCorners) >= 2:
                pen = QtGui.QPen(QtCore.Qt.red)
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawLine(self.arenaCamCorners[0][0],self.arenaCamCorners[0][1],
                                 self.arenaCamCorners[1][0],self.arenaCamCorners[1][1])
                painter.setPen(QtGui.QColor(168, 34, 3))
                painter.setFont(QtGui.QFont('Decorative',14))
                painter.drawText(self.arenaCamCorners[0][0],self.arenaCamCorners[0][1],str(self.currState))

    def start(self):
        #Global start button not used.
        pass

    def stop(self):
        #Global stop button not used.
        pass

    #---------------------------------------------------
    # CALLBACK METHODS
    #---------------------------------------------------
    def startSwitches(self):
        self.mutex.acquire()
        try:
            if self.currState == State.OFF:
                if self.isReadyToStart():
                    self.paramGroup.setDisabled(True)
                    self.infoGroup.setDisabled(True)
                    td = datetime.datetime.now()
                    self.saveLocation = str(self.infoDir.text())
                    [p, self.fnResults] = os.path.split(self.saveLocation)
                    self.fnResults = self.fnResults + '_' + td.strftime('%Y-%m-%d-%H-%M-%S')
                    self.jsonFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '.json'
                    self.initArenaData()
                    
                    t = time.time()
                    self.currState = State.ACCLIMATE
                    self.nextStateTime = t + self.paramAcclimate.value()*60
                    self.bInShockBout = False
                    self.nextShockBoutTime = float('inf')
                    self.setShockState(False,False)
                    self.stopOMR()
                    self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
                    self.updateProjectorDisplay()
                    self.startButton.setText('Stop')
                else:
                    self.startButton.setChecked(False)
                    self.arenaMain.statusBar().showMessage('Arena not ready to start.  Information is missing.')
            else: 
                t = time.time()
                self.currState = State.OFF
                self.nextStateTime = float('inf')
                self.bInShockBout = False
                self.nextShockBoutTime = float('inf')
                self.setShockState(False,False)
                self.stopOMR()
                self.startButton.setText('Start Switches')
                self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
                self.updateProjectorDisplay()
                self.saveResults()
                self.paramGroup.setDisabled(False) 
                self.infoGroup.setDisabled(False)
                self.pauseButton.setChecked(False)
        except:
            print 'ContextualHelplessnessController:startSwitches failed'
            traceback.print_exc()
            QtCore.pyqtRemoveInputHook() 
            ipdb.set_trace()
        finally:
            self.mutex.release()    

    def doPause(self):   
        t = time.time()
        if self.pauseButton.isChecked():
            self.arenaData['pauseinfo'].append((True, t))
            self.pausedRemainingTime = self.nextStateTime - t
            self.nextStateTime = float('inf')
        else:
            self.arenaData['pauseinfo'].append((False, t))
            self.nextStateTime = t + self.pausedRemainingTime

    def pause(self):
        self.mutex.acquire()
        try:
            self.doPause()
        except:
            print 'ContextualHelplessnessController: pause failed'
            traceback.print_exc()
            QtCore.pyqtRemoveInputHook() 
            ipdb.set_trace()
        finally:
            self.mutex.release()    
                
        
    def getArenaCameraPosition(self):
        self.arenaMain.statusBar().showMessage('Click on the corners of the arena on side 1.')
        self.currArenaClick = 0
        self.arenaCamCorners = []
        self.arenaMain.ftDisp.clicked.connect(self.handleArenaClicks) 

    @QtCore.pyqtSlot(int, int) #not critical but could practice to specify which functions are slots.
    def handleArenaClicks(self, x, y):
        self.currArenaClick+=1
        if self.currArenaClick<5:
            self.arenaCamCorners.append((x,y))
            if self.currArenaClick==1:
                self.arenaMain.statusBar().showMessage('Click on the other corner of the arena on side 1.')
            elif self.currArenaClick==2:
                self.arenaMain.statusBar().showMessage('Now, click on the corners of the arena on side 2.')
            elif self.currArenaClick==3:
                self.arenaMain.statusBar().showMessage('Click on the other corner of the arena on side 2.')	
            elif self.currArenaClick==4:
                self.arenaMain.ftDisp.clicked.disconnect(self.handleArenaClicks)
                self.arenaMain.statusBar().showMessage('')
                [self.arenaMidLine, self.arenaSide1Sign] = self.processArenaCorners(self.arenaCamCorners, .5)
                self.getArenaMask()

    def getFishSize(self):
        self.arenaMain.statusBar().showMessage('Click on the tip of the fish tail.')
        self.currFishClick = 0
        self.fishSize = []
        self.arenaMain.ftDisp.clicked.connect(self.handleFishClicks) 		

    @QtCore.pyqtSlot(int, int) #not critical but could practice to specify which functions are slots.
    def handleFishClicks(self, x, y):
        self.currFishClick+=1
        if self.currFishClick == 1:
            self.fishSize.append((x,y))
            self.arenaMain.statusBar().showMessage('Click on the tip of the fish head.')
        elif self.currFishClick == 2:
            self.arenaMain.ftDisp.clicked.disconnect(self.handleFishClicks)
            self.fishSize.append((x,y))
            self.fishImg = cv.CloneImage(self.currCvFrame)
            self.arenaMain.statusBar().showMessage('')

    #---------------------------------------------------
    # HELPER METHODS
    #---------------------------------------------------

    #def getBackgroundImage(self):
    #    if self.currCvFrame:
    #        self.bcvImg = cv.CloneImage(self.currCvFrame) 
    #        self.trackWidget.setBackgroundImage(self.bcvImg)

    def processArenaCorners(self, arenaCorners, linePosition):
        #return the line dividing the center of the arena, and a definition of side 1.
        a = 1-linePosition
        b = linePosition
        ac = np.array(arenaCorners)
        #arenaDivideLine = [tuple(np.mean(ac[(0,3),:],axis = 0)),tuple(np.mean(ac[(1,2),:],axis = 0))]
        arenaDivideLine = [(a*ac[0,0]+b*ac[3,0], a*ac[0,1]+b*ac[3,1]),(a*ac[1,0]+b*ac[2,0], a*ac[1,1]+b*ac[2,1])]
        side1Sign = 1
        if not self.isOnSide(arenaCorners[1], arenaDivideLine, side1Sign):
            side1Sign = -1	
        return (arenaDivideLine, side1Sign)

    def isOnSide(self, point, line, sideSign):
        #return if the fish is on side1 of the arena.   
        side = (line[1][0] - line[0][0]) * (point[1] - line[0][1]) - (line[1][1] - line[0][1]) * (point[0] - line[0][0])
        return cmp(side,0)==sideSign  

    #convert the arena corners into a color mask image (arena=255, not=0)    
    def getArenaMask(self): 
        if self.arenaView:
            cvImg = self.currCvFrame
            self.arenaCvMask = cv.CreateImage((cvImg.width,cvImg.height), cvImg.depth, cvImg.channels) 
            cv.SetZero(self.arenaCvMask)
            cv.FillConvexPoly(self.arenaCvMask, self.arenaCamCorners, (255,)*cvImg.channels)	
            self.trackWidget.setTrackMask(self.arenaCvMask)

    def initArenaData(self):
        #prepare output data structure
        self.arenaData = {}
        self.arenaData['fishbirthday'] = str(self.infoDOB.date().toPyDate())
        self.arenaData['fishage'] =  (datetime.date.today() - self.infoDOB.date().toPyDate()).days
        self.arenaData['fishstrain'] = str(self.infoType.text())
        self.arenaData['fishsize'] = self.fishSize
        self.arenaData['parameters'] = { 'preDuration':self.paramPreDuration.value(),
                                         'numTrain':self.paramNumTrain.value(),
                                         'postDuration':self.paramPostDuration.value(),
                                         'acclimate (m)':self.paramAcclimate.value(),
                                         'between (m)': self.paramBetweenTime.value(),
                                         'trainUStime': self.paramUSTime.value(),
                                         'trainNeutralMinTime':self.paramNeutralMinTime.value(),
                                         'trainNeutralMaxTime':self.paramNeutralMaxTime.value(),
                                         'shock period (ms)':self.paramShockPeriod.value(),
                                         'shock dura (ms)':self.paramShockDuration.value(),
                                         'shock chan 1':self.paramShockChan1.value(),
                                         'shock chan 2':self.paramShockChan2.value(),
                                         'shock V':self.paramShockV.value(),
                                         'OMR_pre':self.paramPreOMR.isChecked(),
                                         'OMR_train':self.paramTrainOMR.isChecked(),
                                         'OMR_post':self.paramPostOMR.isChecked(),
                                         'OMR_period':self.paramOMRPeriod.value(),
                                         'OMR_dutycycle':self.paramOMRDutyCycle.value(),
                                         'OMR_velocity':self.paramOMRVelocity.value(),
                                         'OMR_interval':self.paramOMRInterval.value(),
                                         'OMR_duration':self.paramOMRDuration.value(),
                                         'OMR_color':str(self.paramColorOMR.currentText()),
                                         'AcclimateColor':str(self.paramColorAcclimate.currentText()),
                                         'BetweenColor':str(self.paramColorBetween.currentText()),
                                         'PreTestColor':str(self.paramColorPreTest.currentText()),
                                         'TrainColor':str(self.paramColorTrain.currentText()),
                                         'PostTestColor':str(self.paramColorPostTest.currentText()),
                                         'numFish': self.paramNumFish.value(),
                                         'CodeVersion':None }
        self.arenaData['trackingParameters'] = self.trackWidget.getParameterDictionary()
        self.arenaData['trackingParameters']['arenaPoly'] = self.arenaCamCorners 
        self.arenaData['trackingParameters']['arenaDivideLine'] = self.arenaMidLine
        self.arenaData['trackingParameters']['arenaSide1Sign'] = self.arenaSide1Sign
        self.arenaData['projectorParameters'] = {'position':[self.projX.value(), self.projY.value()],
                                                 'size':[self.projLen.value(), self.projWid.value()],
                                                 'rotation':self.projRot.value()}
        self.arenaData['tankSize_mm'] = [self.tankLength.value(), self.tankWidth.value()]
        self.arenaData['tracking'] = list() #list of tuples (frametime, posx, posy)
        self.arenaData['video'] = list() #list of tuples (frametime, filename)	
        self.arenaData['stateinfo'] = list() #list of times at switch stimulus flipped.
        self.arenaData['shockinfo'] = list()
        self.arenaData['OMRinfo'] = list()
        self.arenaData['pauseinfo'] = list()
        t = datetime.datetime.now()
      
        #save experiment images
        self.bcvImgFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '_BackImg_' + t.strftime('%Y-%m-%d-%H-%M-%S') + '.tiff'
        cv.SaveImage(self.bcvImgFileName, self.trackWidget.getBackgroundImage())	
        self.fishImgFileName = str(self.infoDir.text()) + os.sep +  self.fnResults + '_FishImg_' + t.strftime('%Y-%m-%d-%H-%M-%S') + '.tiff'
        cv.SaveImage(self.fishImgFileName, self.fishImg)

    def saveResults(self):
        f = open(name=self.jsonFileName, mode='w')
        json.dump(self.arenaData,f)
        f.close()

    def getSideColors(self):
        if self.currState == State.ACCLIMATE:
            return (self.paramColorAcclimate.currentIndex(), self.paramColorAcclimate.currentIndex(),
                    str(self.paramColorAcclimate.currentText()), str(self.paramColorAcclimate.currentText()))
        if self.currState == State.PREDONE or self.currState == State.TRAINDONE:
            return (self.paramColorBetween.currentIndex(), self.paramColorBetween.currentIndex(),
                    str(self.paramColorBetween.currentText()), str(self.paramColorBetween.currentText()))
        elif self.currState == State.PRETEST:
            return (self.paramColorPreTest.currentIndex(), self.paramColorPreTest.currentIndex(),
                    str(self.paramColorPreTest.currentText()), str(self.paramColorPreTest.currentText()))
        elif self.currState == State.TRAIN:
            return (self.paramColorTrain.currentIndex(), self.paramColorTrain.currentIndex(),
                    str(self.paramColorTrain.currentText()), str(self.paramColorTrain.currentText()))
        elif self.currState == State.POSTTEST:
            return (self.paramColorPostTest.currentIndex(), self.paramColorPostTest.currentIndex(),
                    str(self.paramColorPostTest.currentText()), str(self.paramColorPostTest.currentText()))
        else:
            return (-1,-1,'Black','Black')

    def getSide1ColorName(self):
        return self.getSideColors()[2]
    def getSide2ColorName(self):
        return self.getSideColors()[3]
    def getSide1ColorNdx(self):
        return self.getSideColors()[0]
    def getSide2ColorNdx(self):
        return self.getSideColors()[1]

    def setShockState(self, bSide1, bSide2):
        if not self.arenaMain.ard:
            print 'WARNING: Arduino not connected'
            return

        if bSide1:
            curr1 = self.arenaMain.ard.pinPulse(self.paramShockChan1.value(), 
                                        self.paramShockPeriod.value(), 
                                        self.paramShockDuration.value(), 
                                        feedbackPin = self.paramCurrChan1.value())
            print 'Shocking!!!'
        else:
            self.arenaMain.ard.pinLow(self.paramShockChan1.value())
            curr1 = 0
        if bSide2:
            curr2 = self.arenaMain.ard.pinPulse(self.paramShockChan2.value(), 
                                           self.paramShockPeriod.value(), 
                                           self.paramShockDuration.value(), 
                                           feedbackPin = self.paramCurrChan2.value())
            print 'Shocking!!!'
        else:
            self.arenaMain.ard.pinLow(self.paramShockChan2.value()) 
            curr2 = 0
        self.arenaData['shockinfo'].append((time.time(), bSide1, bSide2, curr1, curr2))

    def getBrush(self, colorNdx):
        if colorNdx == 0:
            return QtGui.QBrush(QtCore.Qt.white)
        elif colorNdx == 1:
            return QtGui.QBrush(QtCore.Qt.red)           
        elif colorNdx == 2:
            return QtGui.QBrush(QtCore.Qt.blue)           
        elif colorNdx == 3:
            return QtGui.QBrush(QtGui.QColor(128,128,128)) 
        elif colorNdx == 4:
            return QtGui.QBrush(QtCore.Qt.magenta)
        elif colorNdx == 5:
            return QtGui.QBrush(QtCore.Qt.black)
        else:
            return QtGui.QBrush(QtCore.Qt.black)
