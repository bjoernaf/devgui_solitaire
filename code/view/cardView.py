'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from PyQt5 import *
from PyQt5.QtGui import *

class cardView(QtWidgets.QWidget):
    '''
    classdocs
    '''


    ## TODO: Smartare size
    cardWidth = 80
    cardHeight = 120
    cardXRad = 9.0
    cardYRad = 9.0

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(cardView, self).__init__(parent)
        
        ## TODO: Använd metoder i cardModel för getColor och getValue
        self.color = 0
        self.value = 13
        
        self.setMinimumHeight(cardView.cardHeight + cardView.cardYRad + 1)
        self.setMaximumHeight(cardView.cardHeight + cardView.cardYRad + 1)
        self.setMinimumWidth(cardView.cardWidth + cardView.cardXRad + 1)
        self.setMaximumWidth(cardView.cardWidth + cardView.cardXRad + 1)
        
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
             
        painter.setPen(QtCore.Qt.black)
        painter.setBrush(QtCore.Qt.white)
        painter.drawRoundedRect(0, 0, cardView.cardWidth, cardView.cardHeight, cardView.cardXRad, cardView.cardYRad, QtCore.Qt.AbsoluteSize)

        painter.end() 