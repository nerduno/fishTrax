# Avoidance Learning Free Manager

"""
AA 2012.07.24
Summary:
Class to manage avoidance stimuli displayed on projector
"""

import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

class AvoidanceStimuli(QtGui.QWidget):
    cBLANK = 0
    cCheckerboard = 1
    cLines = 2
    cWHITE = 3
    cGRAY = 4
    cBLACK = 5
    cRED = 6
    cBLUE = 7
    projectorXres = 848
    projectorYres = 400

    def __init__(self):
        super(AvoidanceStimuli, self).__init__()
        self.res = (self.projectorXres,self.projectorYres)
        self.side1 = self.cWHITE
        self.side2 = self.cWHITE
        self.divideLineTop = self.projectorXres/2
        self.divideLineBottom = self.projectorXres/2
        self.bFlip = False
        self.setGeometry(100,100,self.res[0],self.res[1])
        self.show()

    def incDivideLineTop(self):
        self.divideLineTop+=1
        self.update()

    def incDivideLineBottom(self):
        self.divideLineBottom+=1
        self.update()

    def decDivideLineTop(self):
        self.divideLineTop-=1
        self.update()

    def decDivideLineBottom(self):
        self.divideLineBottom-=1
        self.update()

    def updateTankDisplay(self, side1stimulus, side2stimulus):
        self.side1 = side1stimulus
        self.side2 = side2stimulus
        self.update()

    def paintEvent(self, e):
        sp1 = 0
        sp2 = self.res[0]-1
        if self.bFlip:
            sp1 = self.res[0]-1
            sp2 = 0

        painter = QtGui.QPainter()
        painter.begin(self)
        try:		
            #Draw side one
            if self.side1 == self.cRED:
                brush = QtGui.QBrush(QtCore.Qt.red) #vb change
            elif self.side1 == self.cWHITE:
                brush = QtGui.QBrush(QtCore.Qt.white) #vb change
            elif self.side1 == self.cBLUE:
                brush = QtGui.QBrush(QtCore.Qt.blue) #vb change
            elif self.side1 == self.cGRAY:
                brush = QtGui.QBrush(QtCore.Qt.gray) 
            elif self.side1 == self.cCheckerboard:
                checkerboardimg = QtGui.QPixmap('/home/vburns/fish images/checkerboard.png')
                scaledchecker = QtGui.QPixmap(checkerboardimg.scaledToHeight(500,QtCore.Qt.FastTransformation))
                brush = QtGui.QBrush(scaledchecker)
            elif self.side1 == self.cLines:
                lineimg = QtGui.QPixmap('/home/vburns/fish images/lines.png')
                scaledline = QtGui.QPixmap(lineimg.scaledToHeight(500,QtCore.Qt.FastTransformation))
                brush = QtGui.QBrush(scaledline)
            painter.setBrush(brush)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(sp1,0))
            poly.append(QtCore.QPointF(self.divideLineTop,0))
            poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]-1))
            poly.append(QtCore.QPointF(sp1,self.res[1]-1))
            painter.drawPolygon(poly)

            #Draw side two
            if self.side2 == self.cRED:
                brush = QtGui.QBrush(QtCore.Qt.red) #vb change
            elif self.side2 == self.cWHITE:
                brush = QtGui.QBrush(QtCore.Qt.white) #vb change
            elif self.side2 == self.cBLUE:
                brush = QtGui.QBrush(QtCore.Qt.blue) #vb change
            elif self.side2 == self.cGRAY:
                brush = QtGui.QBrush(QtCore.Qt.gray) 
            elif self.side2 == self.cCheckerboard:
                checkerboardimg = QtGui.QPixmap('/home/vburns/fish images/checkerboard.png')
                scaledchecker = QtGui.QPixmap(checkerboardimg.scaledToHeight(500,QtCore.Qt.FastTransformation))
                brush = QtGui.QBrush(scaledchecker)
            elif self.side2 == self.cLines:
                lineimg = QtGui.QPixmap('/home/vburns/fish images/lines.png')
                scaledline = QtGui.QPixmap(lineimg.scaledToHeight(500,QtCore.Qt.FastTransformation))
                brush = QtGui.QBrush(scaledline)
            painter.setBrush(brush)
            poly = QtGui.QPolygonF()
            poly.append(QtCore.QPointF(sp2,0))
            poly.append(QtCore.QPointF(self.divideLineTop,0))
            poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]-1))
            poly.append(QtCore.QPointF(sp2,self.res[1]-1))
            painter.drawPolygon(poly)	

        finally:
            painter.end()


# 		
# 		#draw side 1

# 		painter.setBrush(brush)
# 		poly = QtGui.QPolygonF()
# 		poly.append(QtCore.QPointF(sp1,0))
# 		poly.append(QtCore.QPointF(self.divideLineTop,0))
# 		poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]))
# 		poly.append(QtCore.QPointF(sp1,self.res[1]))
# 		painter.drawPolygon(poly)
# 		
# 		#draw side 2
# 		if self.side2 == self.cRED:
# 			brush = QtGui.QBrush(QtCore.Qt.red)
# 		elif self.side2 == self.cWHITE:
# 			brush = QtGui.QBrush(QtCore.Qt.white)
# 		painter.setBrush(brush)
# 		poly = QtGui.QPolygonF()
# 		poly.append(QtCore.QPointF(sp2,0))
# 		poly.append(QtCore.QPointF(self.divideLineTop,0))
# 		poly.append(QtCore.QPointF(self.divideLineBottom,self.res[1]))
# 		poly.append(QtCore.QPointF(sp2,self.res[1]))
# 		painter.drawPolygon(poly)
