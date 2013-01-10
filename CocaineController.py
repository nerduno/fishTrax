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
    OFF = 0
    RUNNING = 1

class CocaineController(ArenaController.ArenaController):
    def __init__(self, parent, arenaMain):        
        super(CocaineController, self).__init__(parent, arenaMain)

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
        self.currRun = -1 #a run is started each time Start Switches is pressed
        self.currSwitch = 0
        self.lastSwitchTime = 0
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

        #experimental parameters groupbox
        self.paramGroup = QtGui.QGroupBox()
        self.paramGroup.setTitle('Exprimental Parameters')
        self.paramLayout = QtGui.QGridLayout()
        self.paramLayout.setHorizontalSpacing(2)
        self.paramLayout.setVerticalSpacing(2)

        self.paramNumSwitches = LabeledSpinBox(None,'NumSwitches',0,100,1,60)
        self.paramLayout.addWidget(self.paramNumSwitches,1,0,1,2)
        self.paramSwitchTime = LabeledSpinBox(None,'SwitchTime (s)',1,3600,300,60)
        self.paramLayout.addWidget(self.paramSwitchTime,1,2,1,2)

        self.paramCond = QtGui.QComboBox()
        self.paramCond.addItem('Pre Train')
        self.paramCond.addItem('Cocaine')
        self.paramCond.addItem('Neutral')
        self.paramCond.addItem('Post Train')
        self.paramCond.setCurrentIndex(0)
        self.labelCond = QtGui.QLabel('Condition')
        self.paramLayout.addWidget(self.paramCond,2,0)
        self.paramLayout.addWidget(self.labelCond,2,1)

        self.paramColor1 = QtGui.QComboBox()
        self.paramColor1.addItem('White')
        self.paramColor1.addItem('Red')
        self.paramColor1.addItem('Blue')
        self.paramColor1.addItem('Gray')
        self.paramColor1.setCurrentIndex(1)
        self.labelColor1 = QtGui.QLabel('Color1')
        self.paramLayout.addWidget(self.paramColor1,2,2)
        self.paramLayout.addWidget(self.labelColor1,2,3)

        self.paramColor2 = QtGui.QComboBox()
        self.paramColor2.addItem('White')
        self.paramColor2.addItem('Red')
        self.paramColor2.addItem('Blue')
        self.paramColor2.addItem('Gray')
        self.paramColor2.setCurrentIndex(2)
        self.labelColor2 = QtGui.QLabel('Color2')
        self.paramLayout.addWidget(self.paramColor2,3,0)
        self.paramLayout.addWidget(self.labelColor2,3,1)

        self.paramOffColor = QtGui.QComboBox()
        self.paramOffColor.addItem('White')
        self.paramOffColor.addItem('Red')
        self.paramOffColor.addItem('Blue')
        self.paramOffColor.addItem('Gray')
        self.paramOffColor.setCurrentIndex(0)
        self.labelOffColor = QtGui.QLabel('OffColor')
        self.paramLayout.addWidget(self.paramOffColor,3,2)
        self.paramLayout.addWidget(self.labelOffColor,3,3)
        
        self.paramDrugColor = QtGui.QComboBox()
        self.paramDrugColor.addItem('White')
        self.paramDrugColor.addItem('Red')
        self.paramDrugColor.addItem('Blue')
        self.paramDrugColor.addItem('Gray')
        self.paramDrugColor.setCurrentIndex(0)
        self.labelDrugColor = QtGui.QLabel('DrugColor')
        self.paramLayout.addWidget(self.paramDrugColor,4,0)
        self.paramLayout.addWidget(self.labelDrugColor,4,1)
        
        self.paramConc = QtGui.QDoubleSpinBox()
        self.paramConc.setRange(0.0,1000.0)
        self.paramConc.setValue(10.0)
        self.labelConc = QtGui.QLabel('Conc mg/L')
        self.paramLayout.addWidget(self.paramConc,5,0)
        self.paramLayout.addWidget(self.labelConc,5,1)

        self.paramNumFish = LabeledSpinBox(None,'NumFish',1,10,1,60)
        self.paramLayout.addWidget(self.paramNumFish,5,2,1,2)

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
        self.settingsLayout.addWidget(self.startButton,2,0)
        self.settingsLayout.addWidget(self.paramGroup,3,0)
        self.settingsLayout.addWidget(self.infoGroup,4,0)
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
                self.arenaData['runs'][self.currRun]['video'].append((self.frameTime, None)) 
#                if self.paramNumFish.value() == 1:
#                    self.arenaData['runs'][self.currRun]['tracking'].append((self.frameTime, self.fishPos[0], self.fishPos[1]))
#                else:
                d = [self.frameTime, pos[0], pos[1]]
                for nFish in range(1, min(self.paramNumFish.value(),len(allFish))):
                    d.append(allFish[nFish][0])
                    d.append(allFish[nFish][1])
