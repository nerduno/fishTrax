from PyQt4 import QtCore, QtGui

class ArenaController(QtGui.QWidget):
    def __init__(self, parent, arenaMain):        
        QtGui.QWidget.__init__(self,parent)
        self.arenaMain = arenaMain         
        self.bIsCurrentArena = False
        self.arenaView = None
        
        #self.settingsLayout = QtGui.QGridLayout(self)
        #lab = QtGui.QLabel('No Settings')
        #self.settingsLayout.addWidget(lab,0,0)
        #self.setLayout(self.settingsLayout)
    
    def setCurrent(self, bIsCurrent):
        self.bIsCurrentArena = bIsCurrent

    def isCurrent(self):
        return self.bIsCurrentArena

    def getArenaView(self):
        return self.arenaView

    def onNewFrame(self, frame, time):
        self.arenaView = frame

    def updateState(self):
        pass

    def isReadyToStart(self):
        return True

    def drawProjectorDisplay(self, painter):
        pass

    def updateProjectorDisplay(self):
        self.arenaMain.updateProjectorDisplay()
    
    def drawDisplayOverlay(self, painter):
        pass

    def start(self):
        pass

    def stop(self):
        pass
