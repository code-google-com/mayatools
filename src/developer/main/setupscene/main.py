modName = 'SETUP SCENE'

from developer.main.common.QtSubWidget import QtSubWidget

class subWidget(QtSubWidget):
    def __init__(self, modList):
        QtSubWidget.__init__(self, modName, __file__, modList)
        