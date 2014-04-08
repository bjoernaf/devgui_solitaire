'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from model import stackModel

class stackWorldModel(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        # Upside down stack from which the user draws cards.
        self.drawStack = stackModel()
        
        # Stacks at top of screen
        self.topStackOne = stackModel()
        self.topStackTwo = stackModel()
        self.topStackThree = stackModel()
        self.topStackFour = stackModel()
        
        # Stacks at bottom of screen
        self.bottomStackOne = stackModel()
        self.bottomStackTwo = stackModel()
        self.bottomStackThree = stackModel()
        self.bottomStackFour = stackModel()
        
        # Stack that is currently being dragged
        self.dragDropStack = stackModel()
        