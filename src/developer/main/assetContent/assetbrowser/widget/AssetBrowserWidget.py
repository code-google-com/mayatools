try:
	reload(ui)
except:
	from developer.main.assetContent.assetbrowser.widget.ui import AssetBrowserUI as ui
	
try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf
	
try:
	reload(aWg)
except:
	from developer.main.assetContent.assetbrowser.widget import assetWidget as aWg 

from PyQt4 import QtGui, QtOpenGL

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self, scRoot = None, parent = cf.getMayaWindow()):
		super(QtGui.QMainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName('assetBrowserForm')
		self._root = ''
		if scRoot:
			self._root = scRoot
		else:
			self._root = 'D:\Repo_UDK\QtCinematic\SourceArt'.replace('\\' , '/')
		
		# set root location
										
		self.edtRootLocation.setText(self._root)
										
		# set QFileSystemModel
		
		model = QtGui.QFileSystemModel()
		model.setRootPath(self._root)
		
		# set model to QTreeView
		
		self.treeViewPath.setModel(model)
		self.treeViewPath.setRootIndex(model.index(self._root))
		self.treeViewPath.hideColumn(1)
		self.treeViewPath.hideColumn(2)
		self.treeViewPath.hideColumn(3)
		self.treeViewPath.hideColumn(4)	
		
		# set up connection treeView and listWidget
		
		self.view = aWg.AssetWidgetView()
		
		self.view.setSceneRect(0, 0, 1000, 500)
		self.vGraphicsLayout.addWidget(self.view)
		
		# set scene to view
		
		self.scene = aWg.AssetWidgetScene()
		self.view.setScene(self.scene)
		self.view.setSceneRect(0, 0, 1000, 500)
		
		self.item1 = aWg.assetWidget()
		self.item2 = aWg.assetWidget()
		self.scene.addItem(self.item1)
		self.scene.addItem(self.item2)
		self.item1.setPos(0,0)
		self.item2.setPos(120,0)
		
	
		
		
	
		
		
		
		
		
		
	
		
		