#                print d
                self.arenaData['runs'][self.currRun]['tracking'].append(tuple(d))

            self.arenaView = view
        except:
            print 'CocaineController:onNewFrame failed'
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
                    self.arenaMain.statusBar().showMessage('SwitchesCompleted: %d TimeSinceSwitch: %f' % (self.currSwitch, t - self.lastSwitchTime))

                #handle State Changes
                if t >= self.lastSwitchTime + self.paramSwitchTime.value():
                    self.currSwitch += 1
                    self.lastSwitchTime = t
                    if self.currSwitch > self.paramNumSwitches.value():
                        self.currState = State.OFF
                        self.arenaData['runs'][self.currRun]['endTime'] = t
                        self.startButton.setText('Start Switches')
                        self.startButton.setChecked(False)
                        self.paramGroup.setDisabled(False)
                        self.infoGroup.setDisabled(False)
                    self.updateProjectorDisplay()
                    self.arenaData['runs'][self.currRun]['switchTimes'].append(t)
                    self.saveResults()
            except:
                print 'CocaineController:updateState failed'
                traceback.print_exc()
                QtCore.pyqtRemoveInputHook() 
                ipdb.set_trace()
            finally:
                self.mutex.release()

    def isReadyToStart(self):
        return os.path.exists(self.infoDir.text()) and self.trackWidget.getBackgroundImage() and self.fishImg and self.arenaCamCorners

    def drawProjectorDisplay(self, painter):
        if self.currState == State.OFF and self.projCalibButton.isChecked():
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
            if self.currState == State.OFF:
                #Draw whole tank
                pen = QtGui.QPen(QtCore.Qt.NoPen)
                brush = self.getBrush(self.paramOffColor.currentIndex())
                painter.setBrush(brush)
                painter.setPen(pen)
                poly = QtGui.QPolygonF()
                poly.append(QtCore.QPointF(self.proj1X.value(), self.proj1Y.value()))
                poly.append(QtCore.QPointF(self.proj2X.value(), self.proj2Y.value()))
                poly.append(QtCore.QPointF(self.proj3X.value(), self.proj3Y.value()))
                poly.append(QtCore.QPointF(self.proj4X.value(), self.proj4Y.value()))
                painter.drawPolygon(poly)
            else:
                side1Color = self.paramColor1.currentIndex()
                side2Color = self.paramColor2.currentIndex()
                if self.currSwitch%2 == 1:
                    side1Color = self.paramColor2.currentIndex()
                    side2Color = self.paramColor1.currentIndex()
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
        if self.currState == State.OFF:
            if self.isReadyToStart():
                self.paramGroup.setDisabled(True)
                self.infoGroup.setDisabled(True)
                if self.arenaData == None or not str(self.infoDir.text()) == self.saveLocation:
                    td = datetime.datetime.now()
                    self.saveLocation = str(self.infoDir.text())
                    [p, self.fnResults] = os.path.split(self.saveLocation)
                    self.fnResults = self.fnResults + '_' + td.strftime('%Y-%m-%d-%H-%M-%S')
                    self.jsonFileName = str(self.infoDir.text()) + os.sep + self.fnResults  + '.json'
                    self.arenaData = {}
                    self.arenaData['runs'] = list()
                self.initNewRunData()

                t = time.time()
                self.currState = State.RUNNING
                self.lastSwitchTime = t
                self.arenaData['runs'][self.currRun]['startTime'] = t
                self.currSwitch = 0
                self.startButton.setText('Stop')
            else:
                self.arenaMain.statusBar().showMessage('Arena not ready to start.  Information is missing.')
        else: 
            self.mutex.acquire()
            try:
                t = time.time()
                self.currState = State.OFF
                self.arenaData['runs'][self.currRun]['endTime'] = t
                self.arenaData['runs'][self.currRun]['switchTimes'].append(t)
                self.saveResults()
                self.startButton.setText('Start Switches')
                self.paramGroup.setDisabled(False)
                self.infoGroup.setDisabled(False)
            except:
                print 'stop switches failed'
                print "Unexpected error:", sys.exc_info()[0]
            finally:
                self.mutex.release()            
        self.updateProjectorDisplay()
        
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

    def initNewRunData(self):
        #prepare output data structure
        self.arenaData['runs'].append({})
        cr = self.currRun = len(self.arenaData['runs']) - 1
        self.arenaData['runs'][cr]['fishbirthday'] = str(self.infoDOB.date().toPyDate())
        self.arenaData['runs'][cr]['fishage'] =  (datetime.date.today() - self.infoDOB.date().toPyDate()).days
        self.arenaData['runs'][cr]['fishstrain'] = str(self.infoType.text())
        self.arenaData['runs'][cr]['fishsize'] = self.fishSize
        self.arenaData['runs'][cr]['parameters'] = { 'numSwitches':self.paramNumSwitches.value(),
                                                     'SwitchDuration':self.paramSwitchTime.value(),
                                                     'Cond':str(self.paramCond.currentText()),
                                                     'Conc':str(self.paramConc.value()),
                                                     'Color1':str(self.paramColor1.currentText()),
                                                     'Color2':str(self.paramColor2.currentText()),
                                                     'OffColor':str(self.paramOffColor.currentText()),
                                                     'DrugColor':str(self.paramDrugColor.currentText()),
                                                     'CodeVersion':None }
        self.arenaData['runs'][cr]['trackingParameters'] = self.trackWidget.getParameterDictionary()
        self.arenaData['runs'][cr]['trackingParameters']['arenaPoly'] = self.arenaCamCorners 
        self.arenaData['runs'][cr]['trackingParameters']['arenaDivideLine'] = self.arenaMidLine
        self.arenaData['runs'][cr]['trackingParameters']['arenaSide1Sign'] = self.arenaSide1Sign
        self.arenaData['runs'][cr]['tracking'] = list() #list of tuples (frametime, posx, posy)
        self.arenaData['runs'][cr]['video'] = list() #list of tuples (frametime, filename)	
        self.arenaData['runs'][cr]['switchTimes'] = list() #list of times at switch stimulus flipped.
        self.arenaData['runs'][cr]['startTime'] = None
        self.arenaData['runs'][cr]['endTime'] = None

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




        
                               

                        




