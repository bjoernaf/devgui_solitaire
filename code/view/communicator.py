'''
Created on 24 apr 2014

@author: Sven, Bjorn
'''

from PyQt5.QtCore import QObject, pyqtSignal, QPointF

class communicator(QObject):
    '''
    Communicator contains signals used in the view package.
    '''
    # just a test signal to move a card
    signal = pyqtSignal(int, int, QPointF, name='cardInfo')
    
    # signal to move cards.
    # call as moveCardSignal(fromStack, toStack, cardID)
    moveCardSignal = pyqtSignal(int, int, int, name='moveCard')
    
    turnCardSignal = pyqtSignal(int, name='turnCard')
    
    reenterCardSignal = pyqtSignal(name='reenterCard')
    
    # undo signal
    undoSignal = pyqtSignal(name = 'undo')
    
    # redo signal
    redoSignal = pyqtSignal(name = 'redo')
    
    # signal to start new game
    newGameSignal = pyqtSignal(name = 'newGame')
    
    # transSlider signal
    opacitySignal = pyqtSignal(int, name = 'opacitySignal')
    
    # Signal to begin an undo macro
    beginFlipMacroSignal = pyqtSignal(name = 'beginFlipMacroSignal')
    
    # Signal to start a flip animation
    addFlipAnimationSignal = pyqtSignal(list, int, int, int, int, int, int, int, int, float,
                                        name = 'addFlipAnimationSignal')
    
    # Signal to start a pulsating animation
    addPulsatingAnimationSignal = pyqtSignal(int, name = 'addPulsatingAnimationSignal')

    # Signal to stop a pulsating animation
    removePulsatingAnimationSignal = pyqtSignal(int, name = 'removePulsatingAnimationSignal')
    
    
    def __init__(self):
        '''
        Constructor simply calls super.
        '''
        super(communicator, self).__init__()
