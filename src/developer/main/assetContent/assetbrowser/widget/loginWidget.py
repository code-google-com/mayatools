try:
	reload(ui)
except:
	from developer.main.assetContent.assetbrowser.widget.ui import loginUI as ui
	
try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf

try:
	reload(geXML)
except:
	from developer.main.common import geXML

from PyQt4 import QtGui, QtCore
from P4 import P4, P4Exception
from functools import partial
import socket

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
    SCConnected = QtCore.pyqtSignal([bool])
    def __init__(self, parent = cf.getMayaWindow()):
		super(QtGui.QMainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName('loginForm')
		self.workSpaces = list()
		self.root = list()
		self.dir = ''
		self.isConnected = False
		
		# load ui controls
		
		#self.edtPort.editingFinished.connect(self.loadWorkSpaces)
		#self.edtUserName.editingFinished.connect(self.loadWorkSpaces)
		self.edtPassWord.editingFinished.connect(self.loadWorkSpaces)
		self.btnLogin.clicked.connect(self.authenticateP4Conn)
		self.btnLoginNoSC.clicked.connect(partial(self.SCConnected.emit, self.isConnected))
		
    def showInfo(self):
		pass
		
	# -- loading workspaces base on 
    def loadWorkSpaces(self):
		self.cbbWorkSpaces.clear()
		#geXML.initXmlPath("")
		testXML = geXML.cGeXML()
		testXML.writeHistoryFile('', 'host', '12.34')
		p4 = P4()
		p4.port = str(self.edtPort.text())
		p4.user = str(self.edtUserName.text())
		#p4.password = str(self.edtPassWord.text())
		try:
		    out = list()
		    p4.connect()
		    for wp in p4.run('clients'):
		    	if wp['Host'] == socket.gethostname() and wp['Owner'] == p4.user:
		    		self.root.append(wp['Root'])
		    		self.cbbWorkSpaces.addItem(wp['client'])
		except P4Exception:
			for e in p4.errors:
				self.textEdit.append(e + '\n')
		finally:
			p4.disconnect()

    def authenticateP4Conn(self):
		p4 = P4()
		p4.port = str(self.edtPort.text())
		p4.user = str(self.edtUserName.text())
		p4.password = str(self.edtPassWord.text())
		try:
			p4.connect()
			p4.run_login()
			self.dir =  self.root[self.cbbWorkSpaces.currentIndex()]
			self.textEdit.append('Root location: ' + self.dir + '\n')
			p4.disconnect()
			self.isConnected = True
			self.SCConnected.emit(self.isConnected)
		except P4Exception:
			for e in p4.errors:
				self.textEdit.append(e + '\n')
			
		