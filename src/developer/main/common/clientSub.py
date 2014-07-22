import zmq


server = 'tcp://127.0.0.1'
port = '5000'

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(server + ':' + port)
message = socket.recv()
print message
    
