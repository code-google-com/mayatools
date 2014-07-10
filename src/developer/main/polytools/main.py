'''
Created on May 26, 2014

@author: trungtran
@description: This is the entry for package. Please do not touch to the file

'''
pkgname  = 'POLY TOOLS'

from developer.main.common.QtMainWidget import QtMainWidget

class mainWidget(QtMainWidget):
    def __init__(self, subpackages):
        QtMainWidget.__init__(self, subpackages, __file__)