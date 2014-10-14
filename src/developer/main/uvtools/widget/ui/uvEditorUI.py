# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\uvtools\widget\ui\uvEditorUI.ui'
#
# Created: Mon Oct 13 11:54:52 2014
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
        MainWindow.resize(452, 72)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnOpenUVEditor = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOpenUVEditor.sizePolicy().hasHeightForWidth())
        self.btnOpenUVEditor.setSizePolicy(sizePolicy)
        self.btnOpenUVEditor.setMinimumSize(QtCore.QSize(0, 50))
        self.btnOpenUVEditor.setSizeIncrement(QtCore.QSize(0, 30))
        self.btnOpenUVEditor.setBaseSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnOpenUVEditor.setFont(font)
        self.btnOpenUVEditor.setObjectName(_fromUtf8("btnOpenUVEditor"))
        self.verticalLayout.addWidget(self.btnOpenUVEditor)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnOpenUVEditor.setText(_translate("MainWindow", "Open UV Editor", None))

