# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\mirrortools\widget\ui\mirrorUI.ui'
#
# Created: Sat Oct 11 09:23:38 2014
#      by: PyQt4 UI code generator 4.10.4
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
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(631, 224)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(3, 3, 3, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setChecked(False)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(7)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setMargin(3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.rdbNoClone = QtGui.QRadioButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbNoClone.setFont(font)
        self.rdbNoClone.setChecked(False)
        self.rdbNoClone.setObjectName(_fromUtf8("rdbNoClone"))
        self.horizontalLayout_11.addWidget(self.rdbNoClone)
        self.rdbClone = QtGui.QRadioButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbClone.setFont(font)
        self.rdbClone.setChecked(True)
        self.rdbClone.setObjectName(_fromUtf8("rdbClone"))
        self.horizontalLayout_11.addWidget(self.rdbClone)
        self.rdbInstance = QtGui.QRadioButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbInstance.setFont(font)
        self.rdbInstance.setObjectName(_fromUtf8("rdbInstance"))
        self.horizontalLayout_11.addWidget(self.rdbInstance)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.rdbKeepHistory = QtGui.QRadioButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbKeepHistory.setFont(font)
        self.rdbKeepHistory.setChecked(False)
        self.rdbKeepHistory.setObjectName(_fromUtf8("rdbKeepHistory"))
        self.horizontalLayout_18.addWidget(self.rdbKeepHistory)
        self.rdbParentOnly = QtGui.QRadioButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.rdbParentOnly.setFont(font)
        self.rdbParentOnly.setObjectName(_fromUtf8("rdbParentOnly"))
        self.horizontalLayout_18.addWidget(self.rdbParentOnly)
        self.verticalLayout_3.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.btnMirrorU = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMirrorU.sizePolicy().hasHeightForWidth())
        self.btnMirrorU.setSizePolicy(sizePolicy)
        self.btnMirrorU.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);"))
        self.btnMirrorU.setCheckable(True)
        self.btnMirrorU.setObjectName(_fromUtf8("btnMirrorU"))
        self.horizontalLayout_12.addWidget(self.btnMirrorU)
        self.btnAxisX = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAxisX.sizePolicy().hasHeightForWidth())
        self.btnAxisX.setSizePolicy(sizePolicy)
        self.btnAxisX.setObjectName(_fromUtf8("btnAxisX"))
        self.horizontalLayout_12.addWidget(self.btnAxisX)
        self.btnPivotX = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPivotX.sizePolicy().hasHeightForWidth())
        self.btnPivotX.setSizePolicy(sizePolicy)
        self.btnPivotX.setObjectName(_fromUtf8("btnPivotX"))
        self.horizontalLayout_12.addWidget(self.btnPivotX)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setStyleSheet(_fromUtf8("background-color: rgb(0, 255, 0);\n"
"color: rgb(255, 255, 255);"))
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_13.addWidget(self.pushButton)
        self.btnAxisY = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAxisY.sizePolicy().hasHeightForWidth())
        self.btnAxisY.setSizePolicy(sizePolicy)
        self.btnAxisY.setObjectName(_fromUtf8("btnAxisY"))
        self.horizontalLayout_13.addWidget(self.btnAxisY)
        self.btnPivotY = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPivotY.sizePolicy().hasHeightForWidth())
        self.btnPivotY.setSizePolicy(sizePolicy)
        self.btnPivotY.setObjectName(_fromUtf8("btnPivotY"))
        self.horizontalLayout_13.addWidget(self.btnPivotY)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnMirrorV = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMirrorV.sizePolicy().hasHeightForWidth())
        self.btnMirrorV.setSizePolicy(sizePolicy)
        self.btnMirrorV.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);\n"
"color: rgb(255, 255, 255);"))
        self.btnMirrorV.setCheckable(True)
        self.btnMirrorV.setObjectName(_fromUtf8("btnMirrorV"))
        self.horizontalLayout_2.addWidget(self.btnMirrorV)
        self.btnAxisZ = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAxisZ.sizePolicy().hasHeightForWidth())
        self.btnAxisZ.setSizePolicy(sizePolicy)
        self.btnAxisZ.setObjectName(_fromUtf8("btnAxisZ"))
        self.horizontalLayout_2.addWidget(self.btnAxisZ)
        self.btnPivotZ = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPivotZ.sizePolicy().hasHeightForWidth())
        self.btnPivotZ.setSizePolicy(sizePolicy)
        self.btnPivotZ.setObjectName(_fromUtf8("btnPivotZ"))
        self.horizontalLayout_2.addWidget(self.btnPivotZ)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.rdbNoClone.setText(_translate("MainWindow", "No Copy", None))
        self.rdbClone.setText(_translate("MainWindow", "Clone", None))
        self.rdbInstance.setText(_translate("MainWindow", "Instance", None))
        self.rdbKeepHistory.setToolTip(_translate("MainWindow", "Mirror selected mesh with history intact", None))
        self.rdbKeepHistory.setText(_translate("MainWindow", "Keep History", None))
        self.rdbParentOnly.setText(_translate("MainWindow", "Parent Only", None))
        self.btnMirrorU.setText(_translate("MainWindow", "X", None))
        self.btnAxisX.setToolTip(_translate("MainWindow", "Mirror selected mesh by axis", None))
        self.btnAxisX.setText(_translate("MainWindow", "By Axis", None))
        self.btnPivotX.setToolTip(_translate("MainWindow", "Mirror selected mesh by pivot", None))
        self.btnPivotX.setText(_translate("MainWindow", "By Pivot", None))
        self.pushButton.setText(_translate("MainWindow", "Y", None))
        self.btnAxisY.setToolTip(_translate("MainWindow", "Mirror selected mesh by pivot", None))
        self.btnAxisY.setText(_translate("MainWindow", "By Axis", None))
        self.btnPivotY.setToolTip(_translate("MainWindow", "Mirror selected mesh by axis", None))
        self.btnPivotY.setText(_translate("MainWindow", "By Pivot", None))
        self.btnMirrorV.setText(_translate("MainWindow", "Z", None))
        self.btnAxisZ.setToolTip(_translate("MainWindow", "Mirror selected mesh by axis", None))
        self.btnAxisZ.setText(_translate("MainWindow", "By Axis", None))
        self.btnPivotZ.setToolTip(_translate("MainWindow", "Mirror selected mesh by pivot", None))
        self.btnPivotZ.setText(_translate("MainWindow", "By Pivot", None))

