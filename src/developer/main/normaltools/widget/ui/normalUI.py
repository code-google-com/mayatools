# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\normaltools\widget\ui\normalUI.ui'
#
# Created: Mon Aug 18 23:20:22 2014
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
        MainWindow.resize(716, 308)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setMargin(3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.btnLockToLargeFace = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnLockToLargeFace.setFont(font)
        self.btnLockToLargeFace.setObjectName(_fromUtf8("btnLockToLargeFace"))
        self.horizontalLayout_14.addWidget(self.btnLockToLargeFace)
        self.btnLockToSmallFace = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnLockToSmallFace.setFont(font)
        self.btnLockToSmallFace.setObjectName(_fromUtf8("btnLockToSmallFace"))
        self.horizontalLayout_14.addWidget(self.btnLockToSmallFace)
        self.btnUnlock = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnUnlock.setFont(font)
        self.btnUnlock.setObjectName(_fromUtf8("btnUnlock"))
        self.horizontalLayout_14.addWidget(self.btnUnlock)
        self.verticalLayout_5.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.btnCopyNormal = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnCopyNormal.setFont(font)
        self.btnCopyNormal.setObjectName(_fromUtf8("btnCopyNormal"))
        self.horizontalLayout_12.addWidget(self.btnCopyNormal)
        self.btnCopyAverageNormal = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnCopyAverageNormal.setFont(font)
        self.btnCopyAverageNormal.setObjectName(_fromUtf8("btnCopyAverageNormal"))
        self.horizontalLayout_12.addWidget(self.btnCopyAverageNormal)
        self.btnPasteNormal = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnPasteNormal.setFont(font)
        self.btnPasteNormal.setObjectName(_fromUtf8("btnPasteNormal"))
        self.horizontalLayout_12.addWidget(self.btnPasteNormal)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.btnSmoothBevel = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSmoothBevel.setFont(font)
        self.btnSmoothBevel.setObjectName(_fromUtf8("btnSmoothBevel"))
        self.verticalLayout_5.addWidget(self.btnSmoothBevel)
        self.btnmatchSeamNormal = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnmatchSeamNormal.setFont(font)
        self.btnmatchSeamNormal.setObjectName(_fromUtf8("btnmatchSeamNormal"))
        self.verticalLayout_5.addWidget(self.btnmatchSeamNormal)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.btnMirrorTools = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnMirrorTools.setFont(font)
        self.btnMirrorTools.setObjectName(_fromUtf8("btnMirrorTools"))
        self.horizontalLayout_16.addWidget(self.btnMirrorTools)
        self.radioButton_4 = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.horizontalLayout_16.addWidget(self.radioButton_4)
        self.radioButton_5 = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_5.setObjectName(_fromUtf8("radioButton_5"))
        self.horizontalLayout_16.addWidget(self.radioButton_5)
        self.radioButton_6 = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_6.setObjectName(_fromUtf8("radioButton_6"))
        self.horizontalLayout_16.addWidget(self.radioButton_6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.btnSmoothAdjacentEdges = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSmoothAdjacentEdges.setFont(font)
        self.btnSmoothAdjacentEdges.setObjectName(_fromUtf8("btnSmoothAdjacentEdges"))
        self.horizontalLayout_13.addWidget(self.btnSmoothAdjacentEdges)
        self.spnSmoothEdges = QtGui.QDoubleSpinBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spnSmoothEdges.sizePolicy().hasHeightForWidth())
        self.spnSmoothEdges.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spnSmoothEdges.setFont(font)
        self.spnSmoothEdges.setMinimum(0.01)
        self.spnSmoothEdges.setSingleStep(0.01)
        self.spnSmoothEdges.setProperty("value", 0.01)
        self.spnSmoothEdges.setObjectName(_fromUtf8("spnSmoothEdges"))
        self.horizontalLayout_13.addWidget(self.spnSmoothEdges)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        self.btnTransferNormalWithoutDetachMesh = QtGui.QPushButton(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnTransferNormalWithoutDetachMesh.setFont(font)
        self.btnTransferNormalWithoutDetachMesh.setObjectName(_fromUtf8("btnTransferNormalWithoutDetachMesh"))
        self.verticalLayout_5.addWidget(self.btnTransferNormalWithoutDetachMesh)
        self.verticalLayout.addWidget(self.groupBox_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnLockToLargeFace.setToolTip(_translate("MainWindow", "lock normal toward the large bevel faces", None))
        self.btnLockToLargeFace.setText(_translate("MainWindow", "Lock Large face", None))
        self.btnLockToSmallFace.setToolTip(_translate("MainWindow", "lock normal toward the small bevel faces", None))
        self.btnLockToSmallFace.setText(_translate("MainWindow", "Lock Small face", None))
        self.btnUnlock.setToolTip(_translate("MainWindow", "unlock selected vertexes normal", None))
        self.btnUnlock.setText(_translate("MainWindow", "Lock Unlocked", None))
        self.btnCopyNormal.setText(_translate("MainWindow", "Copy Normal", None))
        self.btnCopyAverageNormal.setText(_translate("MainWindow", "Copy Avg Normal", None))
        self.btnPasteNormal.setText(_translate("MainWindow", "Paste Normal", None))
        self.btnSmoothBevel.setText(_translate("MainWindow", "Smooth Beveled faces", None))
        self.btnmatchSeamNormal.setText(_translate("MainWindow", "Match seam normal", None))
        self.btnMirrorTools.setText(_translate("MainWindow", "Mirror Normal Tool", None))
        self.radioButton_4.setText(_translate("MainWindow", "X", None))
        self.radioButton_5.setText(_translate("MainWindow", "Y", None))
        self.radioButton_6.setText(_translate("MainWindow", "Z", None))
        self.btnSmoothAdjacentEdges.setText(_translate("MainWindow", "Smooth adjcent edges", None))
        self.btnTransferNormalWithoutDetachMesh.setText(_translate("MainWindow", "Transfer Normal without Detach mesh", None))

