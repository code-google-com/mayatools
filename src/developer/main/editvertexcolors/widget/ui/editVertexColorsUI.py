# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\editvertexcolors\widget\ui\editVertexColorsUI.ui'
#
# Created: Sat Sep 13 05:36:13 2014
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
        MainWindow.resize(587, 183)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_10.setMargin(3)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setMargin(3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout.addWidget(self.checkBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(9)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy)
        self.doubleSpinBox.setMinimum(-1.0)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.01)
        self.doubleSpinBox.setProperty("value", 0.01)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setStyleSheet(_fromUtf8("color: rgb(0, 255, 0);"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_2.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_2.setSizePolicy(sizePolicy)
        self.doubleSpinBox_2.setMinimum(-1.0)
        self.doubleSpinBox_2.setMaximum(1.0)
        self.doubleSpinBox_2.setSingleStep(0.01)
        self.doubleSpinBox_2.setProperty("value", 0.01)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBox_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setStyleSheet(_fromUtf8("color: rgb(85, 0, 255);"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_5.addWidget(self.label_3)
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_3.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_3.setSizePolicy(sizePolicy)
        self.doubleSpinBox_3.setMinimum(-1.0)
        self.doubleSpinBox_3.setMaximum(1.0)
        self.doubleSpinBox_3.setSingleStep(0.01)
        self.doubleSpinBox_3.setProperty("value", 0.01)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.horizontalLayout_5.addWidget(self.doubleSpinBox_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_4.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_4.setSizePolicy(sizePolicy)
        self.doubleSpinBox_4.setMinimum(-1.0)
        self.doubleSpinBox_4.setMaximum(1.0)
        self.doubleSpinBox_4.setSingleStep(0.01)
        self.doubleSpinBox_4.setProperty("value", 0.01)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.btnAddRed = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddRed.sizePolicy().hasHeightForWidth())
        self.btnAddRed.setSizePolicy(sizePolicy)
        self.btnAddRed.setStyleSheet(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/white, without circle/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAddRed.setIcon(icon)
        self.btnAddRed.setIconSize(QtCore.QSize(20, 20))
        self.btnAddRed.setObjectName(_fromUtf8("btnAddRed"))
        self.verticalLayout_6.addWidget(self.btnAddRed)
        self.btnAddGreen = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddGreen.sizePolicy().hasHeightForWidth())
        self.btnAddGreen.setSizePolicy(sizePolicy)
        self.btnAddGreen.setObjectName(_fromUtf8("btnAddGreen"))
        self.verticalLayout_6.addWidget(self.btnAddGreen)
        self.btnAddBlue = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddBlue.sizePolicy().hasHeightForWidth())
        self.btnAddBlue.setSizePolicy(sizePolicy)
        self.btnAddBlue.setObjectName(_fromUtf8("btnAddBlue"))
        self.verticalLayout_6.addWidget(self.btnAddBlue)
        self.btnAddAlpha = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddAlpha.sizePolicy().hasHeightForWidth())
        self.btnAddAlpha.setSizePolicy(sizePolicy)
        self.btnAddAlpha.setObjectName(_fromUtf8("btnAddAlpha"))
        self.verticalLayout_6.addWidget(self.btnAddAlpha)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.btnReplaceRed = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnReplaceRed.sizePolicy().hasHeightForWidth())
        self.btnReplaceRed.setSizePolicy(sizePolicy)
        self.btnReplaceRed.setStyleSheet(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/white, without circle/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnReplaceRed.setIcon(icon1)
        self.btnReplaceRed.setIconSize(QtCore.QSize(20, 20))
        self.btnReplaceRed.setObjectName(_fromUtf8("btnReplaceRed"))
        self.verticalLayout_7.addWidget(self.btnReplaceRed)
        self.btnReplaceGreen = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnReplaceGreen.sizePolicy().hasHeightForWidth())
        self.btnReplaceGreen.setSizePolicy(sizePolicy)
        self.btnReplaceGreen.setObjectName(_fromUtf8("btnReplaceGreen"))
        self.verticalLayout_7.addWidget(self.btnReplaceGreen)
        self.btnReplaceBlue = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnReplaceBlue.sizePolicy().hasHeightForWidth())
        self.btnReplaceBlue.setSizePolicy(sizePolicy)
        self.btnReplaceBlue.setObjectName(_fromUtf8("btnReplaceBlue"))
        self.verticalLayout_7.addWidget(self.btnReplaceBlue)
        self.btnReplaceAlpha = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnReplaceAlpha.sizePolicy().hasHeightForWidth())
        self.btnReplaceAlpha.setSizePolicy(sizePolicy)
        self.btnReplaceAlpha.setObjectName(_fromUtf8("btnReplaceAlpha"))
        self.verticalLayout_7.addWidget(self.btnReplaceAlpha)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.btnGetRed = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetRed.sizePolicy().hasHeightForWidth())
        self.btnGetRed.setSizePolicy(sizePolicy)
        self.btnGetRed.setObjectName(_fromUtf8("btnGetRed"))
        self.verticalLayout_8.addWidget(self.btnGetRed)
        self.btnGetGreen = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetGreen.sizePolicy().hasHeightForWidth())
        self.btnGetGreen.setSizePolicy(sizePolicy)
        self.btnGetGreen.setObjectName(_fromUtf8("btnGetGreen"))
        self.verticalLayout_8.addWidget(self.btnGetGreen)
        self.btnGetBlue = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetBlue.sizePolicy().hasHeightForWidth())
        self.btnGetBlue.setSizePolicy(sizePolicy)
        self.btnGetBlue.setObjectName(_fromUtf8("btnGetBlue"))
        self.verticalLayout_8.addWidget(self.btnGetBlue)
        self.btnGetAlpha = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetAlpha.sizePolicy().hasHeightForWidth())
        self.btnGetAlpha.setSizePolicy(sizePolicy)
        self.btnGetAlpha.setObjectName(_fromUtf8("btnGetAlpha"))
        self.verticalLayout_8.addWidget(self.btnGetAlpha)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.btnSetRed = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetRed.sizePolicy().hasHeightForWidth())
        self.btnSetRed.setSizePolicy(sizePolicy)
        self.btnSetRed.setObjectName(_fromUtf8("btnSetRed"))
        self.verticalLayout_9.addWidget(self.btnSetRed)
        self.btnSetGreen = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetGreen.sizePolicy().hasHeightForWidth())
        self.btnSetGreen.setSizePolicy(sizePolicy)
        self.btnSetGreen.setObjectName(_fromUtf8("btnSetGreen"))
        self.verticalLayout_9.addWidget(self.btnSetGreen)
        self.btnSetBlue = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetBlue.sizePolicy().hasHeightForWidth())
        self.btnSetBlue.setSizePolicy(sizePolicy)
        self.btnSetBlue.setObjectName(_fromUtf8("btnSetBlue"))
        self.verticalLayout_9.addWidget(self.btnSetBlue)
        self.btnSetAlpha = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetAlpha.sizePolicy().hasHeightForWidth())
        self.btnSetAlpha.setSizePolicy(sizePolicy)
        self.btnSetAlpha.setObjectName(_fromUtf8("btnSetAlpha"))
        self.verticalLayout_9.addWidget(self.btnSetAlpha)
        self.horizontalLayout_2.addLayout(self.verticalLayout_9)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setSpacing(3)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.pushButton_5 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.verticalLayout_11.addWidget(self.pushButton_5)
        self.pushButton_6 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.verticalLayout_11.addWidget(self.pushButton_6)
        self.pushButton_7 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.verticalLayout_11.addWidget(self.pushButton_7)
        self.pushButton_8 = QtGui.QPushButton(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.verticalLayout_11.addWidget(self.pushButton_8)
        self.horizontalLayout_2.addLayout(self.verticalLayout_11)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_10.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.checkBox.setText(_translate("MainWindow", "Apply for RGB", None))
        self.label.setText(_translate("MainWindow", "X", None))
        self.label_2.setText(_translate("MainWindow", "Y", None))
        self.label_3.setText(_translate("MainWindow", "Z", None))
        self.label_4.setText(_translate("MainWindow", "A", None))
        self.btnAddRed.setToolTip(_translate("MainWindow", "Thêm", None))
        self.btnAddRed.setText(_translate("MainWindow", "Add", None))
        self.btnAddGreen.setText(_translate("MainWindow", "Add", None))
        self.btnAddBlue.setText(_translate("MainWindow", "Add", None))
        self.btnAddAlpha.setText(_translate("MainWindow", "Add", None))
        self.btnReplaceRed.setText(_translate("MainWindow", "Rep", None))
        self.btnReplaceGreen.setText(_translate("MainWindow", "Rep", None))
        self.btnReplaceBlue.setText(_translate("MainWindow", "Rep", None))
        self.btnReplaceAlpha.setText(_translate("MainWindow", "Rep", None))
        self.btnGetRed.setText(_translate("MainWindow", "Get", None))
        self.btnGetGreen.setText(_translate("MainWindow", "Get", None))
        self.btnGetBlue.setText(_translate("MainWindow", "Get", None))
        self.btnGetAlpha.setText(_translate("MainWindow", "Get", None))
        self.btnSetRed.setText(_translate("MainWindow", "Set", None))
        self.btnSetGreen.setText(_translate("MainWindow", "Set", None))
        self.btnSetBlue.setText(_translate("MainWindow", "Set", None))
        self.btnSetAlpha.setText(_translate("MainWindow", "Set", None))
        self.pushButton_5.setText(_translate("MainWindow", "Heal", None))
        self.pushButton_6.setText(_translate("MainWindow", "Heal", None))
        self.pushButton_7.setText(_translate("MainWindow", "Heal", None))
        self.pushButton_8.setText(_translate("MainWindow", "Heal", None))

import developer.main.source.IconResource_rc
