import clearnersetitems as csi # cleanersetitems

class subWidget(QtGui.QWidget):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Tech Tools'
        self._contentCleanUp = list()
        self._customCheck = inputFile
        self.btnCheckAll.clicked.connect(self.executeAll)
        
        self.loadFunction()
        
    def loadFunction(self):
        contentToCleanUpCommon = [(fileDirCommmon + '/' + f) for f in os.listdir(fileDirCommmon) if os.path.isdir(fileDirCommmon + '/' + f) and f not in ['UI']]#,'Technical Setup','Fix issues per mesh']]
        contentToCleanUpProject = []
        project = self._customCheck.split('.')[0]
        customPath = os.path.split(os.path.split(os.path.split(fileDirCommmon)[0])[0])[0]
        try:
             contentToCleanUpProject = [(customPath + '/Project/' + project + '/python/' + f) for f in os.listdir(customPath + '/Project/' + project + '/python/')if os.path.isdir(customPath + '/Project/' + project + '/python/' + f) and f != 'UI']
        except:
             pass
        for f in contentToCleanUpCommon + contentToCleanUpProject:
            self.contents.addWidget(csi.cleanerSetWidget(f))
            
    def updateContent(self, strResult):
        if bool(strResult.split('_')[0]):
            self._contentCleanUp.append(strResult.split('_')[1])
        else:
            self._contentCleanUp.remove(strResult.split('_')[1])
        print self._contentCleanUp
        
    def executeAll(self):
        for module in self._contentCleanUp:
            instanceModule = loadModule(fileDirCommmon + '/python/', module)
            instanceModule.execute()


