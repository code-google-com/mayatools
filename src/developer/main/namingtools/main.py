pkgname  = 'NAMING TOOLS'

from developer.main.common.QtMainWidget import QtMainWidget

class mainWidget(QtMainWidget):
    def __init__(self, subpackages):
        QtMainWidget.__init__(self, subpackages, __file__)