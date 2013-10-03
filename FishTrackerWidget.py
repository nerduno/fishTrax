import cv
import numpy as np
from PyQt4 import QtCore
from PyQt4 import QtGui
from utility_widgets import LabeledSpinBox
from utility_widgets import LabeledDoubleSpinBox

dilateKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)
erodeKernal = cv.CreateStructuringElementEx(3, 3, 1, 1, cv.CV_SHAPE_CROSS)

class FishTrackerWidget(QtGui.QGroupBox):

    def __init__(self, parent, ftDisp):
        #ftDisp is necessary so the FishTrackerWidget can collect mouse clicks
        
        super(FishTrackerWidget, self).__init__(parent)

        self.ftDisp = ftDisp

        self.currCvFrame = None
        self.arenaCvMask = None #track mask
        self.bcvImg = None #background image for subtraction
        self.currG = None
        self.maskG = None
        self.backG = None
        self.backG32 = None
        self.diffG = None
        self.thrsG = None
        self.thrsMG = None
        self.tracEG = None
        self.tracDG = None
        self.fmask = None
        self.bFixBackgroundNow = False

        self.setTitle('Tracking Parameters')
        self.trackLayout = QtGui.QGridLayout(self)
        self.trackLayout.setHorizontalSpacing(3)
        self.trackLayout.setVerticalSpacing(3)

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
        self.trackLayout.addWidget(self.viewLabel, 0,0,1,2)
        self.trackLayout.addWidget(self.selView, 0,2,1,2)

        self.bgButton = QtGui.QPushButton('Get Background')
        self.bgButton.clicked.connect(self.setBackgroundImage)
        self.trackLayout.addWidget(self.bgButton, 1,0,1,2)

        self.fixButton = QtGui.QPushButton('Fix Background')
        self.fixButton.clicked.connect(self.fixBackground)
        self.trackLayout.addWidget(self.fixButton, 1,2,1,2)

        self.trackThreshold = LabeledSpinBox(None,'Threshold',0,255,3,60)
        self.trackErode = LabeledSpinBox(None,'Erode',0,20,0,60)
        self.trackDilate = LabeledSpinBox(None,'Dilate',0,20,0,60)
        self.trackMinArea = LabeledSpinBox(None,'MinArea',0,600000,0,75)
        self.trackMaxArea = LabeledSpinBox(None,'MaxArea',0,600000,600000,75)
        self.updateCheckbox = QtGui.QCheckBox('Use Updating BG')
        self.numFish = LabeledSpinBox(None,'NumFish',0,20,1,60)
        self.fishSize = LabeledSpinBox(None,'FG Size',0,1000,30,60)
        self.learningRate = LabeledDoubleSpinBox(None,'Learning rate',0,1,0.1,60)

        self.trackLayout.addWidget(self.trackThreshold,2,0,1,2)
        self.trackLayout.addWidget(self.trackErode, 2,2,1,2)
        self.trackLayout.addWidget(self.trackDilate, 3,0,1,2)        
        self.trackLayout.addWidget(self.trackMinArea, 3,2,1,2)
        self.trackLayout.addWidget(self.trackMaxArea, 4,0,1,2) 
        self.trackLayout.addWidget(self.updateCheckbox,5,0,1,2)
        self.trackLayout.addWidget(self.numFish,5,2,1,2)
        self.trackLayout.addWidget(self.fishSize,6,0,1,2)
        self.trackLayout.addWidget(self.learningRate,6,2,1,2)

        self.setLayout(self.trackLayout)

    def setBackgroundImage(self):
        if self.currCvFrame:
            self.bcvImg = cv.CloneImage(self.currCvFrame)
            if not self.maskG:
                self.backG = cv.CreateImage(cv.GetSize(self.currCvFrame), cv.IPL_DEPTH_8U, 1)
                self.backG32 = cv.CreateImage(cv.GetSize(self.currCvFrame), cv.IPL_DEPTH_32F, 1)
                cv.CvtColor(self.bcvImg, self.backG, cv.CV_BGR2GRAY)
                cv.ConvertScale(self.backG, self.backG32)
            else:
                self.backG = cv.CreateImage(cv.GetSize(self.maskG), cv.IPL_DEPTH_8U, 1)
                self.backG32 = cv.CreateImage(cv.GetSize(self.maskG), cv.IPL_DEPTH_32F, 1)
                cv.CvtColor(self.bcvImg[self.maskBoundedR0:self.maskBoundedR0+self.maskBoundedHeight, 
                                        self.maskBoundedC0:self.maskBoundedC0+self.maskBoundedWidth], self.backG, cv.CV_BGR2GRAY)
                cv.ConvertScale(self.backG, self.backG32)

    def getBackgroundImage(self):
        return self.bcvImg

    def fixBackground(self):
        self.ftDisp.clicked.connect(self.handleFixBackgroundClick)
        self.bFixBackgroundNow = False

    def handleFixBackgroundClick(self,x,y):
        self.correctFish = (x - self.maskBoundedC0, y - self.maskBoundedR0)
        self.ftDisp.clicked.disconnect(self.handleFixBackgroundClick)
        self.bFixBackgroundNow = True

    def setTrackMask(self, img):
        #Convert mask to gray scale.
        self.arenaCvMask = img
        self.maskG = cv.CreateImage((self.arenaCvMask.width, self.arenaCvMask.height), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(self.arenaCvMask, self.maskG, cv.CV_BGR2GRAY)
        
        #get bounding rectangle of mask and resize it
        maskArray = np.asarray(self.maskG[:,:])
        self.maskBoundedC0 = np.min(np.nonzero(np.max(maskArray,0))) #X = width = cols
        self.maskBoundedR0 = np.min(np.nonzero(np.max(maskArray,1))) #Y = height = rows
        self.maskBoundedWidth = np.max(np.nonzero(np.max(maskArray,0))) - self.maskBoundedC0 + 1
        self.maskBoundedHeight = np.max(np.nonzero(np.max(maskArray,1))) - self.maskBoundedR0 + 1
        print self.maskBoundedC0, self.maskBoundedR0, self.maskBoundedWidth, self.maskBoundedHeight
        self.maskG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(self.arenaCvMask[self.maskBoundedR0:self.maskBoundedR0+self.maskBoundedHeight, 
                                     self.maskBoundedC0:self.maskBoundedC0+self.maskBoundedWidth], self.maskG, cv.CV_BGR2GRAY)

        #recrop background image
        if self.bcvImg:
            self.backG = cv.CreateImage(cv.GetSize(self.maskG), cv.IPL_DEPTH_8U, 1)
            self.backG32 = cv.CreateImage(cv.GetSize(self.maskG), cv.IPL_DEPTH_32F, 1)
            cv.CvtColor(self.bcvImg[self.maskBoundedR0:self.maskBoundedR0+self.maskBoundedHeight, 
                                    self.maskBoundedC0:self.maskBoundedC0+self.maskBoundedWidth], self.backG, cv.CV_BGR2GRAY)
            cv.ConvertScale(self.backG, self.backG32)

        #resize temp images to bounded rect size
        self.currG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)	
        self.diffG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        self.thrsG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        self.thrsMG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        self.tracEG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        self.tracDG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        self.tracG = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)
        self.fmask = cv.CreateImage((self.maskBoundedWidth, self.maskBoundedHeight), cv.IPL_DEPTH_8U, 1)

    def getParameterDictionary(self):
        pd = {}
        pd['nDiffThreshold'] = self.trackThreshold.value()
        pd['nErode'] = self.trackErode.value()
        pd['nDilate'] = self.trackDilate.value()
        return pd

    def getTrackDisplay(self):
        if self.currCvFrame == None:
            return None

        dispImg = cv.CreateImage(cv.GetSize(self.currCvFrame), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(self.currCvFrame, dispImg, cv.CV_BGR2GRAY)
        if self.maskG:
            cv.SetImageROI(dispImg, (self.maskBoundedC0, self.maskBoundedR0, self.maskBoundedWidth, self.maskBoundedHeight))
      
        dispModeNdx = self.selView.currentIndex()
        if dispModeNdx == 1 and self.backG:
            cv.Copy(self.backG, dispImg)
        elif dispModeNdx == 2 and self.diffG:
            cv.Copy(self.diffG, dispImg)
        elif dispModeNdx == 3 and self.thrsG:
            cv.Copy(self.thrsG, dispImg)
        elif dispModeNdx == 4 and self.thrsMG:
            cv.Copy(self.thrsMG, dispImg)
        elif dispModeNdx == 5 and self.tracEG:
            cv.Copy(self.tracEG, dispImg)
        elif dispModeNdx == 6 and self.tracDG:
            cv.Copy(self.tracDG, dispImg)
        elif dispModeNdx == 7 and self.maskG:
            cv.Copy(self.maskG, dispImg)
        else:
            return self.currCvFrame

        cv.ResetImageROI(dispImg)
        return dispImg

    def findFish(self, cvImg):
        ####NEED TO MODIFY TO USE CV2 
        self.currCvFrame = cvImg
        foundFish = False
        fishPos = (0,0)
        allFish = []
        if not self.bcvImg == None and not self.arenaCvMask == None:
            #Background subtract, threshold, mask, erode and dilate
            cv.CvtColor(self.currCvFrame[self.maskBoundedR0:self.maskBoundedR0+self.maskBoundedHeight, 
                                         self.maskBoundedC0:self.maskBoundedC0+self.maskBoundedWidth], self.currG, cv.CV_BGR2GRAY)
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
                    fishPos = (moments[ndx].m10/moments[ndx].m00 + self.maskBoundedC0, moments[ndx].m01/moments[ndx].m00 + self.maskBoundedR0)
                #get all fish sorted by size.
                sndx = np.argsort(areas)[::-1]
                for bn in sndx:
                    if (moments[bn].m00 > self.trackMinArea.value() and moments[bn].m00 < self.trackMaxArea.value()):
                        allFish.append((moments[bn].m10/moments[bn].m00 + self.maskBoundedC0, moments[bn].m01/moments[bn].m00 + self.maskBoundedR0))
            del seq  

            #update background image:
            if self.bFixBackgroundNow:
                cv.Rectangle(self.fmask,(0,0),cv.GetSize(self.fmask),255,-1)
                cv.Circle(self.fmask, tuple([int(x) for x in self.correctFish]), self.fishSize.value(), 0, -1)
                cv.Copy(self.currG, self.backG, self.fmask)
                cv.ConvertScale(self.backG, self.backG32) 
                self.bFixBackgroundNow = False
            elif self.updateCheckbox.isChecked():
                if foundFish:
                    cv.Rectangle(self.fmask,(0,0),cv.GetSize(self.fmask),255,-1)
                    for nFish in range(min(self.numFish.value(),len(allFish))):
                        pos = (int(allFish[nFish][0] - self.maskBoundedC0), int(allFish[nFish][1] - self.maskBoundedR0))
                        cv.Circle(self.fmask, pos, self.fishSize.value(),0,-1)
                    cv.RunningAvg(self.currG, self.backG32, self.learningRate.value(), self.fmask)
                    cv.ConvertScaleAbs(self.backG32,self.backG)

        return (foundFish, fishPos, self.getTrackDisplay(), allFish)
