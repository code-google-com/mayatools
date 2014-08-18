# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\nametools\widget\ui\basicnameUI.ui'
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
        MainWindow.resize(387, 223)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(3, 1, 3, 1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.edtNameStr = QtGui.QLineEdit(self.groupBox)
        self.edtNameStr.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.edtNameStr.setObjectName(_fromUtf8("edtNameStr"))
        self.horizontalLayout_5.addWidget(self.edtNameStr)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_7.addWidget(self.label_3)
        self.edtNamePrefix = QtGui.QLineEdit(self.groupBox)
        self.edtNamePrefix.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 3px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.edtNamePrefix.setObjectName(_fromUtf8("edtNamePrefix"))
        self.horizontalLayout_7.addWidget(self.edtNamePrefix)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_8.addWidget(self.label_5)
        self.edtNameSuffix = QtGui.QLineEdit(self.groupBox)
        self.edtNameSuffix.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.edtNameSuffix.setObjectName(_fromUtf8("edtNameSuffix"))
        self.horizontalLayout_8.addWidget(self.edtNameSuffix)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.ldtFind = QtGui.QLineEdit(self.groupBox)
        self.ldtFind.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.ldtFind.setObjectName(_fromUtf8("ldtFind"))
        self.horizontalLayout_3.addWidget(self.ldtFind)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_10.addWidget(self.label_6)
        self.edtSelectByName = QtGui.QLineEdit(self.groupBox)
        self.edtSelectByName.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.edtSelectByName.setObjectName(_fromUtf8("edtSelectByName"))
        self.horizontalLayout_10.addWidget(self.edtSelectByName)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.edtReplaceStr = QtGui.QLineEdit(self.groupBox)
        self.edtReplaceStr.setStyleSheet(_fromUtf8("QLineEdit {\n"
"padding: 4px;\n"
"border-style: solid;\n"
"border: 1px solid gray;\n"
"border-radius: 10px;\n"
"font:  bold 11px\n"
"}"))
        self.edtReplaceStr.setObjectName(_fromUtf8("edtReplaceStr"))
        self.horizontalLayout.addWidget(self.edtReplaceStr)
        self.chkHierrachy = QtGui.QCheckBox(self.groupBox)
        self.chkHierrachy.setText(_fromUtf8(""))
        self.chkHierrachy.setObjectName(_fromUtf8("chkHierrachy"))
        self.horizontalLayout.addWidget(self.chkHierrachy)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnUpperCase = QtGui.QPushButton(self.groupBox)
        self.btnUpperCase.setObjectName(_fromUtf8("btnUpperCase"))
        self.horizontalLayout_2.addWidget(self.btnUpperCase)
        self.btnUpper1stLetter = QtGui.QPushButton(self.groupBox)
        self.btnUpper1stLetter.setObjectName(_fromUtf8("btnUpper1stLetter"))
        self.horizontalLayout_2.addWidget(self.btnUpper1stLetter)
        self.btnLowerCase = QtGui.QPushButton(self.groupBox)
        self.btnLowerCase.setObjectName(_fromUtf8("btnLowerCase"))
        self.horizontalLayout_2.addWidget(self.btnLowerCase)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Rename", None))
        self.label_3.setText(_translate("MainWindow", "Prefix", None))
        self.label_5.setText(_translate("MainWindow", "Suffix", None))
        self.label.setText(_translate("MainWindow", "Find", None))
        self.label_6.setText(_translate("MainWindow", "Select By Name", None))
        self.label_4.setText(_translate("MainWindow", "Replace By:", None))
        self.chkHierrachy.setToolTip(_translate("MainWindow", "apply to whole Hierrachy", None))
        self.btnUpperCase.setText(_translate("MainWindow", "UpperCase", None))
        self.btnUpper1stLetter.setText(_translate("MainWindow", "Upper1stLetter", None))
        self.btnLowerCase.setText(_translate("MainWindow", "LowerCase", None))

