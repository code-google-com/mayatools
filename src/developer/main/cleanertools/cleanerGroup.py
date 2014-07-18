try:
    reload(clw)
except:
    import cleanerWidget as clw


class cleanerGroup(dW.DockWidget):
    def __init__(self, pkgName, filterList):
        super(dockWidget.DockWidget, self).__init__(os.path.split(pkgName))
        self.createGUI()
        self.loadChildrenTesting()
        
    def createGUI(self):
        self.titleBar = dockWidget.DockWidgetTitleBar(self)
        self.setTitleBarWidget(self.titleBar)
        self._layout = QtGui.QVBoxLayout()
        self._layout.setSpacing(1)
        self._layout.setContentsMargins(margins) 
        self._container = QtGui.QWidget()
        self._container.setLayout(self._layout)
        self.setWidget(self._container)
        
        if len(filterList):
            contentCheck = ''
        else: 
            pass
        contentToCleanUpCommon = [(self._dir + '/' + f) for f in os.listdir(self._dir) if f.endswith('py')]
        for module in contentToCleanUpCommon:
            widget = clw.cleanerWidget(module)
            self._layout.addLayout(widget.layout)
