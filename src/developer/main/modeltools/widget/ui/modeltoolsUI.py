# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\modeltools\widget\ui\modeltoolsUI.ui'
#
# Created: Wed Sep 17 15:13:02 2014
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
        MainWindow.resize(435, 198)
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
        self.verticalLayout_2.setContentsMargins(3, 3, 3, -1)
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
        self.line = QtGui.QFrame(self.groupBox_3)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
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
        self.line_2 = QtGui.QFrame(self.groupBox_3)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_2.addWidget(self.line_2)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.btnToSelected = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnToSelected.setFont(font)
        self.btnToSelected.setObjectName(_fromUtf8("btnToSelected"))
        self.horizontalLayout_15.addWidget(self.btnToSelected)
        self.btnToClosest = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnToClosest.setFont(font)
        self.btnToClosest.setObjectName(_fromUtf8("btnToClosest"))
        self.horizontalLayout_15.addWidget(self.btnToClosest)
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
        self.line_3 = QtGui.QFrame(self.groupBox_3)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_2.addWidget(self.line_3)
        self.btnCleanUp = QtGui.QPushButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.btnCleanUp.setFont(font)
        self.btnCleanUp.setObjectName(_fromUtf8("btnCleanUp"))
        self.verticalLayout_2.addWidget(self.btnCleanUp)
        self.verticalLayout.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnAttach.setToolTip(_translate("MainWindow", "<html><head/><body><p>Combine 2 mesh to single mesh and keep:</p><p>- Keep name of first selected mesh.</p><p>- Keep pivot\'s position of first selected mesh.</p><p>- Clean up result mesh. (deleted history + freeze transformation).</p></body></html>", None))
        self.btnAttach.setText(_translate("MainWindow", "Attach", None))
        self.btnDetach.setToolTip(_translate("MainWindow", "<html><head/><body><p>Detach selected faces to a separated mesh.</p></body></html>", None))
        self.btnDetach.setText(_translate("MainWindow", "Detach", None))
        self.btnDuplicate.setToolTip(_translate("MainWindow", "Clone selected faces to a single mesh.", None))
        self.btnDuplicate.setText(_translate("MainWindow", "Duplicate", None))
        self.pushButton.setToolTip(_translate("MainWindow", "Detach selected mesh to many separated meshes based on element.", None))
        self.pushButton.setText(_translate("MainWindow", "Detach By Element", None))
        self.pushButton_2.setToolTip(_translate("MainWindow", "Detach selected mesh base on materials.", None))
        self.pushButton_2.setText(_translate("MainWindow", "Detach By Material", None))
        self.btnSmartCollapse.setText(_translate("MainWindow", "Un-Chamfered", None))
        self.btnReplace.setText(_translate("MainWindow", "Edit Edge Flow", None))
        self.btnToSelected.setToolTip(_translate("MainWindow", "Snap Closest Vertexes to Selected Vertexes", None))
        self.btnToSelected.setText(_translate("MainWindow", "To Selected", None))
        self.btnToClosest.setToolTip(_translate("MainWindow", "Snap Selected Vertexes to Closest Vertexes ", None))
        self.btnToClosest.setText(_translate("MainWindow", "To Closest", None))
        self.btnSnapVertexTool.setToolTip(_translate("MainWindow", "Snap to Center of vertexes", None))
        self.btnSnapVertexTool.setText(_translate("MainWindow", "To Center", None))
        self.btnCleanUp.setText(_translate("MainWindow", "Clean up Mesh", None))

