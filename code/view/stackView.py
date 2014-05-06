'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsItem, QGraphicsRectItem)
from view import communicator

class stackView(QGraphicsRectItem):
    '''
    Class to display stacks
    '''


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
        
        self.setAcceptDrops(True)
        
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