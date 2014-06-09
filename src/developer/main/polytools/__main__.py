'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''

from developer.main import CommonFunctions
CommonFunctions.importQtPlugin()

class polytoolsForm(QtGui.QWidget):
    def __init__(self, parent = None, subpackages):
        super(polytoolsForm, self)._init__(parent)
        self.vLayout = QtGui.QVBoxLayout()
        self.vSpacer = QtGui.QSpacer()
        self.setLayout(QtGui.QVBoxLayout)
        
    def loadSubPacks(subs):
        for p in subs:
            module = __import__(p + '.__main__')
            form = module.__load__()
    
        #-- get __main__ function from subpackages
         
        