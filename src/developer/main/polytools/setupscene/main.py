'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
modName = 'SETUP SCENE'

from developer.main.common.QtSubWidget import QtSubWidget

class subWidget(QtSubWidget):
    def __init__(self):
        QtSubWidget.__init__(self, modName, __file__)