from PyQt4 import QtCore, QtGui
import controllers.AvoidanceController as AvoidanceController
import controllers.CocaineController as CocaineController
import controllers.ClassicalConditioningController as ClassicalConditioningController
import controllers.ContextualHelplessnessController as ContextualHelplessnessController
import controllers.RealTimeShockController as RealTimeShockController
import controllers.YokedAvoidanceController as YokedAvoidanceController


#relay pin side1, relay pin side 2, analonIn pin side 1, analogIn pin side 2
defaultTankChannels = {0:(53,52,15,14), 
                       1:(51,50, 9, 8), 
                       2:(48,49, 7, 6),
                       3:(46,47, 0, 1),
                       4:(43,42,13,12),
                       5:(41,40,10,11),
                       6:(38,39, 4, 5),
                       7:(44,45, 2, 3)}

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
        self.arenaType.addItem('YokedAvoidance')
        self.arenaType.addItem('ContextualLH')
        self.arenaType.addItem('Cocaine')
        self.arenaType.addItem('Avoidance')
        self.arenaType.addItem('Classical')
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
            a = YokedAvoidanceController.YokedAvoidanceController(self, self.arenaMain, False)
            a.configTank(*self.grid2TankConfig(len(self.arenas)%4, len(self.arenas)/4))
        elif str(self.arenaType.currentText()) == 'Cocaine':
            a = CocaineController.CocaineController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'Classical':
            a = ClassicalConditioningController.ClassicalConditioningController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'ContextualLH':
            a = ContextualHelplessnessController.ContextualHelplessnessController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'RealTimeShock':
            a = RealTimeShockController.RealTimeShockController(self, self.arenaMain)
        elif str(self.arenaType.currentText()) == 'YokedAvoidance':
            #create and config two tank
            a = YokedAvoidanceController.YokedAvoidanceController(self, self.arenaMain, False)
            b = YokedAvoidanceController.YokedAvoidanceController(self, self.arenaMain, True)
            a.setPartnerTank(b)
            b.setPartnerTank(a)
            #Todo make config apply to all tank types not just Yoked
            a.configTank(*self.grid2TankConfig(len(self.arenas)%4, len(self.arenas)/4))
            b.configTank(*self.grid2TankConfig((len(self.arenas)+1)%4, (len(self.arenas)+1)/4))
            #add the tanks to management panel
            self.arenaCounter+=1
            self.arenas.append(a)
            self.selArena.addItem('Arena %d'%self.arenaCounter)
            self.arenaStack.addWidget(a)
            self.arenaCounter+=1
            self.arenas.append(b)
            self.selArena.addItem('Arena %d'%self.arenaCounter)
            self.arenaStack.addWidget(b)
            return
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

    #Helper methods for quickly configuring tanks 
    def grid2CamCoords(self, px,py):
        #hard coded for now, but should GUI set x0, y0, plus rotation and scale.
        y0 = 17
        x0 = 106
        xSp = 44
        ySp = 45
        tW = 207
        tH = 431 
        return (( x0+(tW+xSp)*px   , y0+(tH+ySp)*py+tH), #Lower Left
                ( x0+(tW+xSp)*px+tW, y0+(tH+ySp)*py+tH), #Lower Right (y flipped)
                ( x0+(tW+xSp)*px+tW, y0+(tH+ySp)*py   ), #UpperRight
                ( x0+(tW+xSp)*px   , y0+(tH+ySp)*py   )) #UpperLeft

    def grid2Proj(self, px,py):
        x0 = 280
        y0 = 222
        tW = 105
        tH = 213
        rot = 270
        xSp = 19
        ySp = 10
        return (x0+(tW+xSp)*px, y0+(tH+ySp)*py, tW, tH, rot)

    def grid2ArduinoConfig(self, px,py):
        return defaultTankChannels[px+4*py]
    
    def grid2TankConfig(self, px,py):
        return self.grid2ArduinoConfig(px,py), self.grid2CamCoords(px,py), self.grid2Proj(px,py)
                
