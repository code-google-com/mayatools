'''
Created on Jul 6, 2014

@author: Trung
'''

import zmq
import sys
import time

def isUpdate():
    return True

def pubServer():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    server = 'tcp://127.0.0.1:5000'
    socket.bind(server)
    while True:
        if isUpdate():
            print ('Project update: Sony, IronMonkey ...')
            socket.send('Project Sony need to updated')
            socket.send('Project IronMonkey need to updated')
            time.sleep(1)
            
if __name__ == '__main__':
    pubServer()


