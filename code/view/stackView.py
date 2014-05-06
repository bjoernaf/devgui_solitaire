'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
'''

from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import (QGraphicsItem)
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
    
    rectx = penWidth/2
    recty = penWidth/2 
    rectWidth = width + penWidth
    rectHeight = height + penWidth

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
        
        # Accept drops on the stacks
        self.setAcceptDrops(True)
        

    def boundingRect(self):
        return QRectF(self.rectx, self.recty,
                      self.rectWidth, self.rectHeight) 
    
        
    

    def paint(self, painter, option, widget=None):
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setColor(Qt.white)
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRoundedRect(0, 0, 90, 130, 9.0, 9.0, Qt.AbsoluteSize)
        painter.setPen(Qt.white)
        
        
    def dragEnterEvent(self, event):
        '''
        Run when a drag object enters the bounding rectangle of a stack
        Set event to accepted, drop will then generate dropEvent
        '''
        if event.mimeData().text() == "Card":
            event.setAccepted(True)
            print("Event drop accepted")
        else:
            print("Event drop ignored")
            
    def dropEvent(self, event):
        '''
        DropEvent when an item is dropped on the stack
        '''
        print("Dropped item: " + event.mimeData().text())
        
        # Update stack to add moved cards
        #self.com.moveCardSignal.emit(fromStack, toStack, cardID)
