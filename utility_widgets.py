import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

class LabeledSpinBox(QtGui.QWidget):
    def __init__(self, parent, label, nMin, nMax, nVal, nWidth):
        super(LabeledSpinBox, self).__init__(parent)
        self.gbox = QtGui.QGridLayout()
        self.gbox.setHorizontalSpacing(1)
        self.gbox.setVerticalSpacing(1)
        self.gbox.setContentsMargins(1,1,1,1)
        self.spin = QtGui.QSpinBox()
        self.spin.setRange(nMin,nMax)
        self.spin.setValue(nVal)
        self.spin.setMaximumWidth(nWidth)
        self.label = QtGui.QLabel(label)
        self.gbox.addWidget(self.spin,0,0)
        self.gbox.addWidget(self.label,0,1)
        self.setLayout(self.gbox)

    def value(self):
        return self.spin.value()

    def setValue(self, val):
        self.spin.setValue(val)

class LabeledDoubleSpinBox(QtGui.QWidget):
    def __init__(self, parent, label, nMin=0.0, nMax=1.0, nVal=0.0, nWidth=60):
        super(LabeledDoubleSpinBox, self).__init__(parent)
        self.gbox = QtGui.QGridLayout()
        self.gbox.setHorizontalSpacing(1)
        self.gbox.setVerticalSpacing(1)
        self.gbox.setContentsMargins(1,1,1,1)
        self.spin = QtGui.QDoubleSpinBox()
        self.spin.setRange(nMin,nMax)
        self.spin.setValue(nVal)
        self.spin.setMaximumWidth(nWidth)
        self.label = QtGui.QLabel(label)
        self.gbox.addWidget(self.spin,0,0)
        self.gbox.addWidget(self.label,0,1)
        self.setLayout(self.gbox)

    def value(self):
        return self.spin.value()

    def setValue(self, val):
        self.spin.setValue(val)


class TextAndBrowseWidget(QtGui.QWidget):
    """
    A widget that has both a text input field and a browse button
    """
    def __init__(self, browseLabel='', browseFunc=None, default='', browseIcon=None, parent=None):
        """
        Instantiate a TextAndBrowseWidget

        label is the name of the field
        browseLabel is the label on the browse button
        browseFunc is the function called when the browse
                   button is pressed and either returns
                   None for no change or returns a new string
                   It takes the string in the text field as input
        default is the default value in the text field
        browseIcon is an optional icon for the button

        This widget emits the following signals:
          textChanged(QString) - when the text changes
          textEdited(QString) - when the text has been edited in the edit box
          textBrowsed(QString) - when the text has been changed by the browser

        This widget accepts the following slots:
          setText(str) - set the text in the input field
        """
        QtGui.QWidget.__init__(self, parent)

        # create the UI
        self.lineEdit = QtGui.QLineEdit(default)
        if browseIcon:
            self.browseButton = QtGui.QPushButton(browseIcon,browseLabel)
        else:
            self.browseButton = QtGui.QPushButton(browseLabel)
        self._browseFunc = browseFunc
        self.groupLayout = QtGui.QHBoxLayout()
        self.groupLayout.addWidget(self.lineEdit)
        self.groupLayout.addWidget(self.browseButton)
        self.groupLayout.setStretchFactor(self.lineEdit,1)
        self.setLayout(self.groupLayout)

        # connect the signals
        self.connect(self.lineEdit,QtCore.SIGNAL('textChanged(QString)'),
                     self._textChanged)
        self.connect(self.lineEdit,QtCore.SIGNAL('textEdited(QString)'),
                     self._textEdited)
        self.connect(self.lineEdit,QtCore.SIGNAL('editingFinished()'),
                     self._editingFinished)
        self.connect(self.browseButton,QtCore.SIGNAL('clicked(bool)'),
                     self._browseClicked)

    def _textChanged(self, s):
        self.emit(QtCore.SIGNAL('textChanged(QString)'), s)

    def _textEdited(self, s):
        self.emit(QtCore.SIGNAL('textEdited(QString)'), s)

    def _editingFinished(self):
        self.emit(QtCore.SIGNAL('editingFinished()'))

    def _textBrowsed(self, s):
        self.lineEdit.setText(s)
        self.emit(QtCore.SIGNAL('editingFinished()'))

    def _browseClicked(self):
        if not self._browseFunc:
            return # no browse function defined
        result = self._browseFunc(self.lineEdit.text())
        if result != None:
            self._textBrowsed(result)

    def text(self):
        "Return the text in the text field"
        return self.lineEdit.text()

    def setText(self, s):
        "Set the text in the text field"
        self.lineEdit.setText(s)

class TextAndBrowseGroupBox(QtGui.QGroupBox):
    """
    A widget that has both a text input field and a browse button
    """
    def __init__(self, label='', browseLabel='', browseFunc=None, default='', browseIcon=None, parent=None):
        """
        Instantiate a TextAndBrowseWidget

        label is the name of the field
        browseLabel is the label on the browse button
        browseFunc is the function called when the browse
                   button is pressed and either returns
                   None for no change or returns a new string
                   It takes the string in the text field as input
        default is the default value in the text field
        browseIcon is an optional icon for the button

        This widget emits the following signals:
          textChanged(QString) - when the text changes
          textEdited(QString) - when the text has been edited in the edit box
          textBrowsed(QString) - when the text has been changed by the browser

        This widget accepts the following slots:
          setText(str) - set the text in the input field
        """
        QtGui.QGroupBox.__init__(self, label, parent)

        # create the UI
        self.lineEdit = QtGui.QLineEdit(default)
        if browseIcon:
            self.browseButton = QtGui.QPushButton(browseIcon,browseLabel)
        else:
            self.browseButton = QtGui.QPushButton(browseLabel)
        self._browseFunc = browseFunc
        self.groupLayout = QtGui.QHBoxLayout()
        self.groupLayout.addWidget(self.lineEdit)
        self.groupLayout.addWidget(self.browseButton)
        self.groupLayout.setStretchFactor(self.lineEdit,1)
        self.setLayout(self.groupLayout)

        # connect the signals
        self.connect(self.lineEdit,QtCore.SIGNAL('textChanged(QString)'),
                     self._textChanged)
        self.connect(self.lineEdit,QtCore.SIGNAL('textEdited(QString)'),
                     self._textEdited)
        self.connect(self.browseButton,QtCore.SIGNAL('clicked(bool)'),
                     self._browseClicked)

    def _textChanged(self, s):
        self.emit(QtCore.SIGNAL('textChanged(QString)'), s)

    def _textEdited(self, s):
        self.emit(QtCore.SIGNAL('textEdited(QString)'), s)

    def _textBrowsed(self, s):
        self.emit(QtCore.SIGNAL('textBrowsed(QString)'), s)

    def _browseClicked(self):
        if not self._browseFunc:
            return # no browse function defined
        result = self._browseFunc(self.lineEdit.text())
        if result != None:
            self.lineEdit.setText(result)
            self._textBrowsed(result)

    def text(self):
        "Return the text in the text field"
        return self.lineEdit.text()

    def setText(self, s):
        "Set the text in the text field"
        self.lineEdit.setText(s)

class PathSelectorWidget(TextAndBrowseWidget):
    def __init__(self,  browseCaption='', default='', parent=None):
        TextAndBrowseWidget.__init__(self, '...', self.browseFunc, default, None, parent)
        self.browseCaption = browseCaption

    def browseFunc(self, default):
        result = QtGui.QFileDialog.getExistingDirectory(self, self.browseCaption, default)
        if result:
            return result
        else:
            return None
