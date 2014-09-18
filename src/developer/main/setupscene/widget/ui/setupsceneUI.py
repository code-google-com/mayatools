# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\setupscene\widget\ui\setupsceneUI.ui'
#
# Created: Thu Sep 18 14:38:29 2014
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
        MainWindow.resize(268, 123)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setTitle(_fromUtf8(""))
        self.groupBox_5.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_6.setMargin(3)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.btnSetupAxis = QtGui.QPushButton(self.groupBox_5)
        self.btnSetupAxis.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Y_up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSetupAxis.setIcon(icon)
        self.btnSetupAxis.setIconSize(QtCore.QSize(50, 50))
        self.btnSetupAxis.setCheckable(False)
        self.btnSetupAxis.setFlat(True)
        self.btnSetupAxis.setObjectName(_fromUtf8("btnSetupAxis"))
        self.horizontalLayout_7.addWidget(self.btnSetupAxis)
        self.btnSetupBackground = QtGui.QPushButton(self.groupBox_5)
        self.btnSetupBackground.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/background.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSetupBackground.setIcon(icon1)
        self.btnSetupBackground.setIconSize(QtCore.QSize(50, 50))
        self.btnSetupBackground.setCheckable(False)
        self.btnSetupBackground.setFlat(True)
        self.btnSetupBackground.setObjectName(_fromUtf8("btnSetupBackground"))
        self.horizontalLayout_7.addWidget(self.btnSetupBackground)
        self.btnSetNormalSize = QtGui.QPushButton(self.groupBox_5)
        self.btnSetNormalSize.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.btnSetNormalSize.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/normal_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSetNormalSize.setIcon(icon2)
        self.btnSetNormalSize.setIconSize(QtCore.QSize(50, 50))
        self.btnSetNormalSize.setCheckable(True)
        self.btnSetNormalSize.setFlat(True)
        self.btnSetNormalSize.setObjectName(_fromUtf8("btnSetNormalSize"))
        self.horizontalLayout_7.addWidget(self.btnSetNormalSize)
        self.btnDisplayOptions = QtGui.QPushButton(self.groupBox_5)
        self.btnDisplayOptions.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.btnDisplayOptions.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/display_options.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDisplayOptions.setIcon(icon3)
        self.btnDisplayOptions.setIconSize(QtCore.QSize(50, 50))
        self.btnDisplayOptions.setFlat(True)
        self.btnDisplayOptions.setObjectName(_fromUtf8("btnDisplayOptions"))
        self.horizontalLayout_7.addWidget(self.btnDisplayOptions)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.groupBox_5)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnSetupAxis.setToolTip(_translate("MainWindow", "change Axis", None))

import developer.main.source.IconResource_rc
