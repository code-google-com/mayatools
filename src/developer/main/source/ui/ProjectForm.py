# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\ge_Tools\src\developer\main\source\ui\ProjectForm.ui'
#
# Created: Thu Sep 18 10:47:12 2014
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

class Ui_ProjectMainForm(object):
    def setupUi(self, ProjectMainForm):
        ProjectMainForm.setObjectName(_fromUtf8("ProjectMainForm"))
        ProjectMainForm.setWindowModality(QtCore.Qt.NonModal)
        ProjectMainForm.resize(383, 948)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(8)
        sizePolicy.setHeightForWidth(ProjectMainForm.sizePolicy().hasHeightForWidth())
        ProjectMainForm.setSizePolicy(sizePolicy)
        ProjectMainForm.setWindowTitle(_fromUtf8(""))
        ProjectMainForm.setAutoFillBackground(False)
        ProjectMainForm.setStyleSheet(_fromUtf8(""))
        ProjectMainForm.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        ProjectMainForm.setAnimated(True)
        ProjectMainForm.setDocumentMode(True)
        ProjectMainForm.setTabShape(QtGui.QTabWidget.Triangular)
        ProjectMainForm.setDockNestingEnabled(False)
        ProjectMainForm.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(ProjectMainForm)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setAcceptDrops(True)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.Vietnamese, QtCore.QLocale.VietNam))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout_3.addWidget(self.tabWidget)
        ProjectMainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ProjectMainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 383, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAssets = QtGui.QMenu(self.menubar)
        self.menuAssets.setObjectName(_fromUtf8("menuAssets"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuIntegrate_with_Source_Control = QtGui.QMenu(self.menuHelp)
        self.menuIntegrate_with_Source_Control.setGeometry(QtCore.QRect(915, 193, 248, 222))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Exchange.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuIntegrate_with_Source_Control.setIcon(icon)
        self.menuIntegrate_with_Source_Control.setObjectName(_fromUtf8("menuIntegrate_with_Source_Control"))
        self.menuConnect_to_Source_Control = QtGui.QMenu(self.menuIntegrate_with_Source_Control)
        self.menuConnect_to_Source_Control.setObjectName(_fromUtf8("menuConnect_to_Source_Control"))
        self.menuCheck_out = QtGui.QMenu(self.menuIntegrate_with_Source_Control)
        self.menuCheck_out.setObjectName(_fromUtf8("menuCheck_out"))
        self.menuDocking = QtGui.QMenu(self.menuHelp)
        self.menuDocking.setObjectName(_fromUtf8("menuDocking"))
        self.menuHelp_2 = QtGui.QMenu(self.menubar)
        self.menuHelp_2.setObjectName(_fromUtf8("menuHelp_2"))
        self.menuProjects = QtGui.QMenu(self.menubar)
        self.menuProjects.setObjectName(_fromUtf8("menuProjects"))
        ProjectMainForm.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ProjectMainForm)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ProjectMainForm.setStatusBar(self.statusbar)
        self.actionImport_Asset = QtGui.QAction(ProjectMainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImport_Asset.setIcon(icon1)
        self.actionImport_Asset.setObjectName(_fromUtf8("actionImport_Asset"))
        self.actionRemove_Items = QtGui.QAction(ProjectMainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemove_Items.setIcon(icon2)
        self.actionRemove_Items.setObjectName(_fromUtf8("actionRemove_Items"))
        self.actionCreate_Workflow = QtGui.QAction(ProjectMainForm)
        self.actionCreate_Workflow.setIcon(icon1)
        self.actionCreate_Workflow.setObjectName(_fromUtf8("actionCreate_Workflow"))
        self.actionEdit = QtGui.QAction(ProjectMainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit.setIcon(icon3)
        self.actionEdit.setObjectName(_fromUtf8("actionEdit"))
        self.actionChange = QtGui.QAction(ProjectMainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionChange.setIcon(icon4)
        self.actionChange.setObjectName(_fromUtf8("actionChange"))
        self.actionTo_Left = QtGui.QAction(ProjectMainForm)
        self.actionTo_Left.setObjectName(_fromUtf8("actionTo_Left"))
        self.actionTo_Right = QtGui.QAction(ProjectMainForm)
        self.actionTo_Right.setObjectName(_fromUtf8("actionTo_Right"))
        self.actionQA = QtGui.QAction(ProjectMainForm)
        self.actionQA.setIcon(icon3)
        self.actionQA.setObjectName(_fromUtf8("actionQA"))
        self.actionUpdatedProject = QtGui.QAction(ProjectMainForm)
        self.actionUpdatedProject.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Check.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUpdatedProject.setIcon(icon5)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI"))
        font.setPointSize(9)
        self.actionUpdatedProject.setFont(font)
        self.actionUpdatedProject.setObjectName(_fromUtf8("actionUpdatedProject"))
        self.actionSettings_2 = QtGui.QAction(ProjectMainForm)
        self.actionSettings_2.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/cryControlPanel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings_2.setIcon(icon6)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Segoe UI"))
        font.setPointSize(9)
        self.actionSettings_2.setFont(font)
        self.actionSettings_2.setObjectName(_fromUtf8("actionSettings_2"))
        self.actionAdd = QtGui.QAction(ProjectMainForm)
        self.actionAdd.setIcon(icon1)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.actionRevert = QtGui.QAction(ProjectMainForm)
        self.actionRevert.setIcon(icon4)
        self.actionRevert.setObjectName(_fromUtf8("actionRevert"))
        self.actionDelete = QtGui.QAction(ProjectMainForm)
        self.actionDelete.setIcon(icon2)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionSettings = QtGui.QAction(ProjectMainForm)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionUpdate_tools = QtGui.QAction(ProjectMainForm)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/Import.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUpdate_tools.setIcon(icon7)
        self.actionUpdate_tools.setObjectName(_fromUtf8("actionUpdate_tools"))
        self.actionAbouts = QtGui.QAction(ProjectMainForm)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/Project/About.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbouts.setIcon(icon8)
        self.actionAbouts.setObjectName(_fromUtf8("actionAbouts"))
        self.actionAbout_2 = QtGui.QAction(ProjectMainForm)
        self.actionAbout_2.setIcon(icon8)
        self.actionAbout_2.setObjectName(_fromUtf8("actionAbout_2"))
        self.actionGuildlines = QtGui.QAction(ProjectMainForm)
        self.actionGuildlines.setObjectName(_fromUtf8("actionGuildlines"))
        self.actionPerforce = QtGui.QAction(ProjectMainForm)
        self.actionPerforce.setObjectName(_fromUtf8("actionPerforce"))
        self.actionSVN = QtGui.QAction(ProjectMainForm)
        self.actionSVN.setObjectName(_fromUtf8("actionSVN"))
        self.actionGet_latest_version = QtGui.QAction(ProjectMainForm)
        self.actionGet_latest_version.setObjectName(_fromUtf8("actionGet_latest_version"))
        self.actionSubmit = QtGui.QAction(ProjectMainForm)
        self.actionSubmit.setObjectName(_fromUtf8("actionSubmit"))
        self.actionRevert_2 = QtGui.QAction(ProjectMainForm)
        self.actionRevert_2.setObjectName(_fromUtf8("actionRevert_2"))
        self.actionAdd_to_Existing_Changelist = QtGui.QAction(ProjectMainForm)
        self.actionAdd_to_Existing_Changelist.setObjectName(_fromUtf8("actionAdd_to_Existing_Changelist"))
        self.actionAdd_to_new_changelist = QtGui.QAction(ProjectMainForm)
        self.actionAdd_to_new_changelist.setObjectName(_fromUtf8("actionAdd_to_new_changelist"))
        self.actionShow_History = QtGui.QAction(ProjectMainForm)
        self.actionShow_History.setObjectName(_fromUtf8("actionShow_History"))
        self.actionGet_revision = QtGui.QAction(ProjectMainForm)
        self.actionGet_revision.setObjectName(_fromUtf8("actionGet_revision"))
        self.actionLeft = QtGui.QAction(ProjectMainForm)
        self.actionLeft.setObjectName(_fromUtf8("actionLeft"))
        self.actionRight = QtGui.QAction(ProjectMainForm)
        self.actionRight.setObjectName(_fromUtf8("actionRight"))
        self.actionNew_Project = QtGui.QAction(ProjectMainForm)
        self.actionNew_Project.setObjectName(_fromUtf8("actionNew_Project"))
        self.actionEdit_Project = QtGui.QAction(ProjectMainForm)
        self.actionEdit_Project.setObjectName(_fromUtf8("actionEdit_Project"))
        self.actionAssetQA = QtGui.QAction(ProjectMainForm)
        self.actionAssetQA.setObjectName(_fromUtf8("actionAssetQA"))
        self.actionAssetTracking = QtGui.QAction(ProjectMainForm)
        self.actionAssetTracking.setObjectName(_fromUtf8("actionAssetTracking"))
        self.actionAssetBrowser = QtGui.QAction(ProjectMainForm)
        self.actionAssetBrowser.setObjectName(_fromUtf8("actionAssetBrowser"))
        self.menuAssets.addAction(self.actionAssetQA)
        self.menuAssets.addAction(self.actionAssetTracking)
        self.menuAssets.addAction(self.actionAssetBrowser)
        self.menuConnect_to_Source_Control.addAction(self.actionPerforce)
        self.menuConnect_to_Source_Control.addAction(self.actionSVN)
        self.menuCheck_out.addAction(self.actionAdd_to_Existing_Changelist)
        self.menuCheck_out.addAction(self.actionAdd_to_new_changelist)
        self.menuIntegrate_with_Source_Control.addAction(self.actionGet_latest_version)
        self.menuIntegrate_with_Source_Control.addAction(self.actionGet_revision)
        self.menuIntegrate_with_Source_Control.addAction(self.menuCheck_out.menuAction())
        self.menuIntegrate_with_Source_Control.addAction(self.actionSubmit)
        self.menuIntegrate_with_Source_Control.addAction(self.actionRevert_2)
        self.menuIntegrate_with_Source_Control.addAction(self.actionShow_History)
        self.menuIntegrate_with_Source_Control.addAction(self.menuConnect_to_Source_Control.menuAction())
        self.menuDocking.addAction(self.actionLeft)
        self.menuDocking.addAction(self.actionRight)
        self.menuHelp.addAction(self.menuIntegrate_with_Source_Control.menuAction())
        self.menuHelp.addAction(self.actionSettings_2)
        self.menuHelp.addAction(self.actionUpdatedProject)
        self.menuHelp.addAction(self.menuDocking.menuAction())
        self.menuHelp_2.addAction(self.actionAbout_2)
        self.menuHelp_2.addAction(self.actionGuildlines)
        self.menuProjects.addAction(self.actionNew_Project)
        self.menuProjects.addAction(self.actionEdit_Project)
        self.menubar.addAction(self.menuProjects.menuAction())
        self.menubar.addAction(self.menuAssets.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuHelp_2.menuAction())

        self.retranslateUi(ProjectMainForm)
        QtCore.QMetaObject.connectSlotsByName(ProjectMainForm)

    def retranslateUi(self, ProjectMainForm):
        self.menuAssets.setTitle(_translate("ProjectMainForm", "Assets", None))
        self.menuHelp.setTitle(_translate("ProjectMainForm", "Preferences", None))
        self.menuIntegrate_with_Source_Control.setTitle(_translate("ProjectMainForm", "Integrate with Source Control", None))
        self.menuConnect_to_Source_Control.setTitle(_translate("ProjectMainForm", "Connect to Source Control", None))
        self.menuCheck_out.setTitle(_translate("ProjectMainForm", "Check out", None))
        self.menuDocking.setTitle(_translate("ProjectMainForm", "Docking", None))
        self.menuHelp_2.setTitle(_translate("ProjectMainForm", "Help", None))
        self.menuProjects.setTitle(_translate("ProjectMainForm", "Projects", None))
        self.actionImport_Asset.setText(_translate("ProjectMainForm", "Add Items", None))
        self.actionRemove_Items.setText(_translate("ProjectMainForm", "Remove Items", None))
        self.actionCreate_Workflow.setText(_translate("ProjectMainForm", "New", None))
        self.actionEdit.setText(_translate("ProjectMainForm", "Edit", None))
        self.actionChange.setText(_translate("ProjectMainForm", "Change", None))
        self.actionTo_Left.setText(_translate("ProjectMainForm", "to Left", None))
        self.actionTo_Right.setText(_translate("ProjectMainForm", "to Right", None))
        self.actionQA.setText(_translate("ProjectMainForm", "QA", None))
        self.actionUpdatedProject.setText(_translate("ProjectMainForm", "Install Update", None))
        self.actionUpdatedProject.setShortcut(_translate("ProjectMainForm", "Ctrl+U", None))
        self.actionSettings_2.setText(_translate("ProjectMainForm", "Settings...", None))
        self.actionSettings_2.setShortcut(_translate("ProjectMainForm", "Ctrl+R", None))
        self.actionAdd.setText(_translate("ProjectMainForm", "Add file to Source Control", None))
        self.actionRevert.setText(_translate("ProjectMainForm", "Revert", None))
        self.actionDelete.setText(_translate("ProjectMainForm", "Delete file", None))
        self.actionSettings.setText(_translate("ProjectMainForm", "Connect to Source Control ...", None))
        self.actionUpdate_tools.setText(_translate("ProjectMainForm", "Update tools", None))
        self.actionAbouts.setText(_translate("ProjectMainForm", "About", None))
        self.actionAbout_2.setText(_translate("ProjectMainForm", "About", None))
        self.actionGuildlines.setText(_translate("ProjectMainForm", "Guildlines", None))
        self.actionPerforce.setText(_translate("ProjectMainForm", "Perforce", None))
        self.actionSVN.setText(_translate("ProjectMainForm", "SVN", None))
        self.actionGet_latest_version.setText(_translate("ProjectMainForm", "Get latest version", None))
        self.actionGet_latest_version.setShortcut(_translate("ProjectMainForm", "Ctrl+Shift+G", None))
        self.actionSubmit.setText(_translate("ProjectMainForm", "Submit...", None))
        self.actionSubmit.setShortcut(_translate("ProjectMainForm", "Ctrl+S", None))
        self.actionRevert_2.setText(_translate("ProjectMainForm", "Revert", None))
        self.actionAdd_to_Existing_Changelist.setText(_translate("ProjectMainForm", "Add to Existing changelist", None))
        self.actionAdd_to_new_changelist.setText(_translate("ProjectMainForm", "Add to new changelist", None))
        self.actionShow_History.setText(_translate("ProjectMainForm", "Show History...", None))
        self.actionGet_revision.setText(_translate("ProjectMainForm", "Get revision...", None))
        self.actionLeft.setText(_translate("ProjectMainForm", "Left", None))
        self.actionRight.setText(_translate("ProjectMainForm", "Right", None))
        self.actionNew_Project.setText(_translate("ProjectMainForm", "New Project", None))
        self.actionEdit_Project.setText(_translate("ProjectMainForm", "Edit Project", None))
        self.actionAssetQA.setText(_translate("ProjectMainForm", "Asset QA", None))
        self.actionAssetTracking.setText(_translate("ProjectMainForm", "Asset Tracking", None))
        self.actionAssetBrowser.setText(_translate("ProjectMainForm", "Asset Browser", None))

