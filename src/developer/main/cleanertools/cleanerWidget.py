from PyQt4 import QtGui
try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf

class cleanerWidget(QtGui.QWidget):
    #checkedContent = QtCore.pyqtSignal('QString', name = 'tooggledStatus')
    def __init__(self, modName, *arg):
        super(QtGui.QWidget, self).__init__()
        mod = cf.loadNestedModule('developer.main.cleanertools.' + modName)
        self.createGUI('Execute', mod.description, mod.tooltip)
        # ui signal
        self.button.clicked.connect(mod.execute)
        #self.chkbox.clicked.connect(self.emitSignal)

    def createGUI(self, *arg):
        self.label = QtGui.QLabel(arg[1]) # get description 
        self.button = QtGui.QPushButton(arg[0]) # get 'Execute' assign to button name
        self.button.setToolTip(arg[2])
        self.chkbox = QtGui.QCheckBox()
        self.chkbox.setChecked(True)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.chkbox)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1) 
        self.layout.addWidget(self.button)

        
    def setEnabled(self, status):
        if status:
            self.chkbox.setChecked(True)
        else:
            self.chkbox.setChecked(False)
        