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

# Constants specifying trial types
#class Trial:
#    PAIRED = 1
#    TEST = 2
#    UNPAIRED = 3
#    SHOCK = 4

# Constants for managing avoidance task state
class State:
    BETWEEN = 0
    LED = 1
    SHOCK = 2

class Side:
    S1 = 1
    S2 = -1

class AvoidanceController(ArenaController.ArenaController):
    def __init__(self, parent, arenaMain):        
        super(AvoidanceController, self).__init__(parent, arenaMain)

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
        self.pulseMutex = Lock()
        self.nDispMode = 0
        self.bRunning = False
        self.currState = State.BETWEEN
        self.fishPosUpdate = False
        self.fishPos = (0,0)
        self.fishSize = None
        self.escapeLine= []
        self.escapeSign = []

        #shock pulse state - only if using labjack
        self.shockSide1_t = 0 #0 if not shocking, otherwise time of next shock
        self.bPulseHigh1 = False #true if shock_pulse in progress
        self.shockSide1_ndx = None
        self.shockSide2_t = 0 #0 if not shocking, otherwise time of next shock
        self.bPulseHigh2 = False #true if shock_pulse in progress
        self.shockSide2_ndx = None

        #tracking related images
        self.currCvFrame = None

        #init UI
        #arena info group box
        self.arenaGroup = QtGui.QGroupBox(self)
        self.arenaGroup.setTitle('Arena Info')
        self.arenaLayout = QtGui.QGridLayout()
        self.arenaLayout.setHorizontalSpacing(3)
        self.arenaLayout.setVerticalSpacing(3)
        self.cntrUI = QtGui.QWidget(self)
        self.cntrLayout = QtGui.QGridLayout()
        self.cntrLayout.setHorizontalSpacing(3)
        self.cntrLayout.setVerticalSpacing(3)
        l1 = QtGui.QLabel('Side1 Control Channel:')
        l2 = QtGui.QLabel('Side2 Control Channel:')
        l3 = QtGui.QLabel('Current Input Channel:')
        self.cntrSide1Channel = QtGui.QSpinBox()
        self.cntrSide1Channel.setValue(8)
        self.cntrSide1Channel.setMaximumWidth(50)
        self.cntrSide1Channel.setRange(0,8000)
        self.cntrSide2Channel = QtGui.QSpinBox()
        self.cntrSide2Channel.setValue(9)
        self.cntrSide2Channel.setMaximumWidth(50)
        self.cntrSide2Channel.setRange(0,8000)
        self.currInputChannel = QtGui.QSpinBox()
        self.currInputChannel.setValue(10)
        self.currInputChannel.setMaximumWidth(50)
        self.currInputChannel.setRange(0,8000)
        self.cntrLayout.addWidget(l1,0,0)
        self.cntrLayout.addWidget(self.cntrSide1Channel,0,1)
        self.cntrLayout.addWidget(l2,1,0)
        self.cntrLayout.addWidget(self.cntrSide2Channel,1,1)
        self.cntrLayout.addWidget(l3,2,0)
        self.cntrLayout.addWidget(self.currInputChannel,2,1)
        self.cntrLayout.setColumnStretch(2,1)
        self.cntrUI.setLayout(self.cntrLayout)
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
        self.proj1X.setValue(0)
        self.proj1X.setMaximumWidth(50)
        self.proj1X.setRange(0,2000)
        self.proj1Y = QtGui.QSpinBox()
        self.proj1Y.setValue(0)
        self.proj1Y.setMaximumWidth(50)
        self.proj1Y.setRange(0,2000)
        self.projLayout.addWidget(self.proj1L,1,0)
        self.projLayout.addWidget(self.proj1X,1,1)
        self.projLayout.addWidget(self.proj1Y,1,2)
        self.proj1X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj1Y.valueChanged.connect(self.updateProjectorDisplay)
        self.proj2L = QtGui.QLabel('C2')
        self.proj2X = QtGui.QSpinBox()
        self.proj2X.setValue(0)
        self.proj2X.setMaximumWidth(50)
        self.proj2X.setRange(0,2000)
        self.proj2Y = QtGui.QSpinBox()
        self.proj2Y.setValue(100)
        self.proj2Y.setMaximumWidth(50)
        self.proj2Y.setRange(0,2000)
        self.proj2X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj2Y.valueChanged.connect(self.updateProjectorDisplay)
        self.projLayout.addWidget(self.proj2L,2,0)
        self.projLayout.addWidget(self.proj2X,2,1)
        self.projLayout.addWidget(self.proj2Y,2,2)
        self.proj3L = QtGui.QLabel('C3')
        self.proj3X = QtGui.QSpinBox()
        self.proj3X.setValue(200)
        self.proj3X.setMaximumWidth(50)
        self.proj3X.setRange(0,2000)
        self.proj3Y = QtGui.QSpinBox()
        self.proj3Y.setValue(100)
        self.proj3Y.setMaximumWidth(50)
        self.proj3Y.setRange(0,2000)
        self.projLayout.addWidget(self.proj3L,2,3)
        self.projLayout.addWidget(self.proj3X,2,4)
        self.projLayout.addWidget(self.proj3Y,2,5)
        self.proj3X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj3Y.valueChanged.connect(self.updateProjectorDisplay)
        self.proj4L = QtGui.QLabel('C4')
        self.proj4X = QtGui.QSpinBox()
        self.proj4X.setValue(200)
        self.proj4X.setMaximumWidth(50)
        self.proj4X.setRange(0,2000)
        self.proj4Y = QtGui.QSpinBox()
        self.proj4Y.setValue(0)
        self.proj4Y.setMaximumWidth(50)
        self.proj4Y.setRange(0,2000)
        self.projLayout.addWidget(self.proj4L,1,3)
        self.projLayout.addWidget(self.proj4X,1,4)
        self.projLayout.addWidget(self.proj4Y,1,5)
        self.proj4X.valueChanged.connect(self.updateProjectorDisplay)
        self.proj4Y.valueChanged.connect(self.updateProjectorDisplay)
        self.projLayout.setColumnStretch(6,1)
        self.projGroup.setLayout(self.projLayout)
        self.arenaLayout.addWidget(self.camCalibButton, 0,0)
        self.arenaLayout.addWidget(self.cntrUI,1,0)
        self.arenaLayout.addWidget(self.projGroup,2,0)
        self.arenaLayout.setColumnStretch(1,1)
        self.arenaGroup.setLayout(self.arenaLayout)

        #tracking group box
        self.trackWidget = FishTrackerWidget(self, self.arenaMain.ftDisp)

        #experimental parameters groupbox
        self.paramGroup = QtGui.QGroupBox()
        self.paramGroup.setTitle('Exprimental Parameters')
        self.paramLayout = QtGui.QGridLayout()
        self.paramLayout.setHorizontalSpacing(2)
        self.paramLayout.setVerticalSpacing(2)

        self.paramNumTrials = LabeledSpinBox(None,'trials',1,999,40,60)
        self.paramLayout.addWidget(self.paramNumTrials,1,0,1,2)
        self.paramAcc = LabeledSpinBox(None,'acclimation (s)',1,3600,900,60)
        self.paramLayout.addWidget(self.paramAcc,1,2,1,2)
        self.paramITIMin = LabeledSpinBox(None,'iti min (s)',1,300,15,60)
        self.paramLayout.addWidget(self.paramITIMin,2,0,1,2)
        self.paramITIMax = LabeledSpinBox(None,'iti max (s)',1,300,30,60)
        self.paramLayout.addWidget(self.paramITIMax,2,2,1,2)
        self.paramEscapeT = LabeledSpinBox(None,'escape (s)',1,60,10,60)
        self.paramLayout.addWidget(self.paramEscapeT,3,0,1,2)
        self.paramShockT = LabeledSpinBox(None,'shock (s)',1,100,30,60)
        self.paramLayout.addWidget(self.paramShockT,3,2,1,2)
        self.paramV = LabeledSpinBox(None,'volts',1,50,12,60)
        self.paramLayout.addWidget(self.paramV,4,0,1,2)
        self.paramShockPeriod = LabeledSpinBox(None,'shock period (ms)',1,5000,1000,60)
        self.paramLayout.addWidget(self.paramShockPeriod,4,2,1,2)
        self.paramShockDura = LabeledSpinBox(None,'shock t (ms)',1,1000,100,60)
        self.paramLayout.addWidget(self.paramShockDura,5,0,1,2)

        self.paramNeutral = QtGui.QComboBox()
        self.paramNeutral.addItem('White')
        self.paramNeutral.addItem('Red')
        self.paramNeutral.addItem('Blue')
        self.paramNeutral.addItem('Gray')
        self.paramNeutral.setCurrentIndex(0)
        self.labelNeutral = QtGui.QLabel('Neutral')
        self.paramLayout.addWidget(self.paramNeutral,5,2)
        self.paramLayout.addWidget(self.labelNeutral,5,3)

        self.paramAvoid = QtGui.QComboBox()
        self.paramAvoid.addItem('White')
        self.paramAvoid.addItem('Red')
        self.paramAvoid.addItem('Blue')
        self.paramAvoid.addItem('Gray')
        self.paramAvoid.setCurrentIndex(1)
        self.labelAvoid = QtGui.QLabel('Avoid')
        self.paramLayout.addWidget(self.paramAvoid,6,0)
        self.paramLayout.addWidget(self.labelAvoid,6,1)

        self.paramEscape = QtGui.QComboBox()
        self.paramEscape.addItem('White')
        self.paramEscape.addItem('Red')
        self.paramEscape.addItem('Blue')
        self.paramEscape.addItem('Gray')
        self.paramEscape.setCurrentIndex(2)
        self.labelEscape = QtGui.QLabel('Escape')
        self.paramLayout.addWidget(self.paramEscape,6,2)
        self.paramLayout.addWidget(self.labelEscape,6,3)

        self.paramDynamic= QtGui.QCheckBox('Dynamic Escape')
        self.paramLayout.addWidget(self.paramDynamic,7,0,1,2)
        
        self.paramEscapePos = QtGui.QDoubleSpinBox()
        self.paramEscapePos.setRange(0,1)
        self.paramEscapePos.setValue(.5)
        self.labelEscapePos = QtGui.QLabel('escape pos (0-1)')
        self.paramLayout.addWidget(self.paramEscapePos,7,2)
        self.paramLayout.addWidget(self.labelEscapePos,7,3)

        self.paramDynamicDraw = QtGui.QCheckBox('Dynamic Draw')
        self.paramDynamicDraw.setChecked(True)
        self.paramLayout.addWidget(self.paramDynamicDraw,8,0,1,2)

        self.paramDebug = QtGui.QPushButton('Debug')
        self.paramDebug.setMaximumWidth(150) 
        self.paramDebug.setCheckable(True)
        self.paramLayout.addWidget(self.paramDebug,8,2,1,2)
        self.paramDebug.clicked.connect(self.useDebugParams)

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
        self.settingsLayout.addWidget(self.arenaGroup,0,0)
        self.settingsLayout.addWidget(self.trackWidget,1,0)
        self.settingsLayout.addWidget(self.paramGroup,2,0)
        self.settingsLayout.addWidget(self.infoGroup,3,0)
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

            if self.bRunning:
                self.avoidData['video'].append((self.frameTime, None)) 
                self.avoidData['tracking'].append((self.frameTime, self.fishPos[0], self.fishPos[1]))

            self.arenaView = view
        except:
            print 'AvoidanceController:onNewFrame failed'
            print "Unexpected error:", sys.exc_info()[0]
        finally:
            self.mutex.release()

  
    def updateState(self):
        self.updateExperimentalState()
        self.handlePulsedShocks()

    def updateExperimentalState(self):
        if self.bRunning:
            self.mutex.acquire()
            try:
                t = time.time()
                #only update status bar if arena is selected.
                if self.isCurrent():
                    if self.nTrial>-1:
                        #print('NextTrial# %d TimeTilNextTrial %f TrialTime %f' % (self.nTrial+1, self.timeOfNextTrial - t, t - self.avoidData['trials'][self.nTrial]['startT']))
                        self.arenaMain.statusBar().showMessage('NextTrial# %d TimeTilNextTrial %f TrialTime %f' % (self.nTrial+1, self.timeOfNextTrial - t, t - self.avoidData['trials'][self.nTrial]['startT']))
                    else:
                        #print('NextTrial# %d TimeTilNextTrial %f' % (self.nTrial+1, self.timeOfNextTrial - t))                        
                        self.arenaMain.statusBar().showMessage('NextTrial# %d TimeTilNextTrial %f' % (self.nTrial+1, self.timeOfNextTrial - t))

                #check if fish escaped
                bDidEscape = False
                if self.fishPosUpdate:
                    self.fishPosUpdate = False
                    if self.escapeLine and (self.currState == State.LED or self.currState == State.SHOCK):
                        bDidEscape = self.isOnSide(self.fishPos, self.escapeLine, self.escapeSign)

                #handle State Changes
                ###BETWEEN###
                if self.currState==State.BETWEEN and t >= self.timeOfNextTrial: 
                    print 'Start Trial'
                    self.nTrial+=1
                    if self.nTrial < self.paramNumTrials.value():
                        self.currState = State.LED;
                        self.timeState = t;

                        #determine relative fish position (0->Side1 1->Side2) (by projecting onto 1 side)
                        ac = self.arenaCamCorners
                        lengC = ((self.fishPos[1]-ac[0][1])**2 + (self.fishPos[0] - ac[0][0])**2)**.5 #length of fish vector
                        lengB = ((ac[3][1]-ac[0][1])**2 + (ac[3][0]-ac[0][0])**2)**.5  #length of tank side
                        lengA = ((self.fishPos[1]-ac[3][1])**2 + (self.fishPos[0]-ac[3][0])**2)**.5  #length of connecting vector
                        #dot product = fish vector length * cos(angle between fish vector and tank side)/normalized by side length
                        relPos = lengC * (lengB**2 + lengC**2 - lengA**2)/(2*lengC*lengB)/lengB

                        #determine side of fish -- not quite the same as relpos<0.5 because corners 2 and 3 not considered in relpos
                        if self.isOnSide(self.fishPos, self.arenaMidLine, self.arenaSide1Sign):
                            self.trialSide = Side.S1
                        else:
                            self.trialSide = Side.S2

                        #determine relative escape position
                        if not self.paramDynamic.isChecked():
                            if self.trialSide == Side.S1:
                                self.escapePos = self.paramEscapePos.value()
                            else:
                                self.escapePos = 1 - self.paramEscapePos.value()
                        else:
                            if self.trialSide == Side.S1:
                                self.escapePos = relPos + self.paramEscapePos.value()
                            else:
                                self.escapePos = relPos - self.paramEscapePos.value()                            
 
                        #convert relative escape position into a line
                        (self.escapeLine, side1Sign) = self.processArenaCorners(self.arenaCamCorners, self.escapePos)
                        self.escapeSign = -1 * self.trialSide * self.arenaSide1Sign

                        self.updateProjectorDisplay()
                        self.avoidData['trials'].append({'trialNum':self.nTrial,
                                                         'startT':self.timeState,
                                                         'side':self.trialSide,
                                                         'escape': (self.escapeLine, self.escapeSign),
                                                         'endT':-1})
                    else:
                        #experiment is complete
                        self.stopController()
                ###LED###
                elif self.currState== State.LED:  
                    if bDidEscape:
                        print 'Avoided Shocks'
                        self.timeState = t
                        self.currState=State.BETWEEN;
                        self.timeOfNextTrial = self.timeState + random.randint(self.paramITIMin.value(),self.paramITIMax.value())
                        self.escapeLine = []
                        self.avoidData['trials'][self.nTrial]['endT'] = self.timeState
                        self.avoidData['trials'][self.nTrial]['bAvoidedShock'] = True
                        self.saveResults()
                    elif (t - self.timeState) > self.paramEscapeT.value(): 
                        print 'Starting Shocks'
                        self.timeState = t
                        self.currState= State.SHOCK;
                        self.avoidData['trials'][self.nTrial]['bAvoidedShock'] = False                    
                        self.setShockState(self.trialSide == Side.S1, self.trialSide == Side.S2)
                        self.avoidData['trials'][self.nTrial]['Shock_current_start'] = self.readCurrentInput()
                    self.updateProjectorDisplay()
                ###SHOCK###
                elif self.currState == State.SHOCK:
                    if bDidEscape or t - self.timeState > self.paramShockT.value():
                        print 'Ending Shocks'
                        self.currState=State.BETWEEN
                        self.timeOfNextTrial = self.timeState + random.randint(self.paramITIMin.value(),self.paramITIMax.value())
                        self.timeState = t;
                        self.escapeLine = []
                        self.setShockState(False, False)
                        self.updateProjectorDisplay()     
                        self.avoidData['trials'][self.nTrial]['endT'] = self.timeState
                        self.saveResults()
                #########
            except:

                print 'AvoidanceController:updateState failed'
                traceback.print_exc()
                QtCore.pyqtRemoveInputHook() 
                ipdb.set_trace()
            finally:
                self.mutex.release()

    def isReadyToStart(self):
        bReady =  os.path.exists(self.infoDir.text()) and self.trackWidget.getBackgroundImage() and self.fishImg and self.arenaCamCorners
        print bReady
        return bReady

    def drawProjectorDisplay(self, painter):
        if not self.bRunning and self.projCalibButton.isChecked():
            brush = QtGui.QBrush(QtCore.Qt.blue)
            pen = QtGui.QPen(QtCore.Qt.black)
            painter.setBrush(brush)
            painter.setPen(pen)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(self.proj1X.value(), self.proj1Y.value()))
            poly.append(QtCore.QPointF(self.proj2X.value(), self.proj2Y.value()))
            poly.append(QtCore.QPointF(self.proj3X.value(), self.proj3Y.value()))
            poly.append(QtCore.QPointF(self.proj4X.value(), self.proj4Y.value()))
            painter.drawPolygon(poly)
        else:
            if self.currState == State.BETWEEN:
                #Draw whole tank
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                print self.paramNeutral.currentIndex()
                brush = self.getBrush(self.paramNeutral.currentIndex())
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(self.proj1X.value(), self.proj1Y.value()))
                poly.append(QtCore.QPointF(self.proj2X.value(), self.proj2Y.value()))
                poly.append(QtCore.QPointF(self.proj3X.value(), self.proj3Y.value()))
                poly.append(QtCore.QPointF(self.proj4X.value(), self.proj4Y.value()))
                painter.drawPolygon(poly)
            else:
                side1Color = side2Color = self.paramEscape.currentIndex()
                if self.trialSide == Side.S1:
                    side1Color = self.paramAvoid.currentIndex()
                else:
                    side2Color = self.paramAvoid.currentIndex()

                if self.paramDynamicDraw.isChecked():
                    a = float(1-self.escapePos)
                    b = float(self.escapePos)
                else:
                    a = 0.5
                    b = 0.5

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
            painter.drawEllipse(QtCore.QPointF(self.fishPos[0],self.fishPos[1]), 3,3)

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

        #draw escape line
        if self.escapeLine:
            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.red)
            pen.setWidth(1)
            l = self.escapeLine
            painter.drawLine(QtCore.QPointF(l[0][0],l[0][1]), QtCore.QPointF(l[1][0],l[1][1]))            

    def start(self):
        self.mutex.acquire()
        try:
            self.paramGroup.setDisabled(True)
            self.infoGroup.setDisabled(True)
            self.initResults()
            
            #initialize experimental state
            self.nTrial = -1
            self.currState = State.BETWEEN
            self.setShockState(False,False)
            self.updateProjectorDisplay()
            self.timeState = time.time()
            self.timeOfNextTrial = self.timeState + self.paramAcc.value()
            self.trialSide = Side.S1
            self.escapeLine = []
            self.bRunning = True
        finally:
            self.mutex.release()

    def stop(self):
        self.mutex.acquire()
        try:
            self.stopController()
        finally:
            self.mutex.release()

    def stopController(self):
        if self.bRunning:
            self.bRunning = False
            self.saveResults()
            print 'Experiment stopped successfully.  Saved experimental data.'    
        self.currState = State.BETWEEN
        self.setShockState(False,False)
        self.nTrial = -1
        self.escapeLine = []
        self.updateProjectorDisplay()
        self.paramGroup.setDisabled(False)
        self.infoGroup.setDisabled(False)       

    #---------------------------------------------------
    # CALLBACK METHODS
    #---------------------------------------------------
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

    def useDebugParams(self):
        if self.paramDebug.isChecked():
            self.debugVals = {}
            self.debugVals['dn'] = self.paramNumTrials.value()
            self.debugVals['da'] = self.paramAcc.value()
            self.debugVals['ds'] = self.paramITIMin.value()
            self.debugVals['dl'] = self.paramITIMax.value()
            self.debugVals['de'] = self.paramEscapeT.value()
            self.debugVals['dt'] = self.paramShockT.value()
            self.debugVals['dv'] = self.paramV.value()
            self.paramNumTrials.setValue(5)
            self.paramAcc.setValue(5)
            self.paramITIMin.setValue(3)
            self.paramITIMax.setValue(3)
            self.paramEscapeT.setValue(5)
            self.paramShockT.setValue(5)
            self.paramV.setValue(0)              
        else:
            self.paramNumTrials.setValue(self.debugVals['dn'])
            self.paramAcc.setValue(self.debugVals['da'])
            self.paramITIMin.setValue(self.debugVals['ds'])
            self.paramITIMax.setValue(self.debugVals['dl'])
            self.paramEscapeT.setValue(self.debugVals['de'])
            self.paramShockT.setValue(self.debugVals['dt'])
            self.paramV.setValue(self.debugVals['dv'])            

    #---------------------------------------------------
    # HELPER METHODS
    #---------------------------------------------------

