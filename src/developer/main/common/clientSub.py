import zmq


server = 'tcp://127.0.0.1'
port = '5000'

class socketSubscribeProjectInfo():
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(server + ':' + port)
        self.receive()
        
    def receive(self):
        message = self.socket.recv()
        print message