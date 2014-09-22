# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\debugshaders\widget\ui\debugshaderUI.ui'
#
# Created: Sat Sep 20 09:29:40 2014
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
        MainWindow.resize(487, 123)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setMargin(3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.btnShowAOOnly = QtGui.QPushButton(self.groupBox)
        self.btnShowAOOnly.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/AO.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnShowAOOnly.setIcon(icon)
        self.btnShowAOOnly.setIconSize(QtCore.QSize(50, 50))
        self.btnShowAOOnly.setCheckable(False)
        self.btnShowAOOnly.setFlat(True)
        self.btnShowAOOnly.setObjectName(_fromUtf8("btnShowAOOnly"))
        self.horizontalLayout_4.addWidget(self.btnShowAOOnly)
        self.btnReflectionView = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnReflectionView.sizePolicy().hasHeightForWidth())
        self.btnReflectionView.setSizePolicy(sizePolicy)
        self.btnReflectionView.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/shini.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReflectionView.setIcon(icon1)
        self.btnReflectionView.setIconSize(QtCore.QSize(50, 50))
        self.btnReflectionView.setCheckable(True)
        self.btnReflectionView.setFlat(True)
        self.btnReflectionView.setObjectName(_fromUtf8("btnReflectionView"))
        self.horizontalLayout_4.addWidget(self.btnReflectionView)
        self.btnNormalView = QtGui.QPushButton(self.groupBox)
        self.btnNormalView.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/normal.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnNormalView.setIcon(icon2)
        self.btnNormalView.setIconSize(QtCore.QSize(50, 50))
        self.btnNormalView.setCheckable(True)
        self.btnNormalView.setFlat(True)
        self.btnNormalView.setObjectName(_fromUtf8("btnNormalView"))
        self.horizontalLayout_4.addWidget(self.btnNormalView)
        self.btnCheckerView = QtGui.QPushButton(self.groupBox)
        self.btnCheckerView.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/checker.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCheckerView.setIcon(icon3)
        self.btnCheckerView.setIconSize(QtCore.QSize(50, 50))
        self.btnCheckerView.setCheckable(True)
        self.btnCheckerView.setFlat(True)
        self.btnCheckerView.setObjectName(_fromUtf8("btnCheckerView"))
        self.horizontalLayout_4.addWidget(self.btnCheckerView)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnShowAOOnly.setToolTip(_translate("MainWindow", "change to AO", None))
        self.btnReflectionView.setToolTip(_translate("MainWindow", "change to Shininess", None))
        self.btnNormalView.setToolTip(_translate("MainWindow", "change to Normal", None))
        self.btnCheckerView.setToolTip(_translate("MainWindow", "change to Checkerboard", None))