#    def getBackgroundImage(self):
#        if self.currCvFrame:
#            self.bcvImg = cv.CloneImage(self.currCvFrame) 
#            self.trackWidget.setBackgroundImage(self.bcvImg)

    #convert the arena corners into a color mask image (arena=255, not=0)    
    def getArenaMask(self): 
        if self.arenaView:
            cvImg = self.currCvFrame
            self.arenaCvMask = cv.CreateImage((cvImg.width,cvImg.height), cvImg.depth, cvImg.channels) 
            cv.SetZero(self.arenaCvMask)
            cv.FillConvexPoly(self.arenaCvMask, self.arenaCamCorners, (255,)*cvImg.channels)	
            self.trackWidget.setTrackMask(self.arenaCvMask)

    def initResults(self):
        #prepare output data structure
        self.avoidData = {}
        self.avoidData['fishbirthday'] = str(self.infoDOB.date().toPyDate())
        self.avoidData['fishage'] =  (datetime.date.today() - self.infoDOB.date().toPyDate()).days
        self.avoidData['fishstrain'] = str(self.infoType.text())
        self.avoidData['fishsize'] = self.fishSize
        self.avoidData['parameters'] = { 'numtrials':self.paramNumTrials.value(),
                                         'LEDTimeMS':self.paramEscapeT.value(),
                                         'ShockTimeMS':self.paramShockT.value(),
                                         'ShockV':self.paramV.value(),
                                         'AcclimationTime':self.paramAcc.value(),
                                         'MinTrialInterval':self.paramITIMin.value(),
                                         'MaxTrialInterval':self.paramITIMax.value(),
                                         'ShockPeriodT':self.paramShockPeriod.value(),
                                         'ShockDurationT':self.paramShockDura.value(),
                                         'NeuralStimulus':str(self.paramNeutral.currentText()),
                                         'AvoidStimulus':str(self.paramAvoid.currentText()),
                                         'EscapeStimulus':str(self.paramEscape.currentText()),
                                         'isDynamicEscape':self.paramDynamic.isChecked(),
                                         'inDynamicDraw':self.paramDynamicDraw.isChecked(),
                                         'fEscapePosition':self.paramEscapePos.value(),
                                         'CodeVersion':None }
        self.avoidData['trackingParameters'] = self.trackWidget.getParameterDictionary()
        self.avoidData['trackingParameters']['arenaPoly'] = self.arenaCamCorners 
        self.avoidData['trackingParameters']['arenaDivideLine'] = self.arenaMidLine
        self.avoidData['trackingParameters']['arenaSide1Sign'] = self.arenaSide1Sign
        self.avoidData['trials'] = list() #outcome on each trial
        self.avoidData['tracking'] = list() #list of tuples (frametime, posx, posy)
        self.avoidData['video'] = list() #list of tuples (frametime, filename)	
        self.avoidData['current'] = list() #list of tuples (time, currentValue)
        self.avoidData['shockPulses'] = list() #list of tuples (side, target_start, actual_start, target_end, actual_end)

        #get experiment filename
        [p, self.fnResults] = os.path.split(str(self.infoDir.text()))
        self.fnResults = self.fnResults + '_' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.jsonFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '.json'

        #save experiment images
        self.bcvImgFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '_BackImg.tiff'
        cv.SaveImage(self.bcvImgFileName, self.trackWidget.getBackgroundImage())	
        self.fishImgFileName = str(self.infoDir.text()) + os.sep +  self.fnResults + '_FishImg.tiff'
        cv.SaveImage(self.fishImgFileName, self.fishImg)


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

    def saveResults(self):
        f = open(name=self.jsonFileName, mode='w')
        json.dump(self.avoidData,f)
        f.close()

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

    def setShockState(self, bSide1, bSide2):
        if bSide1:
            self.arenaMain.ard.pinPulse(self.cntrSide1Channel.value(), 
                                        self.paramShockPeriod.value(), 
                                        self.paramShockDura.value())
        else:
            self.arenaMain.ard.pinLow(self.cntrSide1Channel.value())
        if bSide2:
            self.arenaMain.ard.pinPulse(self.cntrSide2Channel.value(), 
                                           self.paramShockPeriod.value(), 
                                           self.paramShockDura.value())
        else:
            self.arenaMain.ard.pinLow(self.cntrSide2Channel.value())                   
        """
        elif bLabJack:
            self.pulseMutex.acquire()
            try:
                if bSide1 and not self.shockSide1_t:
                    self.shockSide1_t = time.time()
                    self.bPulseHigh1 = False
                elif not bSide1 and self.shockSide1_t:
                    if self.bPulseHigh1:
                        self.arenaMain.labjack.writeRegister(self.cntrSide1Channel.value(), 0)
                        if self.bRunning: self.avoidData['shockPulses'][self.shockSide1_ndx][3] = self.shockSide1_t + self.paramShockDura.value()/1000
                        if self.bRunning: self.avoidData['shockPulses'][self.shockSide1_ndx][4] = time.time()
                    self.bPulseHigh1 = False
                    self.shockSide1_ndx = None
                    self.shockSide1_t = 0  

                if bSide2 and not self.shockSide2_t:
                    self.shockSide2_t = time.time()
                    self.bPulseHigh2 = False
                elif not bSide2 and self.shockSide2_t:
                    if self.bPulseHigh2:
                        self.arenaMain.labjack.writeRegister(self.cntrSide2Channel.value(), 0)
                        if self.bRunning: self.avoidData['shockPulses'][self.shockSide2_ndx][3] = self.shockSide2_t + self.paramShockDura.value()/1000
                        if self.bRunning: self.avoidData['shockPulses'][self.shockSide2_ndx][4] = time.time()
                    self.bPulseHigh2 = False
                    self.shockSide2_ndx = None
                    self.shockSide2_t = 0               
            finally:
                self.pulseMutex.release()
        """

    def handlePulsedShocks(self):
        pass
        """
        self.pulseMutex.acquire()
        try:
            t = time.time()
            if self.shockSide1_t:
                if not self.bPulseHigh1 and t > self.shockSide1_t:
                    self.arenaMain.labjack.writeRegister(self.cntrSide1Channel.value(), 5)
                    if self.bRunning: self.avoidData['shockPulses'].append([1, self.shockSide1_s, t, -1, -1])
                    self.bPulseHigh1 = True
                    self.shockSide1_ndx = len(self.avoidData['shockPulses'])-1
                elif t > self.shockSide1_t + self.paramShockDura.value()/1000:
                    self.arenaMain.labjack.writeRegister(self.cntrSide1Channel.value(), 0)
                    if self.bRunning: self.avoidData['shockPulses'][self.shockSide1_ndx][3] = self.shockSide1_t + self.paramShockDura.value()/1000
                    if self.bRunning: self.avoidData['shockPulses'][self.shockSide1_ndx][4] = t
                    self.shockSide1_t = self.shockSide1_t + self.paramShockPeriod.value()/1000
                    self.bPulseHigh1 = False
                    self.shockSide1_ndx = None
            if self.shockSide2_t:
                if not self.bPulseHigh2 and t > self.shockSide2_t:
                    self.arenaMain.labjack.writeRegister(self.cntrSide2Channel.value(), 5)
                    if self.bRunning: self.avoidData['shockPulses'].append([2, self.shockSide2_s, t, -1, -1])
                    self.bPulseHigh2 = True
                    self.shockSide2_ndx = len(self.avoidData['shockPulses'])-1
                elif t > self.shockSide2_t + self.paramShockDura.value()/1000:
                    self.arenaMain.labjack.writeRegister(self.cntrSide2Channel.value(), 0)
                    if self.bRunning: self.avoidData['shockPulses'][self.shockSide2_ndx][3] = self.shockSide2_t + self.paramShockDura.value()/1000
                    if self.bRunning: self.avoidData['shockPulses'][self.shockSide2_ndx][4] = t
                    self.shockSide2_t = self.shockSide2_t + self.paramShockPeriod.value()/1000
                    self.bPulseHigh2 = False
                    self.shockSide2_ndx = None
        finally:
            self.pulseMutex.release()
        """

    def readCurrentInput(self):
        return None
        #self.arenaMain.ard.analogRead(self.currInputChannel.value())
        """
        #for labjack
        #when start is pressed arenaMain needs to start labjack streaming
        #and arena main need to handle repeated called to:
        #see LFAnalyze/code/common/labjack_logging for configuration example
        #r = lj.streamData(convert = False).next()
        #r = self.lj.processStreamData(r) #convert to float
        #individual arenas, then need to have access to r, and the computer time
        #of the first sample -- this is important!
        #[r, bLostSample] = self.arenaMain.lj.getStream('AIN0')
        #do I need to do a deep copy here??
        #self.avoidData['current'] = self.avoidData['current'] + r
        """


        
                               

                        




