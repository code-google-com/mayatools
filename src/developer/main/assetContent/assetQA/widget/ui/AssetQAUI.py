# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\assetContent\assetQA\widget\ui\AssetQAUI.ui'
#
# Created: Sat Oct 11 19:19:29 2014
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
        MainWindow.resize(1018, 670)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget_2 = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_2.setStyleSheet(_fromUtf8(""))
        self.tabWidget_2.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget_2.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget_2.setDocumentMode(True)
        self.tabWidget_2.setMovable(True)
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.txtFileInfo = QtGui.QTextBrowser(self.tab_3)
        self.txtFileInfo.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0.523, y1:0.119, x2:0.523, y2:0.87, stop:0 rgba(66, 96, 122, 255), stop:1 rgba(3, 65, 99, 255));\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(:/images/strip.png);"))
        self.txtFileInfo.setObjectName(_fromUtf8("txtFileInfo"))
        self.verticalLayout_5.addWidget(self.txtFileInfo)
        self.tabWidget_2.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.splitter_3 = QtGui.QSplitter(self.tab_4)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
        self.tableQAResult = QtGui.QTableView(self.splitter_3)
        self.tableQAResult.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0.523, y1:0.119, x2:0.523, y2:0.87, stop:0 rgba(66, 96, 122, 255), stop:1 rgba(3, 65, 99, 255));\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(:/images/strip.png);"))
        self.tableQAResult.setAlternatingRowColors(True)
        self.tableQAResult.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.tableQAResult.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.tableQAResult.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.tableQAResult.setGridStyle(QtCore.Qt.SolidLine)
        self.tableQAResult.setSortingEnabled(True)
        self.tableQAResult.setObjectName(_fromUtf8("tableQAResult"))
        self.tableQAResult.verticalHeader().setVisible(False)
        self.verticalLayout_6.addWidget(self.splitter_3)
        self.tabWidget_2.addTab(self.tab_4, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_5)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.splitter_2 = QtGui.QSplitter(self.tab_5)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.formLayoutWidget = QtGui.QWidget(self.splitter_2)
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.formLayoutWidget_2 = QtGui.QWidget(self.splitter_2)
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setMargin(0)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.verticalLayout_7.addWidget(self.splitter_2)
        self.tabWidget_2.addTab(self.tab_5, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.tab_6)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.splitter_4 = QtGui.QSplitter(self.tab_6)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName(_fromUtf8("splitter_4"))
        self.formLayoutWidget_3 = QtGui.QWidget(self.splitter_4)
        self.formLayoutWidget_3.setObjectName(_fromUtf8("formLayoutWidget_3"))
        self.formLayout_6 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_6.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.formLayout_6.setMargin(0)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.formLayoutWidget_4 = QtGui.QWidget(self.splitter_4)
        self.formLayoutWidget_4.setObjectName(_fromUtf8("formLayoutWidget_4"))
        self.formLayout_7 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_7.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_7.setMargin(0)
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.listWidget = QtGui.QListWidget(self.formLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setStyleSheet(_fromUtf8("background-color: qlineargradient(spread:pad, x1:0.523, y1:0.119, x2:0.523, y2:0.87, stop:0 rgba(66, 96, 122, 255), stop:1 rgba(3, 65, 99, 255));\n"
"color: rgb(255, 255, 255);\n"
"background-image: url(:/images/strip.png);"))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.SpanningRole, self.listWidget)
        self.verticalLayout_8.addWidget(self.splitter_4)
        self.tabWidget_2.addTab(self.tab_6, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1018, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuQA_Checks = QtGui.QMenu(self.menubar)
        self.menuQA_Checks.setObjectName(_fromUtf8("menuQA_Checks"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_QA_checks = QtGui.QAction(MainWindow)
        self.actionLoad_QA_checks.setObjectName(_fromUtf8("actionLoad_QA_checks"))
        self.actionEdit_QA_checks = QtGui.QAction(MainWindow)
        self.actionEdit_QA_checks.setObjectName(_fromUtf8("actionEdit_QA_checks"))
        self.menuQA_Checks.addAction(self.actionLoad_QA_checks)
        self.menuQA_Checks.addAction(self.actionEdit_QA_checks)
        self.menubar.addAction(self.menuQA_Checks.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Scene Information", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Geometry", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("MainWindow", "Textures", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("MainWindow", "Shaders", None))
        self.menuQA_Checks.setTitle(_translate("MainWindow", "QA Checks", None))
        self.actionLoad_QA_checks.setText(_translate("MainWindow", "Load QA checks", None))
        self.actionEdit_QA_checks.setText(_translate("MainWindow", "Edit QA checks", None))

