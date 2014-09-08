# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\modeltools\widget\ui\modeltoolsUI.ui'
#
# Created: Sun Sep 07 21:01:33 2014
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
        MainWindow.resize(435, 171)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setTitle(_fromUtf8(""))
        self.groupBox_3.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnAttach = QtGui.QPushButton(self.groupBox_3)
        self.btnAttach.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnAttach.setFont(font)
        self.btnAttach.setObjectName(_fromUtf8("btnAttach"))
        self.horizontalLayout_2.addWidget(self.btnAttach)
        self.btnDetach = QtGui.QPushButton(self.groupBox_3)
        self.btnDetach.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnDetach.setFont(font)
        self.btnDetach.setObjectName(_fromUtf8("btnDetach"))
        self.horizontalLayout_2.addWidget(self.btnDetach)
        self.btnDuplicate = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnDuplicate.setFont(font)
        self.btnDuplicate.setObjectName(_fromUtf8("btnDuplicate"))
        self.horizontalLayout_2.addWidget(self.btnDuplicate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnSmartCollapse = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSmartCollapse.setFont(font)
        self.btnSmartCollapse.setObjectName(_fromUtf8("btnSmartCollapse"))
        self.horizontalLayout_3.addWidget(self.btnSmartCollapse)
        self.btnReplace = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnReplace.setFont(font)
        self.btnReplace.setObjectName(_fromUtf8("btnReplace"))
        self.horizontalLayout_3.addWidget(self.btnReplace)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.btnSnapVertexTool = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnSnapVertexTool.setFont(font)
        self.btnSnapVertexTool.setObjectName(_fromUtf8("btnSnapVertexTool"))
        self.horizontalLayout_15.addWidget(self.btnSnapVertexTool)
        self.spnTolerance = QtGui.QDoubleSpinBox(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spnTolerance.sizePolicy().hasHeightForWidth())
        self.spnTolerance.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.spnTolerance.setFont(font)
        self.spnTolerance.setMinimum(0.01)
        self.spnTolerance.setSingleStep(0.01)
        self.spnTolerance.setProperty("value", 0.01)
        self.spnTolerance.setObjectName(_fromUtf8("spnTolerance"))
        self.horizontalLayout_15.addWidget(self.spnTolerance)
        self.verticalLayout_2.addLayout(self.horizontalLayout_15)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnAttach.setText(_translate("MainWindow", "Attach", None))
        self.btnDetach.setText(_translate("MainWindow", "Detach", None))
        self.btnDuplicate.setText(_translate("MainWindow", "Duplicate", None))
        self.pushButton.setText(_translate("MainWindow", "Detach By Element", None))
        self.pushButton_2.setText(_translate("MainWindow", "Detach By Material", None))
        self.btnSmartCollapse.setText(_translate("MainWindow", "Un-Chamfered", None))
        self.btnReplace.setText(_translate("MainWindow", "Edit Edge Flow", None))
        self.btnSnapVertexTool.setText(_translate("MainWindow", "Snap Vertex Tool", None))

