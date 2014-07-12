'''
Created on Jun 27, 2014

@author: Trung
'''

from developer.main.polytools.modeltools.fn import modeltoolsFn as mFn

try:
    reload(ui)
except:
    from developer.main.polytools.modeltools.widget.ui import modeltoolsUI as ui

from PyQt4 import QtGui


class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(parent = None)
        self.setupUi(self)
        self.setObjectName('modelingToolbox')
        