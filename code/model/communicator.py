'''
Created on 24 apr 2014

@author: Sven
'''

from PyQt5.QtCore import (QObject, pyqtSignal)

class communicator(QObject):
    '''
    Communicator for signals 
    '''
    # Update stack signal from model to view
    updateStackSignal = pyqtSignal(dict, name='updateSignal')
    updateCardSignal = pyqtSignal(int, name='updateCardSignal')

    def __init__(self):
        '''
        Constructor
        '''
        super(communicator, self).__init__()