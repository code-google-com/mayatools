# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\editshaders\widget\ui\editShaderUI.ui'
#
# Created: Sat Sep 13 15:45:56 2014
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
        MainWindow.resize(441, 215)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.cbbShadersScene = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbbShadersScene.sizePolicy().hasHeightForWidth())
        self.cbbShadersScene.setSizePolicy(sizePolicy)
        self.cbbShadersScene.setObjectName(_fromUtf8("cbbShadersScene"))
        self.horizontalLayout_2.addWidget(self.cbbShadersScene)
        self.chkAuto = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAuto.sizePolicy().hasHeightForWidth())
        self.chkAuto.setSizePolicy(sizePolicy)
        self.chkAuto.setCheckable(True)
        self.chkAuto.setChecked(True)
        self.chkAuto.setObjectName(_fromUtf8("chkAuto"))
        self.horizontalLayout_2.addWidget(self.chkAuto)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.btnGet = QtGui.QPushButton(self.groupBox)
        self.btnGet.setObjectName(_fromUtf8("btnGet"))
        self.horizontalLayout_3.addWidget(self.btnGet)
        self.btnAssignMat = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAssignMat.sizePolicy().hasHeightForWidth())
        self.btnAssignMat.setSizePolicy(sizePolicy)
        self.btnAssignMat.setObjectName(_fromUtf8("btnAssignMat"))
        self.horizontalLayout_3.addWidget(self.btnAssignMat)
        self.btnGetShader = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetShader.sizePolicy().hasHeightForWidth())
        self.btnGetShader.setSizePolicy(sizePolicy)
        self.btnGetShader.setObjectName(_fromUtf8("btnGetShader"))
        self.horizontalLayout_3.addWidget(self.btnGetShader)
        self.btnSelectShader = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectShader.sizePolicy().hasHeightForWidth())
        self.btnSelectShader.setSizePolicy(sizePolicy)
        self.btnSelectShader.setObjectName(_fromUtf8("btnSelectShader"))
        self.horizontalLayout_3.addWidget(self.btnSelectShader)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_2.setText(_translate("MainWindow", "Material", None))
        self.chkAuto.setText(_translate("MainWindow", "A", None))
        self.btnGet.setToolTip(_translate("MainWindow", "<html><head/><body><p>Chọn Shader được dùng bởi face được chọn.</p></body></html>", None))
        self.btnGet.setText(_translate("MainWindow", "Get", None))
        self.btnAssignMat.setToolTip(_translate("MainWindow", "<html><head/><body><p>Gán material cho faces được chọn. </p></body></html>", None))
        self.btnAssignMat.setText(_translate("MainWindow", "Set ", None))
        self.btnGetShader.setToolTip(_translate("MainWindow", "<html><head/><body><p>Chọn Face sử dụng Material trên mesh được chọn.</p><p>Nếu không có mesh được chọn, thì chọn trên toàn scene.</p></body></html>", None))
        self.btnGetShader.setText(_translate("MainWindow", "Select faces", None))
        self.btnSelectShader.setToolTip(_translate("MainWindow", "<html><head/><body><p>Tùy chỉnh shader được chọn.</p></body></html>", None))
        self.btnSelectShader.setText(_translate("MainWindow", "Select Shader", None))
        self.pushButton_2.setText(_translate("MainWindow", "Open Validate Shader", None))

