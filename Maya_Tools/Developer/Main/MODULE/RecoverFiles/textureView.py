import maya.cmds as cmds
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect


fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/textureView.ui'

form_class, base_class = uic.loadUiType(dirUI)  

class textureView(QtGui.QGraphicsView, form_class,base_class):
    def __init__(self):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.pixmap = QtGui.QPixmap()
        
    def scaleImage(self, para ):
        pass
            
    def showImage(self, fileName):
        scene = QtGui.QGraphicsScene()
        self.graphicsView.setScene(scene)
        self.pixmap.load(fileName)
        #pixmap = pixmap.scaled(72,72, QtCore.Qt.IgnoreAspectRatio)
        scene.addItem(QtGui.QGraphicsPixmapItem(self.pixmap))
        self.graphicsView.fitInView(scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.graphicsView.show()
        
def main():
    form = textureView()
    return form