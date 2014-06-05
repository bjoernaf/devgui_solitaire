'''
Created on 24 apr 2014

@author: Sven
'''

from PyQt5.QtCore import (QObject, pyqtSignal)

class communicator(QObject):
    '''
    Communicator for signals 
    '''
    # just a test signal to move a card
    updateSignal = pyqtSignal(dict, name='updateSignal')

    updateCardSignal = pyqtSignal(int, name='updateCardSignal')
    
    updateAllCardsSignal = pyqtSignal(list, name='updateAllCardsSignal')
    
    # Signal to start a flip animation
    addFlipAnimationSignal = pyqtSignal(list, int, int, int, int, int, int, int, int, float,
                                        name = 'addFlipAnimationSignal')
    
    # Signal to start a pulsating animation
    addPulsatingAnimationSignal = pyqtSignal(int, name = 'addPulsatingAnimationSignal')
    
    # Signal to stop a pulsating animation
    removePulsatingAnimationSignal = pyqtSignal(int, name = 'removePulsatingAnimationSignal')


    def __init__(self):
        '''
        Constructor
        '''
        super(communicator, self).__init__()