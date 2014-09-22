# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\uvtools\widget\ui\setuvratioUI.ui'
#
# Created: Sat Sep 20 09:29:42 2014
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
        MainWindow.resize(399, 81)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
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
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setMargin(3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
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
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnSetTexel = QtGui.QPushButton(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSetTexel.setFont(font)
        self.btnSetTexel.setObjectName(_fromUtf8("btnSetTexel"))
        self.horizontalLayout_2.addWidget(self.btnSetTexel)
        self.ldtRes = QtGui.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ldtRes.setFont(font)
        self.ldtRes.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.ldtRes.setEchoMode(QtGui.QLineEdit.Normal)
        self.ldtRes.setObjectName(_fromUtf8("ldtRes"))
        self.horizontalLayout_2.addWidget(self.ldtRes)
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
        self.ldtTexel.setObjectName(_fromUtf8("ldtTexel"))
        self.horizontalLayout_2.addWidget(self.ldtTexel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnSetUVScale.setText(_translate("MainWindow", "Set UV Scale", None))
        self.btnGetUVScale.setText(_translate("MainWindow", "Get UV Scale", None))
        self.ldtRatio.setText(_translate("MainWindow", "25", None))
        self.ldtRatio.setPlaceholderText(_translate("MainWindow", "--ratio--", None))
        self.btnSetTexel.setText(_translate("MainWindow", "Set texel", None))
        self.ldtRes.setText(_translate("MainWindow", "1024", None))
        self.ldtRes.setPlaceholderText(_translate("MainWindow", "--resolution--", None))
        self.ldtTexel.setText(_translate("MainWindow", "204.8", None))
        self.ldtTexel.setPlaceholderText(_translate("MainWindow", "-- texel--", None))

