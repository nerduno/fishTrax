from PyQt4 import QtCore, QtGui
import controllers.AvoidanceController as AvoidanceController
import controllers.CocaineController as CocaineController
import controllers.ClassicalConditioningController as ClassicalConditioningController
import controllers.ContextualHelplessnessController as ContextualHelplessnessController
import controllers.RealTimeShockController as RealTimeShockController

class ArenaManagementPanel(QtGui.QWidget):
    """
    A settings panel that allows for adding removing and configuring ArenaControllers.
    """

    def __init__(self, parent, arenaMain):        
        QtGui.QWidget.__init__(self,parent)

        self.arenaMain = arenaMain
        self.arenas = []
        self.arenaCounter = 0

        self.manageGroup = QtGui.QGroupBox(self)
        self.manageGroup.setTitle('Manage Arenas')
        self.manageVBox = QtGui.QVBoxLayout()
        self.arenaType = QtGui.QComboBox()
        self.arenaType.addItem('Cocaine')
        self.arenaType.addItem('Avoidance')
        self.arenaType.addItem('Classical')
        self.arenaType.addItem('ContextualLH')
        self.arenaType.addItem('RealTimeShock')
        self.arenaType.addItem('Operant')
        self.arenaType.addItem('Temperature')
        self.arenaType.setCurrentIndex(0)
        self.manageVBox.addWidget(self.arenaType)
        self.buttonHBox = QtGui.QHBoxLayout()
        self.addButton = QtGui.QPushButton('Add Arena')
        self.buttonHBox.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton('Remove Current Arena')
        self.buttonHBox.addWidget(self.removeButton)
        self.buttonWidget = QtGui.QWidget()
        self.buttonWidget.setLayout(self.buttonHBox)
        self.manageVBox.addWidget(self.buttonWidget)
        self.label1 = QtGui.QLabel('Selected Arena:')
        self.manageVBox.addWidget(self.label1)
        self.selArena = QtGui.QComboBox()
        self.selArena.setEditable(False)
        self.manageVBox.addWidget(self.selArena)
        self.manageVBox.addStretch(1)
        self.manageGroup.setLayout(self.manageVBox)

        self.connect(self.addButton,
                     QtCore.SIGNAL('clicked(bool)'),
                     self.addArena)
        self.connect(self.removeButton,
                     QtCore.SIGNAL('clicked(bool)'),
                     self.removeCurrentArena)
        self.connect(self.selArena,
                     QtCore.SIGNAL('activated(int)'),
                     self.arenaSelected)

        self.arenaSettingsGroup = QtGui.QGroupBox(self)
        self.arenaSettingsGroup.setTitle('Selected Arena Settings')
        self.arenaSettingsVBox = QtGui.QVBoxLayout()
        self.arenaStack = QtGui.QStackedWidget()
        self.arenaSettingsVBox.addWidget(self.arenaStack)
        self.arenaSettingsGroup.setLayout(self.arenaSettingsVBox)
        
        self.connect(self.arenaStack, 
                     QtCore.SIGNAL('currentChanged(int)'),
                     self.arenaChanged)
        
        self.settingsLayout = QtGui.QGridLayout(self)
        self.settingsLayout.addWidget(self.manageGroup,1,0)
        self.settingsLayout.addWidget(self.arenaSettingsGroup,2,0)
        self.settingsLayout.setRowStretch(3,1)
        self.setLayout(self.settingsLayout)

    def arenaSelected(self, arenaNdx):
        if arenaNdx > -1:
            self.arenaStack.setCurrentIndex(arenaNdx)
            #caused currentChanged signal which invoke arenaChanged

    def arenaChanged(self, arenaNdx):
        for nArena in range(len(self.arenas)):
            self.arenas[nArena].setCurrent(False)
        if arenaNdx > -1:
            self.arenas[arenaNdx].setCurrent(True)

    def addArena(self,bEvent):
        if str(self.arenaType.currentText()) == 'Avoidance':
            a = AvoidanceController.AvoidanceController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'Cocaine':
            a = CocaineController.CocaineController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'Classical':
            a = ClassicalConditioningController.ClassicalConditioningController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'ContextualLH':
            a = ContextualHelplessnessController.ContextualHelplessnessController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'RealTimeShock':
            a = RealTimeShockController.RealTimeShockController(self, self.arenaMain)
        else:
            return
        self.arenaCounter+=1
        self.arenas.append(a)
        self.selArena.addItem('Arena %d'%self.arenaCounter)
        self.arenaStack.addWidget(a)

    def removeCurrentArena(self,bEvent):
        a = self.arenaStack.currentWidget()
        if a:
            ndx = self.arenaStack.indexOf(a)
            del self.arenas[ndx]
            self.arenaStack.removeWidget(a)
            self.selArena.removeItem(ndx)
    
    def getCurrentArena(self):
        return self.arenaStack.currentWidget()

    def getCurrentArenaView(self):
        a = self.arenaStack.currentWidget()
        if a:
            return a.getArenaView()
        else:
            return None

    def onNewFrame(self, frame, time):
        for a in self.arenas:
            a.onNewFrame(frame, time)

    def updateState(self):
        for a in self.arenas:
            a.updateState()

    def drawDisplayOverlays(self, painter):
        for a in self.arenas:
            a.drawDisplayOverlay(painter)

    def areArenasReadyToStart(self):
        return [a.isReadyToStart() for a in self.arenas]

    def drawProjectorDisplay(self, painter):
        for a in self.arenas:
            a.drawProjectorDisplay(painter)

    def startArenas(self):
        print 'starting'
        for a in self.arenas:
            if a.isReadyToStart():
                a.start()
                print 'a'

    def stopArenas(self):
        for a in self.arenas:
            a.stop()

    
