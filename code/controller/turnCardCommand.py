'''
Created on 19 maj 2014

@author: Sven
'''

from PyQt5.QtWidgets import QUndoCommand

from model import boardModel

class turnCardCommand(QUndoCommand):
    '''
    A QUndoCommand created to turn a card. (up / down)
    '''


    def __init__(self, model, cardId):
        '''
        Constructor
        '''
        super(turnCardCommand, self).__init__()
        self.model = model
        self.cardId = cardId
    
    
    def redo(self):
        '''
        Call to perform or redo a moveCardCommand
        '''
        self.model.turnCard(self.cardId)
        
        
    def undo(self):
        '''
        Call to undo a moveCardCommand
        '''
        self.model.turnCardUndo(self.cardId)
        