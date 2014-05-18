'''
Created on 24 apr 2014

@author: Sven, Max
'''

from PyQt5.QtCore import (QObject, pyqtSignal)

class communicator(QObject):
    '''
    Communicator for signals 
    '''
    # Update stack signal from model to view
    updateStackSignal = pyqtSignal(dict, name='updateSignal')
    updateCardSignal = pyqtSignal(int, name='updateCardSignal')
    updateAllCardsSignal = pyqtSignal(list, name='updateAllCardsSignal')

    def __init__(self):
        '''
        Constructor
        '''
        super(communicator, self).__init__()