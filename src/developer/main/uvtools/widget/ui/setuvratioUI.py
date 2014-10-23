# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\uvtools\widget\ui\setuvratioUI.ui'
#
# Created: Thu Oct 23 16:43:13 2014
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
        MainWindow.resize(609, 150)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnSetUVScale = QtGui.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSetUVScale.setFont(font)
        self.btnSetUVScale.setObjectName(_fromUtf8("btnSetUVScale"))
        self.horizontalLayout.addWidget(self.btnSetUVScale)
        self.btnGetUVScale = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetUVScale.sizePolicy().hasHeightForWidth())
        self.btnGetUVScale.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnGetUVScale.setFont(font)
        self.btnGetUVScale.setObjectName(_fromUtf8("btnGetUVScale"))
        self.horizontalLayout.addWidget(self.btnGetUVScale)
        self.ldtRatio = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ldtRatio.sizePolicy().hasHeightForWidth())
        self.ldtRatio.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ldtRatio.setFont(font)
        self.ldtRatio.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.ldtRatio.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.ldtRatio.setObjectName(_fromUtf8("ldtRatio"))
        self.horizontalLayout.addWidget(self.ldtRatio)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btn64 = QtGui.QPushButton(self.groupBox)
        self.btn64.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);\n"
"background-color: rgb(195, 195, 195);"))
        self.btn64.setProperty("texel", 64)
        self.btn64.setObjectName(_fromUtf8("btn64"))
        self.horizontalLayout_2.addWidget(self.btn64)
        self.btn96 = QtGui.QPushButton(self.groupBox)
        self.btn96.setProperty("texel", 96)
        self.btn96.setObjectName(_fromUtf8("btn96"))
        self.horizontalLayout_2.addWidget(self.btn96)
        self.btn128 = QtGui.QPushButton(self.groupBox)
        self.btn128.setStyleSheet(_fromUtf8("background-color: rgb(195, 195, 195);\n"
"color: rgb(0, 0, 0);"))
        self.btn128.setProperty("texel", 128)
        self.btn128.setObjectName(_fromUtf8("btn128"))
        self.horizontalLayout_2.addWidget(self.btn128)
        self.btn256 = QtGui.QPushButton(self.groupBox)
        self.btn256.setProperty("texel", 256)
        self.btn256.setObjectName(_fromUtf8("btn256"))
        self.horizontalLayout_2.addWidget(self.btn256)
        self.btn512 = QtGui.QPushButton(self.groupBox)
        self.btn512.setStyleSheet(_fromUtf8("background-color: rgb(195, 195, 195);\n"
"color: rgb(0, 0, 0);"))
        self.btn512.setProperty("texel", 512)
        self.btn512.setObjectName(_fromUtf8("btn512"))
        self.horizontalLayout_2.addWidget(self.btn512)
        self.btn1024 = QtGui.QPushButton(self.groupBox)
        self.btn1024.setProperty("texel", 1024)
        self.btn1024.setObjectName(_fromUtf8("btn1024"))
        self.horizontalLayout_2.addWidget(self.btn1024)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnSetTexel = QtGui.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSetTexel.setFont(font)
        self.btnSetTexel.setObjectName(_fromUtf8("btnSetTexel"))
        self.horizontalLayout_3.addWidget(self.btnSetTexel)
        self.ldtTexel = QtGui.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ldtTexel.setFont(font)
        self.ldtTexel.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.ldtTexel.setInputMask(_fromUtf8(""))
        self.ldtTexel.setText(_fromUtf8(""))
        self.ldtTexel.setObjectName(_fromUtf8("ldtTexel"))
        self.horizontalLayout_3.addWidget(self.ldtTexel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Scale UV", None))
        self.btnSetUVScale.setText(_translate("MainWindow", "Set UV Scale", None))
        self.btnGetUVScale.setText(_translate("MainWindow", "Get UV Scale", None))
        self.ldtRatio.setText(_translate("MainWindow", "25", None))
        self.ldtRatio.setPlaceholderText(_translate("MainWindow", "--ratio--", None))
        self.btn64.setText(_translate("MainWindow", "64", None))
        self.btn96.setText(_translate("MainWindow", "96", None))
        self.btn128.setText(_translate("MainWindow", "128", None))
        self.btn256.setText(_translate("MainWindow", "256", None))
        self.btn512.setText(_translate("MainWindow", "512", None))
        self.btn1024.setText(_translate("MainWindow", "1024", None))
        self.btnSetTexel.setText(_translate("MainWindow", "Set texel (pixel/meter)", None))
        self.ldtTexel.setPlaceholderText(_translate("MainWindow", "-- texel--", None))

