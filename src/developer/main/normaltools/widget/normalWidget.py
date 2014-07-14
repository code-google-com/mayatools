'''
Created on Jun 27, 2014

@author: Trung
'''
try:
    reload(mFn)
except:
    from developer.main.modeltools.fn import modeltoolsFn as mFn

try:
    reload(ui)
except:
    from developer.main.normaltools.widget.ui import normalUI as ui

from PyQt4 import QtGui


class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(parent = None)
        self.setupUi(self)
        self.setObjectName('normalWidgetToolbox')
        