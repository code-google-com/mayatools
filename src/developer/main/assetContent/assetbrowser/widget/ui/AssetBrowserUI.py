# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\maya_Tools\src\developer\main\assetContent\assetbrowser\widget\ui\AssetBrowserUI.ui'
#
# Created: Tue Sep 23 16:12:58 2014
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
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1366, 863)
        MainWindow.setAcceptDrops(True)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setDocumentMode(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeViewPath = QtGui.QTreeView(self.splitter)
        self.treeViewPath.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeViewPath.sizePolicy().hasHeightForWidth())
        self.treeViewPath.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.treeViewPath.setFont(font)
        self.treeViewPath.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeViewPath.setAcceptDrops(True)
        self.treeViewPath.setAutoFillBackground(False)
        self.treeViewPath.setFrameShape(QtGui.QFrame.StyledPanel)
        self.treeViewPath.setFrameShadow(QtGui.QFrame.Raised)
        self.treeViewPath.setLineWidth(1)
        self.treeViewPath.setMidLineWidth(0)
        self.treeViewPath.setAutoScrollMargin(21)
        self.treeViewPath.setDragEnabled(True)
        self.treeViewPath.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeViewPath.setAlternatingRowColors(True)
        self.treeViewPath.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeViewPath.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.treeViewPath.setIconSize(QtCore.QSize(20, 20))
        self.treeViewPath.setUniformRowHeights(True)
        self.treeViewPath.setItemsExpandable(True)
        self.treeViewPath.setSortingEnabled(True)
        self.treeViewPath.setAnimated(True)
        self.treeViewPath.setWordWrap(True)
        self.treeViewPath.setHeaderHidden(True)
        self.treeViewPath.setObjectName(_fromUtf8("treeViewPath"))
        self.treeViewPath.header().setVisible(False)
        self.layoutWidget_2 = QtGui.QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnSearch = QtGui.QPushButton(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSearch.sizePolicy().hasHeightForWidth())
        self.btnSearch.setSizePolicy(sizePolicy)
        self.btnSearch.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/arrow-right.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearch.setIcon(icon)
        self.btnSearch.setFlat(True)
        self.btnSearch.setObjectName(_fromUtf8("btnSearch"))
        self.horizontalLayout.addWidget(self.btnSearch)
        self.ldtFilter = QtGui.QLineEdit(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ldtFilter.sizePolicy().hasHeightForWidth())
        self.ldtFilter.setSizePolicy(sizePolicy)
        self.ldtFilter.setObjectName(_fromUtf8("ldtFilter"))
        self.horizontalLayout.addWidget(self.ldtFilter)
        self.horizontalSlider = QtGui.QSlider(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tabWidget = QtGui.QTabWidget(self.layoutWidget_2)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_4.setMargin(3)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.vGraphicsLayout = QtGui.QVBoxLayout()
        self.vGraphicsLayout.setSpacing(3)
        self.vGraphicsLayout.setObjectName(_fromUtf8("vGraphicsLayout"))
        self.verticalLayout_4.addLayout(self.vGraphicsLayout)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.edtRootLocation = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtRootLocation.sizePolicy().hasHeightForWidth())
        self.edtRootLocation.setSizePolicy(sizePolicy)
        self.edtRootLocation.setStyleSheet(_fromUtf8("background-color: rgba(255, 255, 255, 0);"))
        self.edtRootLocation.setFrame(False)
        self.edtRootLocation.setReadOnly(True)
        self.edtRootLocation.setObjectName(_fromUtf8("edtRootLocation"))
        self.horizontalLayout_2.addWidget(self.edtRootLocation)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1366, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName(_fromUtf8("menuPreferences"))
        self.menuConnect_with_Source_Control = QtGui.QMenu(self.menuPreferences)
        self.menuConnect_with_Source_Control.setObjectName(_fromUtf8("menuConnect_with_Source_Control"))
        self.menuHelps = QtGui.QMenu(self.menubar)
        self.menuHelps.setObjectName(_fromUtf8("menuHelps"))
        self.menuViews = QtGui.QMenu(self.menubar)
        self.menuViews.setObjectName(_fromUtf8("menuViews"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuSend_to = QtGui.QMenu(self.menuEdit)
        self.menuSend_to.setObjectName(_fromUtf8("menuSend_to"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionPerforce = QtGui.QAction(MainWindow)
        self.actionPerforce.setObjectName(_fromUtf8("actionPerforce"))
        self.actionSVN = QtGui.QAction(MainWindow)
        self.actionSVN.setObjectName(_fromUtf8("actionSVN"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionOpen_selected_asset = QtGui.QAction(MainWindow)
        self.actionOpen_selected_asset.setObjectName(_fromUtf8("actionOpen_selected_asset"))
        self.actionMax = QtGui.QAction(MainWindow)
        self.actionMax.setObjectName(_fromUtf8("actionMax"))
        self.actionCapture_thumbnail = QtGui.QAction(MainWindow)
        self.actionCapture_thumbnail.setObjectName(_fromUtf8("actionCapture_thumbnail"))
        self.actionImport_selected_asset = QtGui.QAction(MainWindow)
        self.actionImport_selected_asset.setObjectName(_fromUtf8("actionImport_selected_asset"))
        self.actionChange_Color_theme = QtGui.QAction(MainWindow)
        self.actionChange_Color_theme.setObjectName(_fromUtf8("actionChange_Color_theme"))
        self.actionSign_out = QtGui.QAction(MainWindow)
        self.actionSign_out.setObjectName(_fromUtf8("actionSign_out"))
        self.actionImage_View = QtGui.QAction(MainWindow)
        self.actionImage_View.setObjectName(_fromUtf8("actionImage_View"))
        self.menuConnect_with_Source_Control.addAction(self.actionPerforce)
        self.menuConnect_with_Source_Control.addAction(self.actionSVN)
        self.menuPreferences.addAction(self.menuConnect_with_Source_Control.menuAction())
        self.menuPreferences.addAction(self.actionChange_Color_theme)
        self.menuHelps.addAction(self.actionAbout)
        self.menuViews.addAction(self.actionImage_View)
        self.menuSend_to.addAction(self.actionMax)
        self.menuEdit.addAction(self.actionOpen_selected_asset)
        self.menuEdit.addAction(self.menuSend_to.menuAction())
        self.menuEdit.addAction(self.actionCapture_thumbnail)
        self.menuEdit.addAction(self.actionImport_selected_asset)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuViews.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuHelps.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.treeViewPath, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), self.edtRootLocation.show)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Asset Browser", None))
        self.btnSearch.setText(_translate("MainWindow", "Filter Asset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Asset", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Mesh", None))
        self.menuPreferences.setTitle(_translate("MainWindow", "Preferences", None))
        self.menuConnect_with_Source_Control.setTitle(_translate("MainWindow", "Connect with Source Control", None))
        self.menuHelps.setTitle(_translate("MainWindow", "Helps", None))
        self.menuViews.setTitle(_translate("MainWindow", "Views", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Asset", None))
        self.menuSend_to.setTitle(_translate("MainWindow", "Export selected asset", None))
        self.actionPerforce.setText(_translate("MainWindow", "Perforce", None))
        self.actionSVN.setText(_translate("MainWindow", "SVN", None))
        self.actionOpen.setText(_translate("MainWindow", "Sign in", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionOpen_selected_asset.setText(_translate("MainWindow", "Open selected asset", None))
        self.actionMax.setText(_translate("MainWindow", "Max", None))
        self.actionCapture_thumbnail.setText(_translate("MainWindow", "Capture thumbnail...", None))
        self.actionImport_selected_asset.setText(_translate("MainWindow", "Import selected asset", None))
        self.actionChange_Color_theme.setText(_translate("MainWindow", "Change Color Theme", None))
        self.actionSign_out.setText(_translate("MainWindow", "Sign out", None))
        self.actionImage_View.setText(_translate("MainWindow", "Image View", None))

import developer.main.source.IconResource_rc
