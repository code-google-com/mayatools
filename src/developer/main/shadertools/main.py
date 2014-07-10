'''
Created on Jun 21, 2014

@author: Trung
'''

pkgname = 'SHADER TOOLS'

from developer.main.common.mainWidget import QtMainWidget

class mainWidget(QtMainWidget):
    def __init__(self, subpackages):
        QtMainWidget.__init__(self, subpackages, __file__)