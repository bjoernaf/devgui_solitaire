'''
Created on 24 April 2014

@author: Sven, Max, Bjorn
'''

from PyQt5.QtCore import (QObject, pyqtSignal)

class communicator(QObject):
    '''
    Contains signals used in the model package.
    '''
    updateStackSignal = pyqtSignal(dict, name='updateSignal')
    
    updateCardSignal = pyqtSignal(int, name='updateCardSignal')
    
    updateAllCardsSignal = pyqtSignal(list, name='updateAllCardsSignal')
    
    gameWonSignal = pyqtSignal(name='gameWonSignal')

    def __init__(self):
        '''
        Constructor.
        '''
        super(communicator, self).__init__()
