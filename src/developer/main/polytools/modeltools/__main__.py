'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''

#import developer.main.dockWidget as dw
from developer.main import CommonFunctions
import inspect, os

CommonFunctions.importQtPlugin()
filedircommon = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class mainForm(QtGui.QWidget):
    def __init__(self, parent = None):
        super(mainForm).__init__(parent)
        self.vLayout  = QtGui.QVBoxLayout()
        self.loadChildForm()
        
    def loadChildForm(self):
        childForms = [module for module in os.listdir(filedircommon) if 'Form' in module and os.path.splitext(module)[1] == '.py']
        for c in childForms:
            instance = CommonFunctions.loadModule(c)
            self.vLayout.addWidget(instance.main())
            
def __main__():
    form = mainForm()
    return form
        