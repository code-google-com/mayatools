import zmq
import time
import random

def initPubServer():
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind('tcp://127.0.0.1:5000')
    sock.send('Socket has been initialized successfully .....')
    while True:
        number = random.randrange(1110, 1115)
        print 'Socket has sent a message ' + str(number)
        sock.send(str(number))
        time.sleep(1)

if __name__ == '__main__':
    initPubServer()
