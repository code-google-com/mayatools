# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\setupdisplay\setupscene\ui\setupscene.ui'
#
# Created: Sun Jun 29 06:16:57 2014
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(330, 123)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_5 = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_6.setContentsMargins(5, -1, 5, -1)
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
        self.btnSetNormalSize.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/normal_off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSetNormalSize.setIcon(icon2)
        self.btnSetNormalSize.setIconSize(QtCore.QSize(50, 50))
        self.btnSetNormalSize.setFlat(True)
        self.btnSetNormalSize.setObjectName(_fromUtf8("btnSetNormalSize"))
        self.horizontalLayout_7.addWidget(self.btnSetNormalSize)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_7)
        spacerItem = QtGui.QSpacerItem(143, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.verticalLayout.addWidget(self.groupBox_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox_5.setTitle(_translate("Form", "Set up Display Scene:", None))
        self.btnSetupAxis.setToolTip(_translate("Form", "change Axis", None))

