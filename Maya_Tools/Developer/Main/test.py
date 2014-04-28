from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

#############Define MyWindow Class Here ############
class MyWindow(QMainWindow):
##-----------------------------------------  
  def __init__(self):
    QMainWindow.__init__(self)
    self.label = QLabel("No data")
    self.setCentralWidget(self.label)
    self.setWindowTitle("QMainWindow WheelEvent")
    self.x = 0
##-----------------------------------------    
  def wheelEvent(self,event):
    self.x =self.x + event.delta()/120      
    self.label.setText("Total Steps: "+QString.number(self.x))  
##-----------------------------------------    
##########End of Class Definition ################## 


def main():
  app = QApplication(sys.argv)
  window = MyWindow()
  window.show() 
  return app.exec_()
 
if __name__ == '__main__': 
 main() 