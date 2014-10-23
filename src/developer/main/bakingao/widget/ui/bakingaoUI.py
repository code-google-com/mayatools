# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\bakingao\widget\ui\bakingaoUI.ui'
#
# Created: Thu Oct 23 12:26:12 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(331, 81)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setMargin(3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.btnSetGroundPlane = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetGroundPlane.sizePolicy().hasHeightForWidth())
        self.btnSetGroundPlane.setSizePolicy(sizePolicy)
        self.btnSetGroundPlane.setObjectName(_fromUtf8("btnSetGroundPlane"))
        self.horizontalLayout_5.addWidget(self.btnSetGroundPlane)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.btnBakeToVertex = QtGui.QPushButton(self.groupBox_3)
        self.btnBakeToVertex.setObjectName(_fromUtf8("btnBakeToVertex"))
        self.horizontalLayout_7.addWidget(self.btnBakeToVertex)
        self.btnBakeToTexture = QtGui.QPushButton(self.groupBox_3)
        self.btnBakeToTexture.setObjectName(_fromUtf8("btnBakeToTexture"))
        self.horizontalLayout_7.addWidget(self.btnBakeToTexture)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnSetGroundPlane.setText(_translate("MainWindow", "Setup Ground Plane", None))
        self.btnBakeToVertex.setText(_translate("MainWindow", "Bake AO to Vertex ...", None))
        self.btnBakeToTexture.setText(_translate("MainWindow", "Bake AO to Texture ...", None))

