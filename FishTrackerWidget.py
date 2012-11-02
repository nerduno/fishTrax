import cv
import numpy as np
from PyQt4 import QtCore
from PyQt4 import QtGui

dilateKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)
erodeKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)

class FishTrackerWidget(QtGui.QGroupBox):

    def __init__(self, parent, getBackgroundImageFunc):        
        super(FishTrackerWidget, self).__init__(parent)
        self.currCvFrame = None
        self.arenaCvMask = None #track mask
        self.bcvImg = None #background image for subtraction
        self.currG = None
        self.maskG = None
        self.backG = None
        self.diffG = None
        self.thrsG = None
        self.thrsMG = None
        self.tracEG = None
        self.tracDG = None

        self.setTitle('Tracking Parameters')
        self.trackLayout = QtGui.QGridLayout(self)
        self.trackLayout.setHorizontalSpacing(3)
        self.trackLayout.setVerticalSpacing(3)
        self.bgButton = QtGui.QPushButton('Get Background')
        self.bgButton.clicked.connect(getBackgroundImageFunc)
        self.viewLabel = QtGui.QLabel('Track Display Mode:')
        self.viewLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.viewLabel.adjustSize()
        self.selView = QtGui.QComboBox(self)
        self.selView.addItem('Raw')
        self.selView.addItem('Background')
        self.selView.addItem('Subtracted')
        self.selView.addItem('Thresholded')
        self.selView.addItem('Masked')
        self.selView.addItem('Eroded')
        self.selView.addItem('Dilated')
        self.selView.addItem('Mask')
        l1 = QtGui.QLabel('Threshold')
        l1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        l1.adjustSize()
        l2 = QtGui.QLabel('Erode')
        l2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        l2.adjustSize()
        l3 = QtGui.QLabel('Dilate')
        l3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        l3.adjustSize()
        l4 = QtGui.QLabel('MinSize')
        l4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        l4.adjustSize()
        l5 = QtGui.QLabel('MaxSize')
        l5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        l5.adjustSize()
        self.trackThreshold = QtGui.QSpinBox()
        self.trackThreshold.setMaximumWidth(50)
        self.trackThreshold.setValue(3)
        self.trackThreshold.setRange(0,255)
        self.trackErode = QtGui.QSpinBox()
        self.trackErode.setMaximumWidth(50)
        self.trackErode.setValue(0)
        self.trackErode.setRange(0,20)
        self.trackDilate = QtGui.QSpinBox()
        self.trackDilate.setMaximumWidth(50)
        self.trackDilate.setValue(0)
        self.trackDilate.setRange(0,20)
        self.trackMinArea = QtGui.QSpinBox()
        self.trackMinArea.setMaximumWidth(75)
        self.trackMinArea.setRange(0,600000)
        self.trackMinArea.setValue(0)
        self.trackMaxArea = QtGui.QSpinBox()
        self.trackMaxArea.setMaximumWidth(75)
        self.trackMaxArea.setRange(0,600000)
        self.trackMaxArea.setValue(600000)
        self.trackLayout.addWidget(self.viewLabel, 0,0,1,2)
        self.trackLayout.addWidget(self.selView, 0,2,1,2)
        self.trackLayout.addWidget(self.bgButton, 1,0,1,2)
        self.trackLayout.addWidget(l1,1,2)
        self.trackLayout.addWidget(self.trackThreshold, 1,3)
        self.trackLayout.addWidget(l2,2,0)
        self.trackLayout.addWidget(self.trackErode, 2,1)
        self.trackLayout.addWidget(l3,2,2)
        self.trackLayout.addWidget(self.trackDilate, 2,3)        
        self.trackLayout.addWidget(l4,3,0)
        self.trackLayout.addWidget(self.trackMinArea, 3,1)
        self.trackLayout.addWidget(l5,3,2)
        self.trackLayout.addWidget(self.trackMaxArea, 3,3) 
        self.setLayout(self.trackLayout)

    def setBackgroundImage(self, img):
        self.bcvImg = img
        self.backG = cv.CreateImage((self.currCvFrame.width, self.currCvFrame.height), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(self.bcvImg, self.backG, cv.CV_BGR2GRAY)

    def setTrackMask(self, img):
        self.arenaCvMask = img
        self.maskG = cv.CreateImage((self.arenaCvMask.width, self.arenaCvMask.height), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(self.arenaCvMask, self.maskG, cv.CV_BGR2GRAY)

    def getParameterDictionary(self):
        pd = {}
        pd['nDiffThreshold'] = self.trackThreshold.value()
        pd['nErode'] = self.trackErode.value()
        pd['nDilate'] = self.trackDilate.value()
        return pd

    def getTrackDisplay(self):
        dispModeNdx = self.selView.currentIndex()
        if dispModeNdx == 1 and self.backG:
            return self.backG
        elif dispModeNdx == 2 and self.diffG:
            return self.diffG
        elif dispModeNdx == 3 and self.thrsG:
            return self.thrsG
        elif dispModeNdx == 4 and self.thrsMG:
            return self.thrsMG
        elif dispModeNdx == 5 and self.tracEG:
            return self.tracEG
        elif dispModeNdx == 6 and self.tracDG:
            return self.tracDG
        elif dispModeNdx == 7 and self.maskG:
            return self.maskG
        else:
            return self.currCvFrame

    def findFish(self, cvImg):
        self.currCvFrame = cvImg
        foundFish = False
        fishPos = (0,0)
        allFish = []
        if not self.bcvImg == None and not self.arenaCvMask == None:
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
            cv.Threshold ( self.diffG , self.thrsG , self.trackThreshold.value() , 255 , cv.CV_THRESH_BINARY ) #threshold
            cv.And( self.thrsG, self.maskG, self.thrsMG ) #mask
            cv.Erode(self.thrsMG, self.tracEG, erodeKernal, self.trackErode.value()) #erode
            cv.Dilate(self.tracEG, self.tracDG, dilateKernal, self.trackDilate.value()) #dilate
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
                if (moments[ndx].m00 > self.trackMinArea.value() and moments[ndx].m00 < self.trackMaxArea.value()):
                    foundFish = True
                    fishPos = (moments[ndx].m10/moments[ndx].m00, moments[ndx].m01/moments[ndx].m00)
                #get all fish sorted by size.
                sndx = np.argsort(areas)[::-1]
                for bn in sndx:
                    if (moments[bn].m00 > self.trackMinArea.value() and moments[bn].m00 < self.trackMaxArea.value()):
                        allFish.append((moments[bn].m10/moments[bn].m00, moments[bn].m01/moments[bn].m00))
            del seq  
        return (foundFish, fishPos, self.getTrackDisplay(), allFish)
