# ArenaControllerMainWindow.py
"""
AA 2012.10.05
Summary:
Window that manages relationship with Camera, LabJack/Arduino, and Projector.
It provides this information individual Arena Controllers (for example an
Avoidance learning controller).

Summary:
1. Establishes a serial port connection with the Arduino sketch 'AvoidanceLearningFree' to control shocks.
2. Establishes connection with AVT camera via OpenCV highgui (a slow but easy method)
3. Displays GUI for running avoidance learning using PyQt4
4. Creates second window to be placed on projector for fish visual stimulus.
"""

#IMPORTANT NOTE cvImg are pointers and can be modifed even if passed to a function.
#IMPORTANT NOTE cv.QueryImage returns a pointer to the same memory on every call (thus clone)
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
#import LabJackPython, u6
import logging
import datetime
import json
import cv
import numpy as np

from PyQt4 import QtGui
from PyQt4 import QtCore
import ipdb
import SerialArduinoController as aac
from AvoidanceCameraManagement import CameraDevice
from ArenaControllerProjectorWindow import ArenaControllerProjectorWindow 
from OpenCVQImage import OpenCVQImage
        
class FishTrackingDisplay(QtGui.QLabel):
    clicked = QtCore.pyqtSignal(int, int)
    
    def __init__(self, parent=None):
        super(FishTrackingDisplay, self).__init__(parent)
        print 't'	
	
    def mousePressEvent(self, ev):
        self.clicked.emit(ev.x(), ev.y())

