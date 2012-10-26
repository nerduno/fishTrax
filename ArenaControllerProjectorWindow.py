"""
AA 2012.10.15
Summary:
The window that will be displayed on projector.
"""

import sys
import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui

class ArenaControllerProjectorWindow(QtGui.QWidget):
    projectorXres = 848
    projectorYres = 400

    def __init__(self, mainwindow):
        super(ArenaControllerProjectorWindow, self).__init__()
        self.mainwindow = mainwindow
        self.res = (self.projectorXres,self.projectorYres)
        self.setGeometry(100,100,self.res[0],self.res[1])
        self.show()

    def updateProjectorDisplay(self):
        self.update()

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        try:		
            self.mainwindow.drawProjectorDisplay(painter)
        except:
            print 'ArenaControllerProjectorWindow:paintEvent failed'
            print "Unexpected error:", sys.exc_info()[0]
        finally:
            painter.end()
