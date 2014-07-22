'''
Created on Jul 6, 2014

@author: Trung
'''

import zmq
import sys
import time
from PyQt4 import QtCore, QtGui

server = 'tcp://127.0.0.1'
port = '5000'

class socketPubProjectInfo():
    def __init__(self, projectDir):
        print 'inititalize a socket to publish message to client.'
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(server + ':' + port)
        self.socket.send('Socket has been initilized .......')
        self.fileWatcher = QtCore.QFileSystemWatcher()
        self.fileWatcher.addPath(projectDir)
        self.fileWatcher.directoryChanged.connect(self.sendMessage)
          
    def addPath(self, path):
        print path + ' has been added to fileWatcher object.'
        self.fileWatcher.addPath(path)
    
    def sendMessage(self, message):
        print 'server has been sent a message ' + message
        self.socket.send(message)
        print 'server sent message done.'

if __name__  == '__main__':
    app = QtGui.QApplication(sys.argv)
    socket = socketPubProjectInfo('D:/ge_Tools')
    sys.exit(app.exec_())
