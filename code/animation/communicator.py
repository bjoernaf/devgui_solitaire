'''
Created on 5 June 2014

@author: Martin
'''

from PyQt5.QtCore import QObject, pyqtSignal, QPointF

class communicator(QObject):
    '''
    Contains signals used in the animation package.
    '''
    # Signal to move cards between stacks
    moveCardSignal = pyqtSignal(int, int, int, name='moveCard')
    
    # Signal to turn a card
    turnCardSignal = pyqtSignal(int, name='turnCard')
    
    # Signal to end an undo macro
    endFlipMacroSignal = pyqtSignal(name = 'endFlipMacroSignal')

    # Signal to set the z value of a card
    setCardZValueSignal = pyqtSignal(int, int, name = 'setCardZValueSignal')
    
    # Signal to transform a card
    transformCardSignal = pyqtSignal(int, QPointF, int, float, name = 'transformCardSignal')

    # Signal to pulsate a card
    pulsateCardSignal = pyqtSignal(int, int, name = 'pulsateCardSignal')


    def __init__(self):
        '''
        Constructor.
        '''
        super(communicator, self).__init__()