'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
'''

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsItem)
from view import communicator

class stackView(QGraphicsItem):
    '''
    Class to display stacks
    '''
    
    penWidth = 4
    width = 90
    height = 130
    xRadius = 9
    yRadius = 9

    def __init__(self, gameStateController):
        '''
        Constructor
        '''
        super(stackView, self).__init__()
        
        # Create communicator
        self.com = communicator.communicator()
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)

    def boundingRect(self):
        return QRectF(-stackView.penWidth/2, -stackView.penWidth/2,
                      stackView.width + stackView.penWidth,
                      stackView.height + stackView.penWidth) 

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setColor(Qt.white)
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRoundedRect(0, 0, 90, 130, 9.0, 9.0, Qt.AbsoluteSize)
        painter.setPen(Qt.white)
