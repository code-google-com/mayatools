'''
Created on May 27, 2014

@author: trungtran
@email: trungswat@gmail.com
@description: ''

'''
from developer.main.common import commonFunctions
from developer.main.polytools.mirrortools.fn import mirrorFunction as mFn

import os, inspect, functools

#-- get ui path:
filedircommon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
fileNamePrefix = os.path.split(inspect.getfile(inspect.currentframe()))[1].split('.')[0]
uiFile = filedircommon + '/ui/' + fileNamePrefix.replace('Form','UI')
#-- end gt ui path

#-- load ui 
if os.path.isfile(uiFile):
    form_class, base_class = CommonFunctions.loadPyQtUI(uiFile)
else:
    print 'not found ui file:' + uiFile
    return
#-- end load ui

class mirrorForm(form_class,base_class):
    '''
    Description: doing some mirror function.
    '''
    def __init__(self, parent = CommonFunctions.getMayaWindow()):
        super(base_class,self).__init__(parent)
        self.setupUi(self)
        self.btnAxisX.clicked.connect(functools.partial(mFn.mirror, 'x', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By axis'))
        self.btnAxisY.clicked.connect(functools.partial(mFn.mirror, 'y', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By axis'))
        self.btnAxisZ.clicked.connect(functools.partial(mFn.mirror, 'z', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By axis'))
                                                                                                               
        self.btnPivotX.clicked.connect(functools.partial(mFn.mirror, 'x', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By pivot'))
        self.btnPivotY.clicked.connect(functools.partial(mFn.mirror, 'y', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By pivot'))
        self.btnPivotZ.clicked.connect(functools.partial(mFn.mirror, 'z', self.rdbKeepHistory.isChecked(), self.rdbNoClone.isChecked(), 'By pivot'))  
                    
def main():
    form = mirrorForm()
    return form