class SettingsPanel(QtGui.QDockWidget):
    """
    A basic settings panel widget
    """
    def __init__(self, name='', message='', widget=None, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setObjectName(name)
        self.setWindowTitle(name)
        # the default label
        self.label = QtGui.QLabel(message)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # the stack holding the label and setting page
        self.stack = QtGui.QStackedWidget()
        self.stack.addWidget(self.label)
        # the scroller holding the stack
        self.scroller = QtGui.QScrollArea()
        self.scroller.setWidget(self.stack)
        self.scroller.setWidgetResizable(True)
        # add the scoller
        self.setWidget(self.scroller)

        if widget:
            self.placeWidget(widget)

    def placeWidget(self, widget):
        "Place a widget into this setting panel and make it active"
        index = self.stack.addWidget(widget)
        self.stack.setCurrentIndex(index)

    def removeWidget(self, widget=None):
        "Remove a widget from the setting panel"
        if not widget: widget = self.stack.currentWidget()
        if widget == self.label: return
        self.stack.removeWidget(widget)

    def widget(self):
        return self.stack.currentWidget()

class SettingsPanelManager:
    """
    A manager for all the settings panels
    """
    def __init__(self, parent):
        self._parent = parent
        self._settings = []

    def add(self, panel):
        "Add a settings panel, initially all on the right in a tab"
        if panel not in self._settings:
            if self._settings:
                self._parent.tabifyDockWidget(self._settings[-1],panel)
            else:
                self._parent.addDockWidget(QtCore.Qt.LeftDockWidgetArea,
                                           panel)
            self._settings.append(panel)
        else:
            raise Error('Attempting to add the same panel twice')

    def remove(self, panel):
        if panel in self._settings:
            self._parent.removeDockWidget(panel)
            self._settings.remove(panel)
        else:
            raise Error('Attempting to remove a panel that was not added')

    def __getitem__(self, key):
        for panel in self._settings:
            if panel.windowTitle() == key:
                return panel
        return None

    def toggleViewActions(self):
        "Get a list of view actions for all the settings panels"
        actions = [x.toggleViewAction() for x in self._settings]
        for x,y in zip(actions, self._settings):
            x.setText(y.windowTitle())
        return actions

class ArenaControllerMainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(ArenaControllerMainWindow, self).__init__()

        #devices
        self.cam = None
        self.ard = None
        #self.labjack = u6.U6()
        #do I need to do anything to configure a couple registers?

        #parameters and state
        self.bDispRawImage = True
        self.currCvFrame = None
        self.currDispFrame = None
        self.initUI()
        self.projWin = ArenaControllerProjectorWindow(self)
        self.updateTimer = self.startTimer(1)

    def initUI(self):
        self.setWindowIcon(QtGui.QIcon())
        self.setWindowTitle('Arena Controller')

        #Create important actions
        exitAction = QtGui.QAction('Exit',self)
        exitAction.triggered.connect(self.close)

        camAction = QtGui.QAction('Camera',self)
        camAction.triggered.connect(self.connectToCameraDialog)

        ardAction = QtGui.QAction('Arduino',self)
        ardAction.triggered.connect(self.connectToArduinoDialog)

        self.playAction = QtGui.QAction('Play/Pause',self)
        self.playAction.setCheckable(True)
        self.playAction.setChecked(True)
        self.playAction.triggered.connect(self.playpause)

        self.nextViewAction = QtGui.QAction('DispMode:Raw',self)
        self.nextViewAction.triggered.connect(self.nextDispMode)

        self.startExpAction = QtGui.QAction('Start',self)
        self.startExpAction.setCheckable(True)
        self.startExpAction.setChecked(False)
        self.startExpAction.triggered.connect(self.startExperiment)

        #Create the menu bar
        menubar = self.menuBar()
        fileMenu= menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(camAction)

        #Create a toolbar
        self.toolbar = self.addToolBar('Main')
        self.toolbar.addAction(camAction)
        self.toolbar.addAction(ardAction)
        self.toolbar.addSeparator()
        #note that widgets can also be added to the toolbar (like a text box)
        self.toolbar.addAction(self.playAction)
        self.toolbar.addAction(self.nextViewAction)
        self.toolbar.addAction(self.startExpAction)
        self.toolbar.setAllowedAreas(QtCore.Qt.BottomToolBarArea and QtCore.Qt.TopToolBarArea)

 
        #Initialize the settings panel (borrowed Broxton's code)
        self.settingsManager = SettingsPanelManager(self)

        #add arena management panel
        from ArenaManagementPanel import ArenaManagementPanel
        self.arenaPanel = ArenaManagementPanel(self,self)
        self.settingsManager.add(SettingsPanel(name = "Arenas", message = "",
                                               widget = self.arenaPanel))
        #self.connect(self.arenaPanel,
        #             QtCore.SIGNAL('postprocessChanged()'),
        #             self.imageDispWidget.updateDisplay)
        #             self.displaySettings.updateFromParent)
                
        #create the central panel
        self.ftDisp = FishTrackingDisplay() #this label will be used to display video
        self.ftDisp.setAlignment(QtCore.Qt.AlignLeft)  
        self.setCentralWidget(self.ftDisp)

        self.setGeometry(0, 0, 1700, 900)

        #Init to the status bar
        self.statusBar().showMessage('No camera connected. Click on camera connect.')
        self.show()

    def closeEvent(self, event):
        if self.projWin: 
            self.projWin.close()

    def connectToCameraDialog(self):
        cameraId, ok = QtGui.QInputDialog.getInt(self, 'Camera Info', 'Enter a Camera ID (try 0,1,-1, or 2):', value=0)
        if ok:
            self.connectToCamera(cameraId)

    def connectToCamera(self, cameraId):
        self.cam = CameraDevice(cameraId=cameraId, parent=self)
        self.cam.newFrame.connect(self.onNewFrame)
        self.cam.paused = False
        self.statusBar().showMessage('Camera connected.')

    def connectToArduinoDialog(self):
        portName, ok = QtGui.QInputDialog.getText(self, 'Arduino Port', 'Enter the arduino port:',
                                  text=aac.SerialArduinoController.static_getDefaultPortName())
        if ok:
            self.connectToArduino(portName)
    
    def connectToArduino(self, portName):
        portName = str(portName)
        self.statusBar().showMessage('Restart the arduino to complete the connection.')
        if self.ard == None:
            self.ard = aac.SerialArduinoController(portName=portName) 
        else:
            self.ard.connect(portName=portName)

        if self.ard.isConnected():
            self.statusBar().showMessage('Arduino connected.')
        else:
            self.statusBar().showMessage('Arduino failed to connect. Restart arduino and try again.')

    def playpause(self):
        if not self.cam==None:
            self.cam.paused = not self.cam.paused
            if self.cam.paused:
                self.playAction.setText('Play')
            else:
                self.playAction.setText('Pause')

    def nextDispMode(self):
        self.bDispRawImage = not self.bDispRawImage
        if self.bDispRawImage:
            self.nextViewAction.setText('DispMode:Raw')
        else:
            self.nextViewAction.setText('DispMode:CurrArena')

    def onNewFrame(self, frame):
        self.frameTime = time.time()
        self.currCvFrame = cv.CloneImage(frame)
        self.arenaPanel.onNewFrame(self.currCvFrame, self.frameTime)
        self.updateMainDisplay()

    def updateMainDisplay(self):
        #start with either the raw image or the current arena image
        if self.bDispRawImage:
            dispImg = OpenCVQImage(self.currCvFrame)
        else:
            cvImg = self.arenaPanel.getCurrentArenaView()
            if cvImg:
                dispImg = OpenCVQImage(cvImg)
            else:
                dispImg = OpenCVQImage(self.currCvFrame)
        #let each arena draw overlays
        painter = QtGui.QPainter()
        painter.begin(dispImg)
        self.arenaPanel.drawDisplayOverlays(painter)
        painter.end()
        #draw the overlaid image
        pixmap = QtGui.QPixmap.fromImage(dispImg)
        self.ftDisp.setPixmap(pixmap)

    def updateProjectorDisplay(self):
        self.projWin.updateProjectorDisplay()

    def drawProjectorDisplay(self, painter):
        self.arenaPanel.drawProjectorDisplay(painter)

    def startExperiment(self):
        if self.startExpAction.isChecked():
            self.startExpAction.setText('Stop')
            self.arenaPanel.startArenas()
        else:
            self.startExpAction.setText('Start ')
            self.arenaPanel.stopArenas()

    def timerEvent(self, event):
        self.arenaPanel.updateState()

def main(ardPortName=None, cameraId=None): 
    app = QtGui.QApplication(sys.argv)
    ex = ArenaControllerMainWindow()
    if ardPortName is not None:
        ex.connectToArduino(ardPortName)
    if cameraId is not None:
        ex.connectToCamera(cameraId)
    sys.exit(app.exec_())

#if __name__ == '__main__':
#    main()
