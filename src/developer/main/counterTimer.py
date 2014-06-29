'''
Created on Jun 29, 2014

@author: Trung
'''

import threading
import time

class asyncWrite(threading.thread):
    def __init__(self, text, out):
        threading.Thread.__init__(self)
        self.text = text
        self.out = out
        
    def run(self):
        f = open(self.out, "a")
        f.write(self.text + '\n')
        f.close()
        time.sleep(2)
        print 'Done background file write ' + self.out
        
def Main():
    message = raw_input('Enter string to store')
    background = asyncWrite(message, 'out.txt')
    print '                  '
    print 100 + 400
    background.join() 
    print 
