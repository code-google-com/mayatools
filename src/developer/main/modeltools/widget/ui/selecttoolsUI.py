# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\modeltools\widget\ui\selecttoolsUI.ui'
#
# Created: Sun Sep 14 20:55:59 2014
#      by: PyQt4 UI code generator 4.11
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
        MainWindow.resize(457, 221)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(3, 3, 3, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_2.addWidget(self.line)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnSelectHardEdges = QtGui.QPushButton(self.groupBox)
        self.btnSelectHardEdges.setObjectName(_fromUtf8("btnSelectHardEdges"))
        self.horizontalLayout.addWidget(self.btnSelectHardEdges)
        self.btnSelectSoftEdges = QtGui.QPushButton(self.groupBox)
        self.btnSelectSoftEdges.setObjectName(_fromUtf8("btnSelectSoftEdges"))
        self.horizontalLayout.addWidget(self.btnSelectSoftEdges)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btnSelectContEdges = QtGui.QPushButton(self.groupBox)
        self.btnSelectContEdges.setObjectName(_fromUtf8("btnSelectContEdges"))
        self.verticalLayout.addWidget(self.btnSelectContEdges)
        self.pushButton_4 = QtGui.QPushButton(self.groupBox)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.verticalLayout.addWidget(self.pushButton_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.spnRing = QtGui.QSpinBox(self.groupBox)
        self.spnRing.setMaximum(98)
        self.spnRing.setProperty("value", 1)
        self.spnRing.setObjectName(_fromUtf8("spnRing"))
        self.horizontalLayout_3.addWidget(self.spnRing)
        self.btnRingEdges = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRingEdges.sizePolicy().hasHeightForWidth())
        self.btnRingEdges.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnRingEdges.setFont(font)
        self.btnRingEdges.setObjectName(_fromUtf8("btnRingEdges"))
        self.horizontalLayout_3.addWidget(self.btnRingEdges)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.spnLoop = QtGui.QSpinBox(self.groupBox)
        self.spnLoop.setProperty("value", 1)
        self.spnLoop.setObjectName(_fromUtf8("spnLoop"))
        self.horizontalLayout_5.addWidget(self.spnLoop)
        self.btnLoopEdges = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLoopEdges.sizePolicy().hasHeightForWidth())
        self.btnLoopEdges.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnLoopEdges.setFont(font)
        self.btnLoopEdges.setObjectName(_fromUtf8("btnLoopEdges"))
        self.horizontalLayout_5.addWidget(self.btnLoopEdges)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Select Edges", None))
        self.btnSelectHardEdges.setText(_translate("MainWindow", "Select HardEdges", None))
        self.btnSelectSoftEdges.setText(_translate("MainWindow", "Select SoftEdges", None))
        self.btnSelectContEdges.setText(_translate("MainWindow", "Select Continous Edges", None))
        self.pushButton_4.setText(_translate("MainWindow", "Select Shortest Edges", None))
        self.btnRingEdges.setText(_translate("MainWindow", "Dot ring selection", None))
        self.btnLoopEdges.setText(_translate("MainWindow", "Dot loop selection", None))

