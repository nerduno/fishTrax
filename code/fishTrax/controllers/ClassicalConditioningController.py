#----------------------------------------------------------------------------#
#  Imports
#----------------------------------------------------------------------------#
import sys
import os
import os.path 
import math
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
    PREINIT = 2
    PRETEST = 3
    PREDONE = 4
    TRAIN = 5
    TRAINDONE = 6
    POSTINIT = 7
    POSTTEST = 8

class Context:
    BETWEEN = 0
    NEUTRAL = 1
    AVERSIVE = 2
    SPLIT_SIDE1_AVERSIVE = 3
    SPLIT_SIDE1_NEUTRAL = 4

class ClassicalConditioningController(ArenaController.ArenaController):
    def __init__(self, parent, arenaMain):        
        super(ClassicalConditioningController, self).__init__(parent, arenaMain)

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
        self.projCalibButton.clicked.connect(self.updateProjectorDisplay)
        self.projLayout.addWidget(self.projCalibButton,0,0,1,6)
        self.proj1L = QtGui.QLabel('C1')
        self.proj1X = QtGui.QSpinBox()
        self.proj1X.setRange(0,1000)
        self.proj1X.setValue(0)
        self.proj1X.setMaximumWidth(50)
        self.proj1Y = QtGui.QSpinBox()
        self.proj1Y.setValue(0)
        self.proj1Y.setMaximumWidth(50)
        self.proj1Y.setRange(0,1000)
        self.projLayout.addWidget(self.proj1L,1,0)
        self.projLayout.addWidget(self.proj1X,1,1)
        self.projLayout.addWidget(self.proj1Y,1,2)
        self.proj1X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj1Y.valueChanged.connect(self.updateProjectorDisplay)
        self.proj2L = QtGui.QLabel('C2')
        self.proj2X = QtGui.QSpinBox()
        self.proj2X.setRange(0,1000)
        self.proj2X.setValue(0)
        self.proj2X.setMaximumWidth(50)
        self.proj2Y = QtGui.QSpinBox()
        self.proj2Y.setRange(0,1000)
        self.proj2Y.setValue(400)
        self.proj2Y.setMaximumWidth(50)
        self.proj2X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj2Y.valueChanged.connect(self.updateProjectorDisplay)
        self.projLayout.addWidget(self.proj2L,2,0)
        self.projLayout.addWidget(self.proj2X,2,1)
        self.projLayout.addWidget(self.proj2Y,2,2)
        self.proj3L = QtGui.QLabel('C3')
        self.proj3X = QtGui.QSpinBox()
        self.proj3X.setRange(0,1000)
        self.proj3X.setValue(848)
        self.proj3X.setMaximumWidth(50)
        self.proj3Y = QtGui.QSpinBox()
        self.proj3Y.setRange(0,1000)
        self.proj3Y.setValue(400)
        self.proj3Y.setMaximumWidth(50)
        self.projLayout.addWidget(self.proj3L,2,3)
        self.projLayout.addWidget(self.proj3X,2,4)
        self.projLayout.addWidget(self.proj3Y,2,5)
        self.proj3X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj3Y.valueChanged.connect(self.updateProjectorDisplay)
        self.proj4L = QtGui.QLabel('C4')
        self.proj4X = QtGui.QSpinBox()
        self.proj4X.setRange(0,1000)
        self.proj4X.setValue(848)
        self.proj4X.setMaximumWidth(50)
        self.proj4Y = QtGui.QSpinBox()
        self.proj4Y.setRange(0,1000)
        self.proj4Y.setValue(0)
        self.proj4Y.setMaximumWidth(50)
        self.projLayout.addWidget(self.proj4L,1,3)
        self.projLayout.addWidget(self.proj4X,1,4)
        self.projLayout.addWidget(self.proj4Y,1,5)
        self.proj4X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj4Y.valueChanged.connect(self.updateProjectorDisplay)
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

        #testing parameters
        self.paramAcclimate = LabeledSpinBox(None, 'Acclimate (m)', 0, 180, 30, 60)
        self.paramLayout.addWidget(self.paramAcclimate, 0,0,1,2)
        self.paramInitDuration = LabeledSpinBox(None, 'ReminderShock (s)', 0, 30, 4, 60)
        self.paramLayout.addWidget(self.paramInitDuration, 0,2,1,2)
        self.paramNumPre = LabeledSpinBox(None,'NumPre',0,100,4,60) #number of side switches pre test
        self.paramLayout.addWidget(self.paramNumPre,1,0,1,2)
        self.paramNumPost = LabeledSpinBox(None,'NumPost',0,100,4,60) #number of side switches post teset
        self.paramLayout.addWidget(self.paramNumPost,1,2,1,2)
        self.paramTestSwitchTime = LabeledSpinBox(None,'TestSwitchTime (s)',1,3600,300,60) #duration before two sides swap colors during pre and post
        self.paramLayout.addWidget(self.paramTestSwitchTime,2,0,1,2)
        self.paramBetweenTime = LabeledSpinBox(None,'BetweenTime (m)',0,1440,30,60) #time between pre , train and post periods
        self.paramLayout.addWidget(self.paramBetweenTime,2,2,1,2)

        #training parameters
        self.paramNumTrain = LabeledSpinBox(None,'NumTrain',0,100,30,60)
        self.paramLayout.addWidget(self.paramNumTrain,4,0,1,2)
        self.paramUSTime = LabeledSpinBox(None, 'US Time (s)', 1,3600,30,60)
        self.paramLayout.addWidget(self.paramUSTime,4,2,1,2)
        self.paramNeutralMinTime = LabeledSpinBox(None, 'Neutral Min (s)',1,3600,30,60)
        self.paramLayout.addWidget(self.paramNeutralMinTime, 5,0,1,2)
        self.paramNeutralMaxTime = LabeledSpinBox(None, 'Neutral Max (s)',1,3600,60,60)
        self.paramLayout.addWidget(self.paramNeutralMaxTime, 5,2,1,2)
        self.paramShockPeriod = LabeledSpinBox(None, 'Shock Period (ms)', 0,5000,1000,60)
        self.paramLayout.addWidget(self.paramShockPeriod, 6,0,1,2)
        self.paramShockDuration = LabeledSpinBox(None, 'ShockDuration (ms)', 0,1000,50,60)
        self.paramLayout.addWidget(self.paramShockDuration, 6,2,1,2)
        self.paramShockChan1 = LabeledSpinBox(None, 'ShockChan1', 0,10000,12,60)
        self.paramLayout.addWidget(self.paramShockChan1, 7,0,1,2)
        self.paramShockChan2 = LabeledSpinBox(None, 'ShockChan2', 0,10000,13,60)
        self.paramLayout.addWidget(self.paramShockChan2, 7,2,1,2)
        self.paramCurrChan1 = LabeledSpinBox(None, 'CurrChan Side 1', 0,16,0,60)
        self.paramLayout.addWidget(self.paramCurrChan1,8,0,1,2)
        self.paramCurrChan2 = LabeledSpinBox(None, 'CurrChan Side 2', 0,16,0,60)
        self.paramLayout.addWidget(self.paramCurrChan2,8,2,1,2)
        self.paramShockV = LabeledSpinBox(None, 'ShockV', 0,100, 10,60)
        self.paramLayout.addWidget(self.paramShockV, 9,0,1,2)

        #Colors
        self.paramColorUS = QtGui.QComboBox()
        self.paramColorUS.addItem('White')
        self.paramColorUS.addItem('Red')
        self.paramColorUS.addItem('Blue')
        self.paramColorUS.addItem('Gray')
        self.paramColorUS.setCurrentIndex(1)
        self.labelColorUS = QtGui.QLabel('USColor')
        self.paramLayout.addWidget(self.paramColorUS,9,0)
        self.paramLayout.addWidget(self.labelColorUS,9,1)

        self.paramColorNeutral = QtGui.QComboBox()
        self.paramColorNeutral.addItem('White')
        self.paramColorNeutral.addItem('Red')
        self.paramColorNeutral.addItem('Blue')
        self.paramColorNeutral.addItem('Gray')
        self.paramColorNeutral.setCurrentIndex(2)
        self.labelColorNeutral = QtGui.QLabel('NeutralColor')
        self.paramLayout.addWidget(self.paramColorNeutral,9,2)
        self.paramLayout.addWidget(self.labelColorNeutral,9,3)

        self.paramBetweenColor = QtGui.QComboBox()
        self.paramBetweenColor.addItem('White')
        self.paramBetweenColor.addItem('Red')
        self.paramBetweenColor.addItem('Blue')
        self.paramBetweenColor.addItem('Gray')
        self.paramBetweenColor.setCurrentIndex(0)
        self.labelBetweenColor = QtGui.QLabel('BetweenColor')
        self.paramLayout.addWidget(self.paramBetweenColor,10,0)
        self.paramLayout.addWidget(self.labelBetweenColor,10,1)

        self.paramNumFish = LabeledSpinBox(None,'NumFish',1,10,1,60)
        self.paramLayout.addWidget(self.paramNumFish,11,0,1,2)

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
        self.settingsLayout.addWidget(self.startButton,0,0,1,1)
        self.settingsLayout.addWidget(self.pauseButton,1,0,1,1)
        self.settingsLayout.addWidget(self.autoPauseCheckBox,1,1,1,1)
        self.settingsLayout.addWidget(self.arenaGroup,2,0,1,2)
        self.settingsLayout.addWidget(self.trackWidget,3,0,1,2)
        self.settingsLayout.addWidget(self.paramGroup,4,0,1,2)
        self.settingsLayout.addWidget(self.infoGroup,5,0,1,2)
        self.setLayout(self.settingsLayout)


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

    def updateExperimentalState(self):
        if not self.currState == State.OFF:
            self.mutex.acquire()
            try:
                t = time.time()
                #only update status bar if arena is selected.
                if self.isCurrent():
                    self.arenaMain.statusBar().showMessage('State %d'%(self.currState))

                if t > self.nextStateTime:
                    self.setShockState(False, False)
                    self.pauseButton.setDisabled(True)
                    if (self.currState <= State.ACCLIMATE
                        and self.paramInitDuration.value() > 0):
                        self.currState = State.PREINIT
                        self.nextStateTime = t + self.paramInitDuration.value()
                        self.currContext = Context.AVERSIVE
                        self.nextContextTime = float('inf')
                        self.setShockState(True, True)
                    elif (self.currState <= State.PREINIT
                        and self.paramNumPre.value() > 0):
                        self.currState = State.PRETEST
                        self.nextStateTime = float("inf") 
                        self.numContext = 0; self.numContexts = self.paramNumPre.value()
                        self.currContext = Context.SPLIT_SIDE1_NEUTRAL
                        self.nextContextTime = t + self.paramTestSwitchTime.value()
                    elif (self.currState <= State.PRETEST
                        and self.paramBetweenTime.value() > 0):
                        self.currState = State.PREDONE
                        self.nextStateTime = t + self.paramBetweenTime.value()*60
                        self.currContext = Context.BETWEEN
                        self.nextContextTime = float('inf')
                        self.pauseButton.setDisabled(False)
                        if self.autoPauseCheckBox.isChecked():
                            self.pauseButton.setChecked(True)
                            self.doPause()
                    elif (self.currState <= State.PREDONE
                        and self.paramNumTrain.value() > 0):
                        self.currState = State.TRAIN
                        self.nextStateTime = float("inf")
                        self.numContext = 0; self.numContexts = self.paramNumTrain.value()
                        self.currContext = Context.NEUTRAL
                        self.nextContextTime = t + random.uniform(self.paramNeutralMinTime.value(), self.paramNeutralMaxTime.value())
                    elif (self.currState <= State.TRAIN
                          and self.paramBetweenTime.value() > 0):
                        self.currState = State.TRAINDONE
                        self.nextStateTime = t + self.paramBetweenTime.value()*60
                        self.currContext = Context.BETWEEN
                        self.nextContextTime = float('inf')
                        self.nextShockTime = float('inf')
                        self.pauseButton.setDisabled(False)
                        if self.autoPauseCheckBox.isChecked():
                            self.pauseButton.setChecked(True)
                            self.doPause()
                    elif (self.currState <= State.TRAINDONE
                        and self.paramInitDuration.value() > 0):
                        self.currState = State.POSTINIT
                        self.nextStateTime = t + self.paramInitDuration.value()
                        self.currContext = Context.AVERSIVE
                        self.nextContextTime = float('inf')
                        self.setShockState(True,True)
                    elif (self.currState <= State.POSTINIT
                        and self.paramNumPost.value() > 0):
                        self.currState = State.POSTTEST
                        self.nextStateTime = float("inf") 
                        self.numContext = 0; self.numContexts = self.paramNumPost.value()
                        self.currContext = Context.SPLIT_SIDE1_NEUTRAL
                        self.nextContextTime = t + self.paramTestSwitchTime.value()
                    elif self.currState <= State.POSTTEST:
                        self.currState = State.OFF
                        self.currContext = Context.BETWEEN
                        self.nextContextTime = float('inf')
                        self.startButton.setText('Start Switches')
                        self.startButton.setChecked(False)
                        self.paramGroup.setDisabled(False)
                        self.infoGroup.setDisabled(False)
                        self.saveResults()
                    self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
                    self.updateProjectorDisplay()
                    self.saveResults()
                          
                #handle context changes
                if t > self.nextContextTime:
                    self.setShockState(False,False)
                    self.numContext += 1
                    if self.numContext >= self.numContexts:
                        self.nextStateTime = t
                        self.nextContextTime = float('inf')
                    else:
                        if self.currContext == Context.AVERSIVE:
                            self.currContext = Context.NEUTRAL
                            self.nextContextTime = t + random.uniform(self.paramNeutralMinTime.value(),
                                                                      self.paramNeutralMaxTime.value())
                            print 'N ', self.nextContextTime
                        elif self.currContext == Context.NEUTRAL:
                            self.currContext = Context.AVERSIVE
                            self.nextContextTime = t + self.paramUSTime.value()
                            self.setShockState(True,True)
                            print 'A ', self.nextContextTime
                        elif self.currContext == Context.SPLIT_SIDE1_NEUTRAL:
                            self.currContext = Context.SPLIT_SIDE1_AVERSIVE
                            self.nextContextTime = t + self.paramTestSwitchTime.value()
                        elif self.currContext == Context.SPLIT_SIDE1_AVERSIVE:
                            self.currContext = Context.SPLIT_SIDE1_NEUTRAL
                            self.nextContextTime = t + self.paramTestSwitchTime.value()
                        self.updateProjectorDisplay()
                        self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
            except:
                print 'ClassicalConditioningController:updateState failed'
                traceback.print_exc()
                QtCore.pyqtRemoveInputHook() 
                ipdb.set_trace()
            finally:
                self.mutex.release()

    def isReadyToStart(self):
        return os.path.exists(self.infoDir.text()) and self.trackWidget.getBackgroundImage() and self.fishImg and self.arenaCamCorners

    def drawProjectorDisplay(self, painter):
        if self.currState == State.OFF and self.projCalibButton.isChecked() and self.isCurrent():
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
            poly.append(QtCore.QPointF(self.proj1X.value(), self.proj1Y.value()))
            poly.append(QtCore.QPointF(self.proj2X.value(), self.proj2Y.value()))
            poly.append(QtCore.QPointF(a*self.proj2X.value() + b*self.proj3X.value(), a*self.proj2Y.value() + b*self.proj3Y.value()))
            poly.append(QtCore.QPointF(a*self.proj1X.value() + b*self.proj4X.value(), a*self.proj1Y.value() + b*self.proj4Y.value()))
            painter.drawPolygon(poly)
            painter.drawText(self.proj1X.value(),self.proj1Y.value(),'1')
            #Draw side two
            pen = QtGui.QPen(QtCore.Qt.NoPen)
            brush = QtGui.QBrush(side2Color)
            painter.setBrush(brush)
            painter.setPen(pen)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(a*self.proj1X.value() + b*self.proj4X.value(), a*self.proj1Y.value() + b*self.proj4Y.value()))
            poly.append(QtCore.QPointF(a*self.proj2X.value() + b*self.proj3X.value(), a*self.proj2Y.value() + b*self.proj3Y.value()))
            poly.append(QtCore.QPointF(self.proj3X.value(), self.proj3Y.value()))
            poly.append(QtCore.QPointF(self.proj4X.value(), self.proj4Y.value()))
            painter.drawPolygon(poly)
        else:
            if self.currState == State.OFF:
                #Draw whole tank
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                brush = self.getBrush(self.paramBetweenColor.currentIndex())
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(self.proj1X.value(), self.proj1Y.value()))
                poly.append(QtCore.QPointF(self.proj2X.value(), self.proj2Y.value()))
                poly.append(QtCore.QPointF(self.proj3X.value(), self.proj3Y.value()))
                poly.append(QtCore.QPointF(self.proj4X.value(), self.proj4Y.value()))
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
                poly.append(QtCore.QPointF(self.proj1X.value(), self.proj1Y.value()))
                poly.append(QtCore.QPointF(self.proj2X.value(), self.proj2Y.value()))
                poly.append(QtCore.QPointF(a*self.proj2X.value() + b*self.proj3X.value(), a*self.proj2Y.value() + b*self.proj3Y.value()))
                poly.append(QtCore.QPointF(a*self.proj1X.value() + b*self.proj4X.value(), a*self.proj1Y.value() + b*self.proj4Y.value()))
                painter.drawPolygon(poly)
                #Draw side two
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                brush = self.getBrush(side2Color)
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(a*self.proj1X.value() + b*self.proj4X.value(), a*self.proj1Y.value() + b*self.proj4Y.value()))
                poly.append(QtCore.QPointF(a*self.proj2X.value() + b*self.proj3X.value(), a*self.proj2Y.value() + b*self.proj3Y.value()))
                poly.append(QtCore.QPointF(self.proj3X.value(), self.proj3Y.value()))
                poly.append(QtCore.QPointF(self.proj4X.value(), self.proj4Y.value()))
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
                    self.currContext = Context.BETWEEN
                    self.setShockState(False,False)
                    self.nextContextTime = float('inf')
                    self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
                    self.updateProjectorDisplay()
                    self.startButton.setText('Stop')
                else:
                    self.startButton.setChecked(False)
                    self.arenaMain.statusBar().showMessage('Arena not ready to start.  Information is missing.')
            else: 
                t = time.time()
                self.currState = State.OFF
                self.currContext = Context.BETWEEN
                self.setShockState(False,False)
                self.nextContextTime = float('inf')
                self.startButton.setText('Start Switches')
                self.arenaData['stateinfo'].append((t, self.currState, self.getSide1ColorName(), self.getSide2ColorName()))
                self.updateProjectorDisplay()
                self.saveResults()
                self.paramGroup.setDisabled(False) 
                self.infoGroup.setDisabled(False)
                self.pauseButton.setChecked(False)
        except:
            print 'ClassicalConditioningController:startSwitches failed'
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
            print 'ClassicalConditioningController: pause failed'
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
        self.arenaData['parameters'] = { 'numPre':self.paramNumPre.value(),
                                         'numTrain':self.paramNumTrain.value(),
                                         'numPost':self.paramNumPost.value(),
                                         'acclimate (m)':self.paramAcclimate.value(),
                                         'initShockDuration': self.paramInitDuration.value(),
                                         'between (m)': self.paramBetweenTime.value(),
                                         'prepostswitchtime': self.paramTestSwitchTime.value(),
                                         'trainUStime': self.paramUSTime.value(),
                                         'trainNeutralMinTime':self.paramNeutralMinTime.value(),
                                         'trainNeutralMaxTime':self.paramNeutralMaxTime.value(),
                                         'shock period (ms)':self.paramShockPeriod.value(),
                                         'shock dura (ms)':self.paramShockDuration.value(),
                                         'shock chan 1':self.paramShockChan1.value(),
                                         'shock chan 2':self.paramShockChan2.value(),
                                         'shock V':self.paramShockV.value(),
                                         'USColor':str(self.paramColorUS.currentText()),
                                         'NeutralColor':str(self.paramColorNeutral.currentText()),
                                         'BetweenColor':str(self.paramBetweenColor.currentText()),
                                         'numFish': self.paramNumFish.value(),
                                         'CodeVersion':None }
        self.arenaData['trackingParameters'] = self.trackWidget.getParameterDictionary()
        self.arenaData['trackingParameters']['arenaPoly'] = self.arenaCamCorners 
        self.arenaData['trackingParameters']['arenaDivideLine'] = self.arenaMidLine
        self.arenaData['trackingParameters']['arenaSide1Sign'] = self.arenaSide1Sign
        self.arenaData['tracking'] = list() #list of tuples (frametime, posx, posy)
        self.arenaData['video'] = list() #list of tuples (frametime, filename)	
        self.arenaData['stateinfo'] = list() #list of times at switch stimulus flipped.
        self.arenaData['shockinfo'] = list()
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
        if self.currContext == Context.BETWEEN:
            return (self.paramBetweenColor.currentIndex(), self.paramBetweenColor.currentIndex(),
                    str(self.paramBetweenColor.currentText()), str(self.paramBetweenColor.currentText()))
        elif self.currContext == Context.AVERSIVE:
            return (self.paramColorUS.currentIndex(), self.paramColorUS.currentIndex(),
                    str(self.paramColorUS.currentText()), str(self.paramColorUS.currentText()))
        elif self.currContext == Context.NEUTRAL:
            return (self.paramColorNeutral.currentIndex(), self.paramColorNeutral.currentIndex(),
                    str(self.paramColorNeutral.currentText()), str(self.paramColorNeutral.currentText()))
        elif self.currContext == Context.SPLIT_SIDE1_AVERSIVE:
            return (self.paramColorUS.currentIndex(), self.paramColorNeutral.currentIndex(),
                    str(self.paramColorUS.currentText()), str(self.paramColorNeutral.currentText()))
        elif self.currContext == Context.SPLIT_SIDE1_NEUTRAL:
            return (self.paramColorNeutral.currentIndex(), self.paramColorUS.currentIndex(),
                    str(self.paramColorNeutral.currentText()), str(self.paramColorUS.currentText()))
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
        else:
            self.arenaMain.ard.pinLow(self.paramShockChan1.value())
            curr1 = 0
        if bSide2:
            curr2 = self.arenaMain.ard.pinPulse(self.paramShockChan2.value(), 
                                           self.paramShockPeriod.value(), 
                                           self.paramShockDuration.value(), 
                                           feedbackPin = self.paramCurrChan2.value())
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
        else:
            return QtGui.QBrush(QtCore.Qt.black)




        
                               

                        




