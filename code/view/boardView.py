'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from PyQt5 import *
from PyQt5.QtGui import *
from view import cardView

class boardView(QtWidgets.QWidget):
    '''
    classdocs
    '''
    
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        
        self.text = "hejsan"
        
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont('Decorative', 10))
        painter.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)  
        painter.drawRect(0,0,30,200)
        
        painter.setBrush(QtCore.Qt.darkGreen)
        painter.drawRect(0, 0, 500, 500)

        
        painter.end()
        
        card = cardView.cardView(self)
        card.move(200, 100)
        card.show()
        
        card2 = cardView.cardView(self)
        card2.move(220,120)
        card2.show()
        

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(boardView,self).__init__(parent)
        
        self.setMaximumSize(1280,1280)
        self.setMinimumSize(parent.size().width(), parent.size().height())
        
        #self.setGeometry(0, 0, parent.size().width(), parent.size().height())
        self.show()