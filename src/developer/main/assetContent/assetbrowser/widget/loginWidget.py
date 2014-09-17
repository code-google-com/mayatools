try:
	reload(ui)
except:
	from developer.main.assetContent.assetbrowser.widget.ui import loginUI as ui
	
try:
	reload(cf)
except:
	from developer.main.common import commonFunctions as cf

from PyQt4 import QtGui
from P4 import P4, P4Exception
import socket

class QtWidget(QtGui.QMainWindow, ui.Ui_MainWindow):
                
	def __init__(self, parent = cf.getMayaWindow()):
		super(QtGui.QMainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setObjectName('loginForm')
		self.workSpaces = list()
		self.root = list()
		
		# load ui controls
		
		#self.edtPort.editingFinished.connect(self.loadWorkSpaces)
		#self.edtUserName.editingFinished.connect(self.loadWorkSpaces)
		self.edtPassWord.editingFinished.connect(self.loadWorkSpaces)
		
	def loadWorkSpaces(self):
		self.cbbWorkSpaces.clear()
		p4 = P4()
		p4.port = str(self.edtPort.text())
		p4.user = str(self.edtUserName.text())
		p4.password = str(self.edtPassWord.text())
		try:
		    out = list()
		    p4.connect()
		    for wp in p4.run('clients'):
		    	if wp['Host'] == socket.gethostname() and wp['Owner'] == p4.user:
		    		self.root.addItem(wp['Root'])
		    		self.workSpaces.append(wp['client'])
		except P4Exception:
			for e in p4.errors:
				print e
		finally:
			p4.disconnect()

			
	def authenticateP4Conn(self):
		p4 = P4()
		p4.port = self.edtPort.text()
		p4.user = self.edtUserName.text()
		p4.password = self.edtPassWord.text()
		p4.client = self.getClients(p4.port, p4.username, p4.password)['client']
		try:
			p4.connect()
		except P4Exception:
			print p4.errors()
		finally:
			p4.disconnect()
			
		