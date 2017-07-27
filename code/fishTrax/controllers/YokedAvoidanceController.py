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
from transitions import Machine

# Set up state machine logging to std out
import logging
from transitions import logger
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from itertools import tee, izip
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)

class Side:
    S1 = 1
    S2 = -1

class YokedAvoidanceController(ArenaController.ArenaController, Machine):
    def __init__(self, parent, arenaMain, bIsYoked):
        super(YokedAvoidanceController, self).__init__(parent, arenaMain)

        print type(parent)

        #calibration
        self.arenaCamCorners = None
        self.arenaMidLine = []
        self.arenaSide1Sign = 1
        self.arenaProjCorners = []
        self.fishImg = None #image of fish

        #tracking
        self.arenaCvMask = None   

        #state
        self.mutex = Lock()
        states = ['off', 'acclimate', 'baseline', 'trial_running', 'trial_CS', 'trial_CS_and_US', 'trial_US', 'trial_between','post']
        Machine.__init__(self, states=states, initial='off', after_state_change='update_and_save')
        self.add_transition('begin', 'off', 'acclimate', conditions='isReadyToStart')
        self.add_transition('next', 'acclimate', 'baseline')
        self.add_transition('next', 'baseline', 'trial_running')
        self.add_transition('start_shock', 'trial_running', 'trial_US', after='on_start_shock')
        self.add_transition('start_shock', 'trial_CS', 'trial_CS_and_US', after='on_start_shock')
        self.add_transition('start_escape', 'trial_running', 'trial_CS', after='on_start_escape')
        self.add_transition('start_escape', 'trial_US', 'trial_CS_and_US', after='on_start_escape')
        self.add_transition('escape', ['trial_CS','trial_CS_and_US'], 'trial_between', before='on_escape')
        self.add_transition('end_trial', ['trial_running','trial_CS','trial_US','trial_CS_and_US'], 'trial_between', before='on_end_trial')
        self.add_transition('start_trial', 'trial_between', 'trial_running')
        self.add_transition('next', 'trial_between','post')
        self.add_transition('next', 'post', 'off')
        self.add_transition('quit', '*', 'off')
        self.fishPosUpdate = False
        self.fishPos = (0,0)
        self.fishPosBuffer = []
        self.fishPosBufferT = []
        self.currCvFrame = None
        #Note additional state variable will be created during state transitions (like nextStateTime)

        self.bIsYoked = bIsYoked
        self.partnerTank = None
        if self.bIsYoked:
            self.yokedTank = self
            self.masterTank = None
        else:
            self.yokedTank = None
            self.masterTank = self

        #data results
        self.arenaData = None
        self.fishSize = None

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
        self.resetCamCorners = None
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
        self.projSizeL = QtGui.QLabel('Size W,L')
        self.projWid = QtGui.QSpinBox()
        self.projWid.setRange(0,1000)
        self.projWid.setValue(115)
        self.projWid.setMaximumWidth(50)
        self.projLen = QtGui.QSpinBox()
        self.projLen.setRange(0,1000)
        self.projLen.setValue(220)
        self.projLen.setMaximumWidth(50)
        self.projLen.valueChanged.connect(self.projectorPositionChanged)
        self.projWid.valueChanged.connect(self.projectorPositionChanged)
        self.projLayout.addWidget(self.projSizeL,2,0)
        self.projLayout.addWidget(self.projWid,2,1)
        self.projLayout.addWidget(self.projLen,2,2)
        self.projRotL = QtGui.QLabel('Rotation')
        self.projRot = QtGui.QSpinBox()
        self.projRot.setRange(0,360)
        self.projRot.setValue(270)
        self.projRot.setMaximumWidth(50)
        self.projLayout.addWidget(self.projRotL,3,0)
        self.projLayout.addWidget(self.projRot,3,1)
        self.projRot.valueChanged.connect(self.projectorPositionChanged)
        
        self.tankLength = LabeledSpinBox(None, 'Tank Len (mm)', 0,100,46,60)
        self.projLayout.addWidget(self.tankLength, 4,0,1,2)
        self.tankWidth = LabeledSpinBox(None, 'Tank Wid (mm)', 0,100,21,60)
        self.projLayout.addWidget(self.tankWidth, 4,2,1,2)

        self.projLayout.setColumnStretch(6,1)
        self.projGroup.setLayout(self.projLayout)
        self.arenaLayout.addWidget(self.camCalibButton, 0,0)
        self.arenaLayout.addWidget(self.projGroup,1,0)
        self.arenaLayout.setColumnStretch(1,1)
        self.arenaGroup.setLayout(self.arenaLayout)

        #tracking group box
        self.trackWidget = FishTrackerWidget(self, self.arenaMain.ftDisp)

        #start button for individual tank
        self.startButton = QtGui.QPushButton('Start')
        self.startButton.setMaximumWidth(150)
        self.startButton.clicked.connect(self.startstop)
        if self.bIsYoked:
            self.startButton.setDisabled(True)
        
        #whether to save movie  
        self.paramSaveMovie = QtGui.QCheckBox('Save Movie')
            

        #experimental parameters groupbox
        self.paramGroup = QtGui.QGroupBox()
        self.paramGroup.setTitle('Exprimental Parameters')
        self.paramLayout = QtGui.QGridLayout()
        self.paramLayout.setHorizontalSpacing(2)
        self.paramLayout.setVerticalSpacing(2)

        self.paramShockChan1 = LabeledSpinBox(None, 'ShockChan1', 0,10000,53,60)
        self.paramLayout.addWidget(self.paramShockChan1, 0,0,1,2)
        self.paramShockChan2 = LabeledSpinBox(None, 'ShockChan2', 0,10000,52,60)
        self.paramLayout.addWidget(self.paramShockChan2, 0,2,1,2)
        self.paramCurrChan1 = LabeledSpinBox(None, 'CurrChan1', 0,16,15,60)
        self.paramLayout.addWidget(self.paramCurrChan1,1,0,1,2)
        self.paramCurrChan2 = LabeledSpinBox(None, 'CurrChan2', 0,16,14,60)
        self.paramLayout.addWidget(self.paramCurrChan2,1,2,1,2)

        if not self.bIsYoked:
            #high level flow - acclimate -> baseline -> N trials -> post
            self.paramAcclimate = LabeledSpinBox(None, 'Acclimate (m)', 0, 240, 10, 60)
            self.paramLayout.addWidget(self.paramAcclimate, 2,0,1,2)
            self.paramBaseline = LabeledSpinBox(None,'Baseline (m)',0,240,10,60)
            self.paramLayout.addWidget(self.paramBaseline,2,2,1,2)
            self.paramNumTrials = LabeledSpinBox(None,'#Trials',0,500,30,60)
            self.paramLayout.addWidget(self.paramNumTrials,3,0,1,2)
            self.paramPost = LabeledSpinBox(None,'Post (m)',0,240,10,60) #number of side switches post teset
            self.paramLayout.addWidget(self.paramPost,3,2,1,2)

            #trial parameters - (optional cs or us) -> cs and us -> on escape or end ITI.
            self.paramTrialDura = LabeledSpinBox(None, 'Trial (s)', 1,3600,60,60)
            self.paramLayout.addWidget(self.paramTrialDura,4,0,1,2)
            self.paramShockOnset = LabeledSpinBox(None, 'Shock onset (s)',0,3600,0,60)
            self.paramLayout.addWidget(self.paramShockOnset, 5,0,1,2)
            self.paramEscapeOnset = LabeledSpinBox(None, 'Escape onset (s)',0,3600,5,60)
            self.paramLayout.addWidget(self.paramEscapeOnset, 5,2,1,2)
            self.paramITIMin = LabeledSpinBox(None, 'ITI Min (s)',0,3600,15,60)
            self.paramLayout.addWidget(self.paramITIMin, 6,0,1,2)
            self.paramITIMax = LabeledSpinBox(None, 'ITI Max (s)',0,3600,30,60)
            self.paramLayout.addWidget(self.paramITIMax, 6,2,1,2)
            self.paramShockPeriod = LabeledSpinBox(None, 'ShockITI (ms)', 0,5000,1000,60)
            self.paramLayout.addWidget(self.paramShockPeriod, 7,0,1,2)
            self.paramShockDuration = LabeledSpinBox(None, 'ShockPulse (ms)', 0,1000,50,60)
            self.paramLayout.addWidget(self.paramShockDuration, 7,2,1,2)

            self.paramShockV = LabeledSpinBox(None, 'ShockV', 0,100, 5,60)
            self.paramLayout.addWidget(self.paramShockV, 8,0,1,2)
            (self.paramColorNeutral,self.labelColorNeutral) = self.getColorComboBox('Neutral', 0)
            self.paramLayout.addWidget(self.paramColorNeutral,9,0)
            self.paramLayout.addWidget(self.labelColorNeutral,9,1)
            (self.paramColorEscape,self.labelColorEscape) = self.getColorComboBox('Escape', 0)
            self.paramLayout.addWidget(self.paramColorEscape,9,2)
            self.paramLayout.addWidget(self.labelColorEscape,9,3)
            (self.paramColorAvoid,self.labelColorAvoid) = self.getColorComboBox('Avoid', 2)
            self.paramLayout.addWidget(self.paramColorAvoid,10,0)
            self.paramLayout.addWidget(self.labelColorAvoid,10,1)
            self.paramDynamic= QtGui.QCheckBox('Dynamic Escape')
            self.paramLayout.addWidget(self.paramDynamic,11,0,1,2)
            self.paramEscapePos = QtGui.QDoubleSpinBox()
            self.paramEscapePos.setRange(0,1)
            self.paramEscapePos.setValue(.5)
            self.labelEscapePos = QtGui.QLabel('escape pos (0-1)')
            self.paramLayout.addWidget(self.paramEscapePos,11,2)
            self.paramLayout.addWidget(self.labelEscapePos,11,3)
            self.paramDynamicDraw = QtGui.QCheckBox('Dynamic Draw')
            self.paramDynamicDraw.setChecked(True)
            self.paramLayout.addWidget(self.paramDynamicDraw,12,0,1,2)
            self.paramDebug = QtGui.QPushButton('Debug')
            self.paramDebug.setMaximumWidth(150)
            self.paramDebug.setCheckable(True)
            self.paramLayout.addWidget(self.paramDebug,12,2,1,2)
            self.paramDebug.clicked.connect(self.useDebugParams)
        else:
            self.paramYokedLabel = QtGui.QLabel('Other params are yoked to another tank')
            self.paramLayout.addWidget(self.paramYokedLabel,3,0,1,4)
        self.paramGroup.setLayout(self.paramLayout)

        #Experimental info group
        self.infoGroup = QtGui.QGroupBox()
        self.infoGroup.setTitle('Experiment Info')
        self.infoLayout = QtGui.QGridLayout()
        self.infoLayout.setHorizontalSpacing(3)
        self.infoLayout.setVerticalSpacing(3)

        self.labelDir = QtGui.QLabel('Dir: ')
        self.infoDir = PathSelectorWidget(browseCaption='Experimental Data Directory', default=os.path.expanduser('~/data/test'))
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
        self.settingsLayout.addWidget(self.infoGroup,2,0,1,2)
        self.settingsLayout.addWidget(self.startButton,3,0,1,1)
        self.settingsLayout.addWidget(self.paramSaveMovie,3,1,1,1)
        self.settingsLayout.addWidget(self.paramGroup,4,0,1,2)
        self.setLayout(self.settingsLayout)

        #HACK Couldn't quick initialize arena lcation until after frist image arrives, so stuck in onNewFrame

        #initialize projector
        self.projectorPositionChanged()
        self.t = 0

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

    def setPartnerTank(self, partnerArena):
        self.partnerTank = partnerArena
        if self.bIsYoked:
            self.masterTank = partnerArena
        else:
            self.yokedTank = partnerArena

    def configTank(self, ardConfig, camPos, projPos):
        #config arduino
        self.paramShockChan1.setValue(ardConfig[0])
        self.paramShockChan2.setValue(ardConfig[1])
        self.paramCurrChan1.setValue(ardConfig[2])
        self.paramCurrChan2.setValue(ardConfig[3])
        
        #set tank position in camera
        self.resetCamCorners = camPos

        #set tank position in projector
        self.projX.setValue(projPos[0])
        self.projY.setValue(projPos[1])
        self.projWid.setValue(projPos[2])
        self.projLen.setValue(projPos[3])
        self.projRot.setValue(projPos[4])
        

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
                #if experiment is running then keep track of the average fish speed in one minute blocks
                if not self.is_off():
                    self.fishPosBuffer.append(pos)
                    self.fishPosBufferT.append(time)
                    if (self.fishPosBufferT[-1] - self.fishPosBufferT[0]) > 60:                       
                        self.fishPosBuffer = [np.sqrt((f1[0]-f0[0])**2 + (f1[1]-f0[1])**2) for f0, f1 in pairwise(self.fishPosBuffer)]
                        self.averageSpeed.append(np.mean(self.fishPosBuffer)/(self.fishPosBufferT[-1] - self.fishPosBufferT[0])) #pixels/sec
                        self.fishPosBuffer = []
                        self.fishPosBufferT = []

            if not self.is_off():
                #record location
                self.arenaData['video'].append((self.frameTime, None)) 
                d = [self.frameTime, pos[0], pos[1]]
                self.arenaData['tracking'].append(tuple(d))
                if self.paramSaveMovie.isChecked():                
                    img = np.array(self.currCvFrame[:,:]) #convert IplImage into numpy array
                    img = img[self.arenaBB[0][1]:self.arenaBB[1][1],self.arenaBB[0][0]:self.arenaBB[1][0]] 
                    self.movie_logger.write_frame(img)

            self.arenaView = view

            #HACK: couldn't quickly initilize cam corner before currCvFrame is set, so I stuck it here.
            #not a great place since conditoin will be checked frequently
            if self.resetCamCorners is not None:
                self.setArenaCamCorners(self.resetCamCorners)
                self.resetCamCorners = None

        except:
            print 'ClassicalConditioningController:onNewFrame failed'
            traceback.print_exc()
            QtCore.pyqtRemoveInputHook() 
            ipdb.set_trace()
        finally:
            self.mutex.release()

  
    def updateState(self):
        if not self.bIsYoked:
            self.updateExperimentalState()
        else:
            #state is managed by master tank
            pass

    def updateExperimentalState(self):
        if not self.is_off():
            self.mutex.acquire()
            try:
                self.t = time.time()
                if self.yokedTank:
                    self.yokedTank.t = self.t

                #Check if it time to transition to next high level state (acclimate->baseline->trials->post->off)
                if self.t > self.nextStateTime:
                    self.next(); 
                    if self.yokedTank: 
                        self.yokedTank.next()

                #If we are between trials, check if it is time to start next trial
                if self.is_trial_between() and self.t > self.nextTrialTime:
                    self.start_trial(); 
                    if self.yokedTank: 
                        self.yokedTank.start_trial();

                #If we are current running a trial...
                if self.is_trial_running() or self.is_trial_US() or self.is_trial_CS() or self.is_trial_CS_and_US():
                    #then check it is time to make escape possible (CS)...
                    if (self.is_trial_running() or self.is_trial_US()) and self.t > self.trialStartEscapeTime:
                        self.start_escape(); 
                        if self.yokedTank: 
                            self.yokedTank.start_escape();
                    #then check if is time to start shocking (US)...
                    if (self.is_trial_running() or self.is_trial_CS()) and self.t > self.trialStartShockTime:
                        self.start_shock(); 
                        if self.yokedTank: 
                            self.yokedTank.start_shock();

                    #If escape is possible then check if fish escaped...
                    bEscaped=False
                    if self.is_trial_CS() or self.is_trial_CS_and_US():
                        if self.fishPosUpdate:
                            #if updateState is called more freq then on_new_Frame then this condition saves computation
                            self.fishPosUpdate = False
                            bEscaped = self.isOnSide(self.fishPos, self.escapeLine, self.escapeSign)
                            if bEscaped:
                                self.escape(); 
                                if self.yokedTank: 
                                    self.yokedTank.end_trial() #yoked fish never escape

                    #If trial is over and fish didn't escape then transition to trial_between...
                    if self.t > self.trialEndTime and not bEscaped:
                        self.end_trial(); 
                        if self.yokedTank: 
                            self.yokedTank.end_trial()

                    #if we now in between trials because fish escaped or trial ended...
                    if self.is_trial_between():
                        #then check if time to move to post:
                        if self.nTrial >= self.masterTank.paramNumTrials.value() :
                            self.next(); 
                            if self.yokedTank: 
                                self.yokedTank.next()
            except:
                print 'ContextualHelplessnessController:updateState failed'
                traceback.print_exc()
                QtCore.pyqtRemoveInputHook()
                ipdb.set_trace()
            finally:
                self.mutex.release()

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
        if self.is_off() and self.projCalibButton.isChecked() and self.isCurrent():
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
            side1Color = self.getSide1ColorNdx()
            side2Color = self.getSide2ColorNdx()

            if (self.is_trial_CS() or self.is_trial_CS_and_US()) and self.masterTank.paramDynamicDraw.isChecked():
                a = float(1-self.escapePos)
                b = float(self.escapePos)
            else:
                a = 0.5
                b = 1.0 - a

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

    def drawDisplayOverlay(self, painter):
        #draw the fish position
        if self.fishPos and self.fishPos[0] > 0:
            brush = QtGui.QBrush(QtCore.Qt.red)
            painter.setBrush(brush)
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawEllipse(QtCore.QPointF(self.fishPos[0],self.fishPos[1]), 3,3)
            
        #draw escape line
        if self.is_trial_CS() or self.is_trial_CS_and_US(): 
            pen = QtGui.QPen()
            pen.setColor(QtCore.Qt.red)
            pen.setWidth(1)
            painter.setPen(pen)
            l = self.escapeLine
            painter.drawLine(QtCore.QPointF(l[0][0],l[0][1]), QtCore.QPointF(l[1][0],l[1][1]))

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
                statustext = ""
                if self.bIsYoked:
                    statustext = statustext + "Yoked. "
                statustext = statustext + self.state
                if self.is_acclimate() or self.is_baseline():
                    statustext = statustext + ": %0.1f"%(self.nextStateTime-self.t)
                if self.is_trial_running() or self.is_trial_US() or self.is_trial_CS() or self.is_trial_CS_and_US():
                    statustext = statustext + ": %d/%d %d %0.1f"%(self.nTrial, self.masterTank.paramNumTrials.value(), self.nEscape, self.trialEndTime-self.t)
                if self.is_trial_between():
                    statustext = statustext + ": %d/%d %d %0.1f"%(self.nTrial, self.masterTank.paramNumTrials.value(), self.nEscape, self.nextTrialTime-self.t)
                if self.is_post():
                    statustext = statustext + ": %0.1f %d"%(self.nextStateTime-self.t, self.nEscape)
                painter.drawText(self.arenaCamCorners[0][0],self.arenaCamCorners[0][1],statustext)

                #Plot average speed of fish overtime
                if not self.is_off() and len(self.averageSpeed)>2:
                    totalDuration = self.masterTank.paramAcclimate.value()+self.masterTank.paramBaseline.value()+self.masterTank.paramPost.value()
                    totalDuration += self.masterTank.paramNumTrials.value() * (self.masterTank.paramITIMax.value() + self.masterTank.paramTrialDura.value())/60.0
                    totalDuration = totalDuration*(60/60.0) #averaging every 20 seconds (see onnewframe)
                    ndx = np.arange(len(self.averageSpeed))
                    x = (np.arange(len(self.averageSpeed))/totalDuration) 
                    x = x * np.array((self.arenaCamCorners[1][0] - self.arenaCamCorners[0][0])) 
                    x = x + self.arenaCamCorners[0][0]
                    #scale = 75 / np.max(self.averageSpeed)
                    scale = 3000
                    y = self.arenaCamCorners[0][1] - (scale * np.array(self.averageSpeed))
                    for ((x1,x2),(y1,y2)) in zip(pairwise(x),pairwise(y)):
                        painter.drawLine(x1,y1,x2,y2)


    def start(self):
        if not self.bIsYoked:
            self.startstop()

    def stop(self):
        if not self.bIsYoked:
            self.startstop()

    #---------------------------------------------------
    # STATE MACHINE CALLBACK METHODS
    #---------------------------------------------------

    def update_and_save(self):
        # runs on every state transition...
        self.updateProjectorDisplay()
        self.arenaData['stateinfo'].append((self.t, self.getStateNumber(self.state), self.getSide1ColorName(), self.getSide2ColorName(), self.state))
        self.saveResults()

    def on_enter_acclimate(self):
        #experiment has started so disable parts of UI
        self.paramGroup.setDisabled(True)
        self.infoGroup.setDisabled(True)
        self.startButton.setText('Stop')

        #experiment has started so prepare result files and data structures
        td = datetime.datetime.now()
        self.saveLocation = str(self.infoDir.text())
        [p, self.fnResults] = os.path.split(self.saveLocation)
        self.fnResults = self.fnResults + '_' + td.strftime('%Y-%m-%d-%H-%M-%S')
        self.jsonFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '.json'

        #prepare to write movie
        if self.paramSaveMovie.isChecked():
            self.movieFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '.mp4'
            from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter as VidWriter
            self.movie_logger = VidWriter(filename=self.movieFileName,
                                          size=(self.arenaBB[1][0] - self.arenaBB[0][0],
                                                self.arenaBB[1][1] - self.arenaBB[0][1]),
                                          fps=15,
                                          codec='mpeg4',
                                          preset='ultrafast')

        self.initArenaData()
        self.averageSpeed = []
        self.nextStateTime = self.t + self.masterTank.paramAcclimate.value()*60
        self.nEscape = 0
        self.setShockState(False,False) #just to be sure

    def on_enter_baseline(self):
        self.nextStateTime = self.t + self.masterTank.paramBaseline.value()*60

    def on_exit_baseline(self):
        self.nextStateTime = float("inf") # we are now starting trials so next state will depend on num trials.
        self.nTrial = 0 # set/reset the triil count

    def on_enter_trial_running(self):
        self.trialStartEscapeTime = self.t + self.masterTank.paramEscapeOnset.value()
        self.trialStartShockTime = self.t + self.masterTank.paramShockOnset.value()
        self.trialEndTime = self.t + self.masterTank.paramTrialDura.value()
        self.arenaData['trials'].append({'trialNum':self.nTrial,
                                         'startT':self.t,
                                         'side':None,
                                         'escape':None,
                                         'escapeStartT':None,
                                         'shockStartT':None,
                                         'bEscaped':None,
                                         'endT':None})

    def on_start_escape(self):
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
        if not self.masterTank.paramDynamic.isChecked():
            if self.trialSide == Side.S1:
                self.escapePos = self.masterTank.paramEscapePos.value()
            else:
                self.escapePos = 1 - self.masterTank.paramEscapePos.value()
        else:
            if self.trialSide == Side.S1:
                self.escapePos = relPos + (1-relPos)*self.masterTank.paramEscapePos.value()
            else:
                self.escapePos = relPos - relPos*self.masterTank.paramEscapePos.value()

        #convert relative escape position into a line
        (self.escapeLine, side1Sign) = self.processArenaCorners(self.arenaCamCorners, self.escapePos)
        self.escapeSign = -1 * self.trialSide * self.arenaSide1Sign

        #save details of escape line to results
        self.arenaData['trials'][self.nTrial]['side'] = self.trialSide
        self.arenaData['trials'][self.nTrial]['escape'] = (self.escapeLine, self.escapeSign)
        self.arenaData['trials'][self.nTrial]['escapeStartT'] = self.t

    def on_start_shock(self):
        #self.setShockState(self.trialSide == Side.S1, self.trialSide == Side.S2)
        self.setShockState(True, True)
        self.arenaData['trials'][self.nTrial]['shockStartT'] = self.t

    def on_escape(self):
        self.nEscape+=1
        self.arenaData['trials'][self.nTrial]['bEscaped']=True

    def on_end_trial(self):
        self.arenaData['trials'][self.nTrial]['bEscaped']=False

    def on_enter_trial_between(self):
        self.escapeLine = []
        self.setShockState(False, False)
        self.arenaData['trials'][self.nTrial]['endT'] = self.t
        self.nTrial += 1
        self.nextTrialTime = self.t + random.randint(self.masterTank.paramITIMin.value(),self.masterTank.paramITIMax.value())

    def on_enter_post(self):
        self.nextStateTime = self.t + self.masterTank.paramPost.value() * 60

    def on_enter_off(self):
        self.nextStateTime = None

        #the off state can be forced by a button click, so we need to disable shock incase this occured mid trial.
        self.setShockState(False,False)

        #note: the projector colors will be reset on call to after_state_change
        if self.paramSaveMovie.isChecked():
            self.movie_logger.close()

        #experiment has ended so enable parts of UI
        self.paramGroup.setDisabled(False)
        self.infoGroup.setDisabled(False)
        self.startButton.setText('Start')

    def isReadyToStart(self):
        if not os.path.exists(self.infoDir.text()):
            try:
                os.mkdir(self.infoDir.text())
            except:
                self.arenaMain.statusBar().showMessage('%s arena not ready to start.  Experiment directory does not exist and cannot be created.'%(self.getYokedStr()))
                return False

        if not self.arenaCamCorners:
            self.arenaMain.statusBar().showMessage('%s arena not ready to start.  The arena location has not been specified.'%(self.getYokedStr()))
            return False

        if not self.trackWidget.getBackgroundImage():
            self.arenaMain.statusBar().showMessage('%s arena not ready to start.  Background image has not been taken.'%(self.getYokedStr()))
            return False

        #if not self.fishImg:
        #    self.arenaMain.statusBar().showMessage('%s arena not ready to start.  Fish image has not been taken.'%(self.getYokedStr()))
        #    return False

        if not self.bIsYoked and self.yokedTank:
            return self.yokedTank.isReadyToStart()

        return True

    #---------------------------------------------------
    # SLOT CALLBACK METHODS
    #---------------------------------------------------

    def startstop(self):
        self.mutex.acquire()
        try:
            self.t = time.time()
            if self.yokedTank:
                self.yokedTank.t = self.t

            if self.is_off():
                self.begin()
                if self.yokedTank and not self.is_off():
                    self.yokedTank.begin()
            else:
                self.quit(); 
                if self.yokedTank: 
                    self.yokedTank.quit() 
        except:
            print 'ContextualHelplessnessController:startSwitches failed'
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
                self.setArenaCamCorners(self.arenaCamCorners)
               
    def setArenaCamCorners(self, corners):
        #corners must be tuple of tuples (not list or np.array)
        self.currArenaclick=4
        self.arenaCamCorners = corners
        print corners
        [self.arenaMidLine, self.arenaSide1Sign] = self.processArenaCorners(self.arenaCamCorners, .5)
        #compute bounding box with vertical and horizontal sides.
        self.arenaBB = [[min([p[0] for p in corners]), min([p[1] for p in corners])],
                        [max([p[0] for p in corners]), max([p[1] for p in corners])]]
        #bounding box needs to have even heights and widths in order to save as mp4
        if (self.arenaBB[1][0] - self.arenaBB[0][0]) % 2:
            self.arenaBB[1][0] += 1
        if (self.arenaBB[1][1] - self.arenaBB[0][1]) % 2:
            self.arenaBB[1][1] += 1


        self.getArenaMask()
        self.trackWidget.setBackgroundImage()
                                             
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

    def getYokedStr(self):
        if self.bIsYoked:
            return 'Yoked'
        else:
            return 'Master'

    def getStateNumber(self,state):
        #this function maps a high level state number to keep arenaData compatible with older datafiles.
        if self.state == 'off':
            return 0
        elif self.state == 'acclimate':
            return 4
        elif self.state == 'baseline':
            return 8
        elif self.state.startswith('trial'):
            return 12
        elif self.state == 'post':
            return 20
        raise('State not recognized')


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



        self.arenaData['parameters'] = { 'bIsYoked': self.bIsYoked,
                                         'partnerTank': str(self.partnerTank.infoDir.text()),
                                         'Acclimate (m)':self.masterTank.paramAcclimate.value(),
                                         'Baseline (m)':self.masterTank.paramBaseline.value(),
                                         'NumTrials':self.masterTank.paramNumTrials.value(),
                                         'Post (m)':self.masterTank.paramPost.value(),
                                         'Trial Duration (s)':self.masterTank.paramTrialDura.value(),
                                         'Shock Onset (s)': self.masterTank.paramShockOnset.value(),
                                         'Escape Onset (s)': self.masterTank.paramEscapeOnset.value(),
                                         'ITI Min (s)':self.masterTank.paramITIMin.value(),
                                         'ITI Max (s)':self.masterTank.paramITIMax.value(),
                                         'shock period (ms)':self.masterTank.paramShockPeriod.value(),
                                         'shock dura (ms)':self.masterTank.paramShockDuration.value(),
                                         'shock chan 1':self.paramShockChan1.value(),
                                         'shock chan 2':self.paramShockChan2.value(),
                                         'curr chan 1':self.paramCurrChan1.value(),
                                         'curr chan 2':self.paramCurrChan2.value(),
                                         'shock V':self.masterTank.paramShockV.value(),
                                         'NeutralColor':str(self.masterTank.paramColorNeutral.currentText()),
                                         'AvoidColor':str(self.masterTank.paramColorAvoid.currentText()),
                                         'EscapeColor':str(self.masterTank.paramColorEscape.currentText()),                                       
                                         'isDynamicEscape':self.masterTank.paramDynamic.isChecked(),
                                         'inDynamicDraw':self.masterTank.paramDynamicDraw.isChecked(),
                                         'fEscapePosition':self.masterTank.paramEscapePos.value(),
                                         'states':self.states.keys(),
                                         'state2num': [(key, self.getStateNumber(key)) for key in self.states.keys()],
                                         'CodeVersion':None }

        self.arenaData['trackingParameters'] = self.trackWidget.getParameterDictionary()
        self.arenaData['trackingParameters']['arenaPoly'] = self.arenaCamCorners 
        self.arenaData['trackingParameters']['arenaDivideLine'] = self.arenaMidLine
        self.arenaData['trackingParameters']['arenaSide1Sign'] = self.arenaSide1Sign
        self.arenaData['projectorParameters'] = {'position':[self.projX.value(), self.projY.value()],
                                                 'size':[self.projLen.value(), self.projWid.value()],
                                                 'rotation':self.projRot.value()}
        self.arenaData['tankSize_mm'] = [self.tankLength.value(), self.tankWidth.value()]
        self.arenaData['trials'] = list() #outcome on each trial
        self.arenaData['tracking'] = list() #list of tuples (frametime, posx, posy)
        self.arenaData['video'] = list() #list of tuples (frametime, filename)	
        self.arenaData['stateinfo'] = list() #list of times at switch stimulus flipped.
        self.arenaData['shockinfo'] = list()

        t = datetime.datetime.now()
      
        #save experiment images
        self.bcvImgFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '_BackImg_' + t.strftime('%Y-%m-%d-%H-%M-%S') + '.tiff'
        cv.SaveImage(self.bcvImgFileName, self.trackWidget.getBackgroundImage())	
        if self.fishImg:
            self.fishImgFileName = str(self.infoDir.text()) + os.sep +  self.fnResults + '_FishImg_' + t.strftime('%Y-%m-%d-%H-%M-%S') + '.tiff'
            cv.SaveImage(self.fishImgFileName, self.fishImg)

    def saveResults(self):
        f = open(name=self.jsonFileName, mode='w')
        json.dump(self.arenaData,f)
        f.close()

    def getSideColors(self):
        if self.is_off() or self.is_acclimate() or self.is_baseline() or self.is_post() or self.is_trial_between() or self.is_trial_running():
            return (self.masterTank.paramColorNeutral.currentIndex(), self.masterTank.paramColorNeutral.currentIndex(),
                    str(self.masterTank.paramColorNeutral.currentText()), str(self.masterTank.paramColorNeutral.currentText()))
        if self.is_trial_US():
            return (self.masterTank.paramColorAvoid.currentIndex(), self.masterTank.paramColorAvoid.currentIndex(),
                    str(self.masterTank.paramColorAvoid.currentText()), str(self.masterTank.paramColorAvoid.currentText()))
        elif self.is_trial_CS() or self.is_trial_CS_and_US():
            if self.trialSide == Side.S1:
                return (self.masterTank.paramColorAvoid.currentIndex(),     self.masterTank.paramColorEscape.currentIndex(),
                    str(self.masterTank.paramColorAvoid.currentText()), str(self.masterTank.paramColorEscape.currentText()))
            else:
                return (self.masterTank.paramColorEscape.currentIndex(),     self.masterTank.paramColorAvoid.currentIndex(),
                    str(self.masterTank.paramColorEscape.currentText()), str(self.masterTank.paramColorAvoid.currentText()))
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

        if not bSide1 and not bSide2:
            self.arenaMain.ard.pinLow(self.paramShockChan1.value())
            curr1 = 0
            self.arenaMain.ard.pinLow(self.paramShockChan2.value())
            curr2 = 0
        elif bSide1 and not bSide2:
            curr1 = self.arenaMain.ard.pinPulse(self.paramShockChan1.value(), 
                                        self.masterTank.paramShockPeriod.value(),
                                        self.masterTank.paramShockDuration.value(),
                                        feedbackPin = self.paramCurrChan1.value())
            self.arenaMain.ard.pinLow(self.paramShockChan2.value())
            curr2 = 0
        elif bSide2 and not bSide1:
            self.arenaMain.ard.pinLow(self.paramShockChan1.value())
            curr1 = 0
            curr2 = self.arenaMain.ard.pinPulse(self.paramShockChan2.value(), 
                                           self.masterTank.paramShockPeriod.value(),
                                           self.masterTank.paramShockDuration.value(),
                                           feedbackPin = self.paramCurrChan2.value())
        elif bSide1 and bSide2:
            #turn on in random order and measure current for second one (since measuring current add 7ms delay)
            curr1 = -1
            curr2 = -1
            if np.random.rand() < 0.5:
                self.arenaMain.ard.pinPulse(self.paramShockChan1.value(),
                                            self.masterTank.paramShockPeriod.value(),
                                            self.masterTank.paramShockDuration.value())
                curr2 = self.arenaMain.ard.pinPulse(self.paramShockChan2.value(),
                                                    self.masterTank.paramShockPeriod.value(),
                                                    self.masterTank.paramShockDuration.value(),
                                                    feedbackPin = self.paramCurrChan2.value())
            else:
                self.arenaMain.ard.pinPulse(self.paramShockChan2.value(),
                                            self.masterTank.paramShockPeriod.value(),
                                            self.masterTank.paramShockDuration.value())
                curr1 = self.arenaMain.ard.pinPulse(self.paramShockChan1.value(),
                                                    self.masterTank.paramShockPeriod.value(),
                                                    self.masterTank.paramShockDuration.value(),
                                                    feedbackPin = self.paramCurrChan1.value())

        print 'Shock state changed: state:',bSide1,bSide2,' curr:',curr1,curr2
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

    def useDebugParams(self):
        pass
