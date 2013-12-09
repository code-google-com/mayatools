from PyQt4 import QtGui, QtCore, uic
import sip, os, inspect
import maya.OpenMayaUI as OpenMayaUI

    
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/common.ui'
try:
    form_class, base_class = uic.loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)

class CommonDockWidget(form_class,base_class):
    def __init__(self, widget1, widget2, parent = getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.dockwidget_01.setWidget(widget1)
        self.dockwidget_02.setWidget(widget2)
        
    def resizeEvent(self, event):
        h = self.height()
        w = self.width()
        #self.dockwidget_01.widget().setMinimumHeight(h)
        #self.dockwidget_02.widget().setMinimumHeight(h)
        
             
        
            
               
            
                
    

        

                
