'''
Created on 24 apr 2014

@author: Sven
'''

from PyQt5.QtCore import (QObject, pyqtSignal, QPointF)

class communicator(QObject):
    '''
    Communicator for signals 
    '''
    # just a test signal to move a card
    signal = pyqtSignal(int, int, QPointF, name='cardInfo')
    
    # signal to move cards.
    # call as moveCardSignal(fromStack, toStack, cardID)
    moveCardSignal = pyqtSignal(int, int, int, name='moveCard')
    
    turnCardSignal = pyqtSignal(int, name='turnCard')
    
    # undo signal
    undoSignal = pyqtSignal(name = 'undo')
    
    # redo signal
    redoSignal = pyqtSignal(name = 'redo')

    def __init__(self):
        '''
        Constructor
        '''
        super(communicator, self).__init__()