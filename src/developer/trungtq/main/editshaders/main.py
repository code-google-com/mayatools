'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
modName = 'Edit Shaders'

from developer.main.common.QtSubWidget import QtSubWidget

class subWidget(QtSubWidget):
    def __init__(self, modList):
        QtSubWidget.__init__(self, modName, __file__, modList)
        