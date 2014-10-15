# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\uvtools\widget\ui\transferuvUI.ui'
#
# Created: Wed Oct 15 10:01:27 2014
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
        MainWindow.resize(328, 154)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.ldtSource = QtGui.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ldtSource.setFont(font)
        self.ldtSource.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ldtSource.setText(_fromUtf8(""))
        self.ldtSource.setFrame(False)
        self.ldtSource.setEchoMode(QtGui.QLineEdit.Normal)
        self.ldtSource.setDragEnabled(True)
        self.ldtSource.setObjectName(_fromUtf8("ldtSource"))
        self.horizontalLayout_4.addWidget(self.ldtSource)
        self.cbbSourceMat = QtGui.QComboBox(self.groupBox)
        self.cbbSourceMat.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cbbSourceMat.setFrame(False)
        self.cbbSourceMat.setObjectName(_fromUtf8("cbbSourceMat"))
        self.horizontalLayout_4.addWidget(self.cbbSourceMat)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.ldtTarget = QtGui.QLineEdit(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ldtTarget.setFont(font)
        self.ldtTarget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ldtTarget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ldtTarget.setAutoFillBackground(True)
        self.ldtTarget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.ldtTarget.setText(_fromUtf8(""))
        self.ldtTarget.setFrame(False)
        self.ldtTarget.setEchoMode(QtGui.QLineEdit.Normal)
        self.ldtTarget.setDragEnabled(True)
        self.ldtTarget.setObjectName(_fromUtf8("ldtTarget"))
        self.horizontalLayout_5.addWidget(self.ldtTarget)
        self.cbbTargetMat = QtGui.QComboBox(self.groupBox)
        self.cbbTargetMat.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cbbTargetMat.setObjectName(_fromUtf8("cbbTargetMat"))
        self.horizontalLayout_5.addWidget(self.cbbTargetMat)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.btnTransferUV = QtGui.QPushButton(self.groupBox)
        self.btnTransferUV.setObjectName(_fromUtf8("btnTransferUV"))
        self.verticalLayout.addWidget(self.btnTransferUV)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Source -- (mesh with correct UVs)", None))
        self.ldtSource.setPlaceholderText(_translate("MainWindow", "please get source node", None))
        self.label_2.setText(_translate("MainWindow", "Target -- (mesh with wrong UVs)", None))
        self.ldtTarget.setPlaceholderText(_translate("MainWindow", "please get target node", None))
        self.btnTransferUV.setText(_translate("MainWindow", "Transfer UV", None))

