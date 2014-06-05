'''
Created on 24 April 2014

@author: Sven, Martin
'''

from PyQt5.QtCore import (QObject, pyqtSignal)

class communicator(QObject):
    '''
    Contains signals used in the controller package.
    '''
    # Signals to update the view
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
        Constructor.
        '''
        super(communicator, self).__init__()