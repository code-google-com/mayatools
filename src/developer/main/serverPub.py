'''
Created on Jul 6, 2014

@author: Trung
'''

import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)

server = 'tcp://127.0.0.1:5000'
socket.bind(server)


