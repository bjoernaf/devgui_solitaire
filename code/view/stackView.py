'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsItem)
from view import communicator

class stackView(QGraphicsItem):
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
        