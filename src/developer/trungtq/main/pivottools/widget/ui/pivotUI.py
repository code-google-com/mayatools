# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\pivottools\widget\ui\pivotUI.ui'
#
# Created: Mon Sep 15 18:57:26 2014
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
        MainWindow.resize(509, 310)
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnPivottoCenterElement = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPivottoCenterElement.sizePolicy().hasHeightForWidth())
        self.btnPivottoCenterElement.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnPivottoCenterElement.setFont(font)
        self.btnPivottoCenterElement.setObjectName(_fromUtf8("btnPivottoCenterElement"))
        self.horizontalLayout.addWidget(self.btnPivottoCenterElement)
        self.btnCenterPivot = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCenterPivot.sizePolicy().hasHeightForWidth())
        self.btnCenterPivot.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnCenterPivot.setFont(font)
        self.btnCenterPivot.setObjectName(_fromUtf8("btnCenterPivot"))
        self.horizontalLayout.addWidget(self.btnCenterPivot)
        self.btnPivottoOrigin = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPivottoOrigin.sizePolicy().hasHeightForWidth())
        self.btnPivottoOrigin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnPivottoOrigin.setFont(font)
        self.btnPivottoOrigin.setObjectName(_fromUtf8("btnPivottoOrigin"))
        self.horizontalLayout.addWidget(self.btnPivottoOrigin)
        self.btnPivottoanotherObj = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPivottoanotherObj.sizePolicy().hasHeightForWidth())
        self.btnPivottoanotherObj.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnPivottoanotherObj.setFont(font)
        self.btnPivottoanotherObj.setObjectName(_fromUtf8("btnPivottoanotherObj"))
        self.horizontalLayout.addWidget(self.btnPivottoanotherObj)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnFreezeTransform = QtGui.QPushButton(self.groupBox)
        self.btnFreezeTransform.setObjectName(_fromUtf8("btnFreezeTransform"))
        self.horizontalLayout_2.addWidget(self.btnFreezeTransform)
        self.btnZeroOffset = QtGui.QPushButton(self.groupBox)
        self.btnZeroOffset.setObjectName(_fromUtf8("btnZeroOffset"))
        self.horizontalLayout_2.addWidget(self.btnZeroOffset)
        self.btnRotatePivot = QtGui.QPushButton(self.groupBox)
        self.btnRotatePivot.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
        self.btnRotatePivot.setObjectName(_fromUtf8("btnRotatePivot"))
        self.horizontalLayout_2.addWidget(self.btnRotatePivot)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnPivotOnFace = QtGui.QPushButton(self.groupBox)
        self.btnPivotOnFace.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
        self.btnPivotOnFace.setObjectName(_fromUtf8("btnPivotOnFace"))
        self.horizontalLayout_3.addWidget(self.btnPivotOnFace)
        self.btnSetPivotAlongEdge = QtGui.QPushButton(self.groupBox)
        self.btnSetPivotAlongEdge.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
        self.btnSetPivotAlongEdge.setObjectName(_fromUtf8("btnSetPivotAlongEdge"))
        self.horizontalLayout_3.addWidget(self.btnSetPivotAlongEdge)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_2 = QtGui.QFrame(self.groupBox)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rdbZmin = QtGui.QPushButton(self.groupBox)
        self.rdbZmin.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/ZMin.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbZmin.setIcon(icon)
        self.rdbZmin.setIconSize(QtCore.QSize(40, 40))
        self.rdbZmin.setCheckable(True)
        self.rdbZmin.setFlat(True)
        self.rdbZmin.setObjectName(_fromUtf8("rdbZmin"))
        self.buttonGroup_2 = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup_2.setObjectName(_fromUtf8("buttonGroup_2"))
        self.buttonGroup_2.addButton(self.rdbZmin)
        self.gridLayout.addWidget(self.rdbZmin, 3, 1, 1, 1)
        self.rdbY = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdbY.sizePolicy().hasHeightForWidth())
        self.rdbY.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbY.setFont(font)
        self.rdbY.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Y.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbY.setIcon(icon1)
        self.rdbY.setIconSize(QtCore.QSize(40, 40))
        self.rdbY.setCheckable(False)
        self.rdbY.setAutoExclusive(False)
        self.rdbY.setFlat(True)
        self.rdbY.setObjectName(_fromUtf8("rdbY"))
        self.gridLayout.addWidget(self.rdbY, 2, 0, 1, 1)
        self.rdbYmid = QtGui.QPushButton(self.groupBox)
        self.rdbYmid.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/YMid.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbYmid.setIcon(icon2)
        self.rdbYmid.setIconSize(QtCore.QSize(40, 40))
        self.rdbYmid.setCheckable(True)
        self.rdbYmid.setFlat(True)
        self.rdbYmid.setObjectName(_fromUtf8("rdbYmid"))
        self.buttonGroup_3 = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup_3.setObjectName(_fromUtf8("buttonGroup_3"))
        self.buttonGroup_3.addButton(self.rdbYmid)
        self.gridLayout.addWidget(self.rdbYmid, 2, 2, 1, 1)
        self.rdbZ = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdbZ.sizePolicy().hasHeightForWidth())
        self.rdbZ.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbZ.setFont(font)
        self.rdbZ.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Z.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbZ.setIcon(icon3)
        self.rdbZ.setIconSize(QtCore.QSize(40, 40))
        self.rdbZ.setCheckable(False)
        self.rdbZ.setAutoExclusive(False)
        self.rdbZ.setFlat(True)
        self.rdbZ.setObjectName(_fromUtf8("rdbZ"))
        self.gridLayout.addWidget(self.rdbZ, 3, 0, 1, 1)
        self.rdbYmax = QtGui.QPushButton(self.groupBox)
        self.rdbYmax.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/YMax.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbYmax.setIcon(icon4)
        self.rdbYmax.setIconSize(QtCore.QSize(40, 40))
        self.rdbYmax.setCheckable(True)
        self.rdbYmax.setFlat(True)
        self.rdbYmax.setObjectName(_fromUtf8("rdbYmax"))
        self.buttonGroup_3.addButton(self.rdbYmax)
        self.gridLayout.addWidget(self.rdbYmax, 2, 3, 1, 1)
        self.rdbZmax = QtGui.QPushButton(self.groupBox)
        self.rdbZmax.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/ZMax.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbZmax.setIcon(icon5)
        self.rdbZmax.setIconSize(QtCore.QSize(40, 40))
        self.rdbZmax.setCheckable(True)
        self.rdbZmax.setFlat(True)
        self.rdbZmax.setObjectName(_fromUtf8("rdbZmax"))
        self.buttonGroup_2.addButton(self.rdbZmax)
        self.gridLayout.addWidget(self.rdbZmax, 3, 3, 1, 1)
        self.rdbXmid = QtGui.QPushButton(self.groupBox)
        self.rdbXmid.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/XMid.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbXmid.setIcon(icon6)
        self.rdbXmid.setIconSize(QtCore.QSize(40, 40))
        self.rdbXmid.setCheckable(True)
        self.rdbXmid.setFlat(True)
        self.rdbXmid.setObjectName(_fromUtf8("rdbXmid"))
        self.buttonGroup = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.rdbXmid)
        self.gridLayout.addWidget(self.rdbXmid, 0, 2, 1, 1)
        self.rdbXmax = QtGui.QPushButton(self.groupBox)
        self.rdbXmax.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/XMax.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbXmax.setIcon(icon7)
        self.rdbXmax.setIconSize(QtCore.QSize(40, 40))
        self.rdbXmax.setCheckable(True)
        self.rdbXmax.setFlat(True)
        self.rdbXmax.setObjectName(_fromUtf8("rdbXmax"))
        self.buttonGroup.addButton(self.rdbXmax)
        self.gridLayout.addWidget(self.rdbXmax, 0, 3, 1, 1)
        self.rdbXmin = QtGui.QPushButton(self.groupBox)
        self.rdbXmin.setText(_fromUtf8(""))
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/XMin.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbXmin.setIcon(icon8)
        self.rdbXmin.setIconSize(QtCore.QSize(40, 40))
        self.rdbXmin.setCheckable(True)
        self.rdbXmin.setFlat(True)
        self.rdbXmin.setObjectName(_fromUtf8("rdbXmin"))
        self.buttonGroup.addButton(self.rdbXmin)
        self.gridLayout.addWidget(self.rdbXmin, 0, 1, 1, 1)
        self.rdbX = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rdbX.sizePolicy().hasHeightForWidth())
        self.rdbX.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbX.setFont(font)
        self.rdbX.setText(_fromUtf8(""))
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/X.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbX.setIcon(icon9)
        self.rdbX.setIconSize(QtCore.QSize(40, 40))
        self.rdbX.setCheckable(False)
        self.rdbX.setAutoExclusive(False)
        self.rdbX.setFlat(True)
        self.rdbX.setObjectName(_fromUtf8("rdbX"))
        self.gridLayout.addWidget(self.rdbX, 0, 0, 1, 1)
        self.rdbZmid = QtGui.QPushButton(self.groupBox)
        self.rdbZmid.setText(_fromUtf8(""))
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/ZMid.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbZmid.setIcon(icon10)
        self.rdbZmid.setIconSize(QtCore.QSize(40, 40))
        self.rdbZmid.setCheckable(True)
        self.rdbZmid.setFlat(True)
        self.rdbZmid.setObjectName(_fromUtf8("rdbZmid"))
        self.buttonGroup_2.addButton(self.rdbZmid)
        self.gridLayout.addWidget(self.rdbZmid, 3, 2, 1, 1)
        self.rdbYmin = QtGui.QPushButton(self.groupBox)
        self.rdbYmin.setText(_fromUtf8(""))
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/YMin.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rdbYmin.setIcon(icon11)
        self.rdbYmin.setIconSize(QtCore.QSize(40, 40))
        self.rdbYmin.setCheckable(True)
        self.rdbYmin.setFlat(True)
        self.rdbYmin.setObjectName(_fromUtf8("rdbYmin"))
        self.buttonGroup_3.addButton(self.rdbYmin)
        self.gridLayout.addWidget(self.rdbYmin, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnPivottoCenterElement.setToolTip(_translate("MainWindow", "Center to element", None))
        self.btnPivottoCenterElement.setText(_translate("MainWindow", "2_CenterSel", None))
        self.btnCenterPivot.setToolTip(_translate("MainWindow", "Center object", None))
        self.btnCenterPivot.setText(_translate("MainWindow", "2_CenterObj", None))
        self.btnPivottoOrigin.setToolTip(_translate("MainWindow", "Pivot to origin", None))
        self.btnPivottoOrigin.setText(_translate("MainWindow", "2_Origin", None))
        self.btnPivottoanotherObj.setToolTip(_translate("MainWindow", "Pivot to object", None))
        self.btnPivottoanotherObj.setText(_translate("MainWindow", "2_Object", None))
        self.btnFreezeTransform.setText(_translate("MainWindow", "Freeze Translation", None))
        self.btnZeroOffset.setText(_translate("MainWindow", "Zero_Offset", None))
        self.btnRotatePivot.setText(_translate("MainWindow", "Rotate Pivot", None))
        self.btnPivotOnFace.setText(_translate("MainWindow", "On faces", None))
        self.btnSetPivotAlongEdge.setText(_translate("MainWindow", "Along Edges", None))
        self.rdbXmid.setShortcut(_translate("MainWindow", "4, 8", None))

