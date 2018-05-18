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

class OMRController(ArenaController.ArenaController, Machine):
    def __init__(self, parent, arenaMain):
        super(OMRController, self).__init__(parent, arenaMain)

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
        states = ['off', 'between_session', 'omr_to_s1', 'no_omr_post_s1', 'omr_to_s2', 'no_omr_post_s2'] # off between L-N-R-N-L-N-R between LNRNLNR between off
        Machine.__init__(self, states=states, initial='off', after_state_change='update_state_data')

        self.add_transition('begin', 'off', 'between_session', conditions='isReadyToStart')
        self.add_transition('start_session', 'between_session', 'omr_to_s1')
        self.add_transition('start_omr', 'no_omr_post_s1', 'omr_to_s2')
        self.add_transition('start_omr', 'no_omr_post_s2', 'omr_to_s1')
        self.add_transition('stop_omr', 'omr_to_s1', 'no_omr_post_s1')
        self.add_transition('stop_omr', 'omr_to_s2', 'no_omr_post_s2')
        self.add_transition('stop_session', ['omr_to_s1', 'omr_to_s2', 'no_omr_post_s1', 'no_omr_post_s2'], 'between_session')
        self.add_transition('quit', '*', 'off')

        self.fishPosUpdate = False
        self.fishPos = (0,0)
        self.fishPosBuffer = []
        self.fishPosBufferT = []
        self.currCvFrame = None
        #Note additional state variable will be created during state transitions (like nextStateTime)

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
        
        #whether to save movie  
        self.paramSaveMovie = QtGui.QCheckBox('Save Movie')
            
        #experimental parameters groupbox
        self.paramGroup = QtGui.QGroupBox()
        self.paramGroup.setTitle('Exprimental Parameters')
        self.paramLayout = QtGui.QGridLayout()
        self.paramLayout.setHorizontalSpacing(2)
        self.paramLayout.setVerticalSpacing(2)

        #high level flow - Between - OMR Session ( OMRS1 - pause - OMRS2
        self.paramNumSession = LabeledSpinBox(None, 'Number of Sessions', 0, 200, 20, 60) #Number of Sessions (a cluster of OMR tests)
        self.paramLayout.addWidget(self.paramNumSession, 1,0,1,2) 
        self.paramBetween = LabeledSpinBox(None, 'Between Sessions (s)', 0, 1200, 300, 60)
        self.paramLayout.addWidget(self.paramBetween, 1,2,1,2)
        self.paramOMRPerSession = LabeledSpinBox(None,'#OMR Per Session', 0 ,10,4,60) # Number of OMR tests per session
        self.paramLayout.addWidget(self.paramOMRPerSession, 2,0,1,2)        
        self.paramOMRDuration = LabeledSpinBox(None,'OMR Duration (s)',0,60,12,60) #duration of each OMR tests
        self.paramLayout.addWidget(self.paramOMRDuration, 2,2,1,2)
        self.paramOMRInterval = LabeledSpinBox(None,'OMR Interval (s)',0,60 ,3 ,60) #time between OMR tests
        self.paramLayout.addWidget(self.paramOMRInterval,3,0,1,2)
 
        #Vision properities of OMR
        self.paramOMRPeriod = LabeledSpinBox(None,'OMR Grating Period (mm)',0,50,5,60) #spacing between grating bars
        self.paramLayout.addWidget(self.paramOMRPeriod,4,0,1,2)
        self.paramOMRDutyCycle = LabeledSpinBox(None, 'OMR DutyCycle %',0,100,50,60) #width of grating bars
        self.paramLayout.addWidget(self.paramOMRDutyCycle,4,2,1,2)
        self.paramOMRVelocity = LabeledSpinBox(None, 'OMR Speed (mm/s)',0,50,5,60) #velocity of moving gratings.
        self.paramLayout.addWidget(self.paramOMRVelocity,5,0,1,2)

        (self.paramColorNeutral,self.labelColorNeutral) = self.getColorComboBox('Neutral', 0)
        self.paramLayout.addWidget(self.paramColorNeutral,6,0)
        self.paramLayout.addWidget(self.labelColorNeutral,6,1)
        (self.paramColorOMR,self.labelColorOMR) = self.getColorComboBox('OMR', 5)
        self.paramLayout.addWidget(self.paramColorOMR,6,2)
        self.paramLayout.addWidget(self.labelColorOMR,6,3)
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

    def configTank(self, ardConfig, camPos, projPos):
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
                    if (self.fishPosBufferT[-1] - self.fishPosBufferT[0]) > 60: #averaging every 60 seconds, must match constant in drawDisplayOverlay               
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
        self.updateExperimentalState()
        
    def updateExperimentalState(self):
        if not self.is_off():
            self.mutex.acquire()
            try:
                self.t = time.time()

                #Check if it time to transition to next high level state (acclimate->baseline->trials->post->off)
                if self.t > self.nextStateTime:
                    if self.is_between_session():
                        if self.nSession < self.paramNumSession.value():
                            self.nOMR = 0 #TODO move to callback for start session
                            self.nSession+=1 #TODO move to callback for start session
                            self.start_session()
                        else:
                            self.quit()

                    elif self.is_omr_to_s1() or self.is_omr_to_s2():
                        self.stop_omr()
                            
                    elif self.is_no_omr_post_s1() or self.is_no_omr_post_s2():
                        if self.nOMR < self.paramOMRPerSession.value():
                            self.start_omr()
                        else:
                            self.stop_session()

                #handle omr projector updates
                if self.is_omr_to_s1() or self.is_omr_to_s2():
                    if self.t - self.omrLastUpdate > 0.010: #only updated display once sufficient time has passed.
                        if self.t - self.omrLastUpdate > 0.060:
                            print 'WARNING: projector slow to update', self.t - self.omrLastUpdate
                        self.updateProjectorDisplay()

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
            #Draw Background
            backColor = self.paramColorNeutral.currentIndex()
            pen = QtGui.QPen(QtCore.Qt.NoPen)
            brush = self.getBrush(backColor)
            painter.setBrush(brush)
            painter.setPen(pen)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(self.pts[0,0], self.pts[0,1]))
            poly.append(QtCore.QPointF(self.pts[1,0], self.pts[1,1]))
            poly.append(QtCore.QPointF(self.pts[2,0], self.pts[2,1]))
            poly.append(QtCore.QPointF(self.pts[3,0], self.pts[3,1]))          
            painter.drawPolygon(poly)

            #Draw OMR grating
            if self.is_omr_to_s1() or self.is_omr_to_s2():
                #update the possition according to time since last update.
                if self.is_omr_to_s1():
                    self.omrPhase -= (float(self.paramOMRVelocity.value())/float(self.paramOMRPeriod.value())) * 360.0 * (self.t-self.omrLastUpdate)
                else:
                    self.omrPhase += (float(self.paramOMRVelocity.value())/float(self.paramOMRPeriod.value())) * 360.0 * (self.t-self.omrLastUpdate)
                self.omrPhase = self.omrPhase%360.0
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
            if len(self.arenaCamCorners) >= 2:
                pen = QtGui.QPen(QtCore.Qt.red)
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawLine(self.arenaCamCorners[0][0],self.arenaCamCorners[0][1],
                                 self.arenaCamCorners[1][0],self.arenaCamCorners[1][1])
                painter.setPen(QtGui.QColor(168, 34, 3))
                painter.setFont(QtGui.QFont('Decorative',14))

                statustext = ""
                statustext = statustext + self.state
                if not self.is_off():
                    statustext = statustext + ": %d/%d %0.1f"%(self.nSession, self.paramNumSession.value(), self.nextStateTime-self.t)
                if self.is_omr_to_s1() or self.is_omr_to_s2() or self.is_no_omr_post_s1() or self.is_no_omr_post_s2():
                    statustext = statustext + ": %d/%d"%(self.nOMR, self.paramOMRPerSession.value())

                painter.drawText(self.arenaCamCorners[0][0],self.arenaCamCorners[0][1],statustext)

                #Plot average speed of fish overtime
                if not self.is_off() and len(self.averageSpeed)>2:
                    ac = np.array(self.arenaCamCorners)
                    plt_b = np.max(ac[:,1]) #Plot bottom
                    plt_l = np.min(ac[:,0]) #Plot left
                    plt_r = np.max(ac[:,0]) #Plot right

                    totalDuration = self.paramBetween.value() + self.paramNumSession.value()*(self.paramBetween.value()+
                                    self.paramOMRPerSession.value() * (self.paramOMRDuration.value() + self.paramOMRInterval.value()))
                    totalDuration = totalDuration*(60/60.0) #averaging every N seconds (see onnewframe)
                    ndx = np.arange(len(self.averageSpeed))
                    x = (np.arange(len(self.averageSpeed))/totalDuration) 
                    x = x * (plt_r - plt_l) 
                    x = x + plt_l
                    #scale = 75 / np.max(self.averageSpeed)
                    scale = 3000
                    y = plt_b - (scale * np.array(self.averageSpeed))
                    for ((x1,x2),(y1,y2)) in zip(pairwise(x),pairwise(y)):
                        painter.drawLine(x1,y1,x2,y2)


    def start(self):
        self.startstop()

    def stop(self):
        self.startstop()

    #---------------------------------------------------
    # STATE MACHINE CALLBACK METHODS
    #---------------------------------------------------

    def update_state_data(self):
        # runs on every state transition...
        self.updateProjectorDisplay()
        self.arenaData['stateinfo'].append((self.t, 0, 0, 0, self.state))
        #self.saveResults() #just save at end to avoid long interframe intervals

    def on_exit_off(self):
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
        self.nSession = 0
        self.averageSpeed = []

    def on_enter_between_session(self):
        self.nextStateTime = self.t + self.paramBetween.value()

    def on_enter_omr_to_s1(self):
        self.nOMR += 1
        self.nextStateTime = self.t + self.paramOMRDuration.value()
        self.omrPhase = 0
        self.omrLastUpdate = self.t #updates everytime the projectory updates 
        self.updateProjectorDisplay()

    def on_exit_omr_to_s1(self):
        self.updateProjectorDisplay()

    def on_enter_omr_to_s2(self):
        self.nOMR += 1
        self.nextStateTime = self.t + self.paramOMRDuration.value()
        self.omrPhase = 0 
        self.omrLastUpdate = self.t #updates everytime the projectory updates 
        self.updateProjectorDisplay()

    def on_exit_omr_to_s2(self):
        self.updateProjectorDisplay()

    def on_enter_no_omr_post_s1(self):
        self.nextStateTime = self.t + self.paramOMRInterval.value()
        self.updateProjectorDisplay()

    def on_enter_no_omr_post_s2(self):
        self.nextStateTime = self.t + self.paramOMRInterval.value()
        self.updateProjectorDisplay()

    def on_enter_off(self):
        self.nextStateTime = None
        self.updateProjectorDisplay()

        self.saveResults()

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

        return True

    #---------------------------------------------------
    # SLOT CALLBACK METHODS
    #---------------------------------------------------

    def startstop(self):
        self.mutex.acquire()
        try:
            self.t = time.time()

            if self.is_off():
                self.begin()
            else:
                self.quit(); 
        except:
            print 'Start Failed:'
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

        self.arenaData['parameters'] = { 'Num Sessions':self.paramNumSession.value(),
                                         'Between (s)':self.paramBetween.value(),
                                         'OMRPerSession':self.paramOMRPerSession.value(),
                                         'OMR Duration (s)':self.paramOMRDuration.value(),
                                         'OMR Interval (s)':self.paramOMRInterval.value(),
                                         'OMR Period (mm)': self.paramOMRPeriod.value(),
                                         'OMR Duty Cycle': self.paramOMRDutyCycle.value(),
                                         'OMR Velocity':self.paramOMRVelocity.value(),
                                         'NeutralColor':str(self.paramColorNeutral.currentText()),
                                         'OMRColor':str(self.paramColorOMR.currentText()),
                                         'states':self.states.keys(),
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
