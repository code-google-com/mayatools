class cleanerWidget(QtGui.QWidget):
    #checkedContent = QtCore.pyqtSignal('QString', name = 'tooggledStatus')
    def __init__(self, module = None):
        super(QtGui.QWidget, self).__init__()
        instanceModule = loadModule(module)
        self.label = QtGui.QLabel(instanceModule.description)
        self.button = QtGui.QPushButton('Execute')
        self.chkbox = QtGui.QCheckBox()
        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(self.chkbox)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1) 
        self.layout.addWidget(self.button)
        self.name = instanceModule.name
        self.chkbox.setChecked(True) 
        self.button.clicked.connect(instanceModule.execute)
        self.chkbox.clicked.connect(self.emitSignal)

    def toogleCheckBox(self):
        flag = self.chkbox.isChecked()
        self.chkbox.setChecked(not flag)
        #return self.chkbox
        
    def emitSignal(self):
        self.checkedContent.emit(str(self.chkbox.isChecked()) + '_' + self.name)
        print self.name
        