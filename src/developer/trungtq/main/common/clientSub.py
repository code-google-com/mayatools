import zmq

def socketSub():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.connect('tcp://127.0.0.1:5000')
    sub.setsockopt(zmq.SUBSCRIBE, '' )
    while True:
        message = sub.recv()
        print message

if __name__ == '__main__':
    socketSub()
    
