class cleanerSetWidget(dW.DockWidget):
    def __init__(self, folderName):
        super(dockWidget.DockWidget, self).__init__(os.path.split(folderName)[-1])
        self.titleBar = dockWidget.DockWidgetTitleBar(self)
        self.setTitleBarWidget(self.titleBar)
        self._dir = folderName
        margins = QtCore.QMargins(1,1,1,1)
        self._layout = QtGui.QVBoxLayout()
        self._layout.setSpacing(1)
        self._layout.setContentsMargins(margins) 
        self._container = QtGui.QWidget()
        self._container.setLayout(self._layout)
        self.setWidget(self._container)
        self.loadChildrenTesting()
        
    def loadChildrenTesting(self):
        contentToCleanUpCommon = [(self._dir + '/' + f) for f in os.listdir(self._dir) if f.endswith('py')]
        for module in contentToCleanUpCommon:
            widget = cleanerWidget(module)
            self._layout.addLayout(widget.layout)
