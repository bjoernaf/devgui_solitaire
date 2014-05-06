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

    def __init__(self):
        '''
        Constructor
        '''
        super(communicator, self).__init__()