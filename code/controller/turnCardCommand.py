'''
Created on 19 May 2014

@author: Sven
'''

from PyQt5.QtWidgets import QUndoCommand

from model import boardModel

class turnCardCommand(QUndoCommand):
    '''
    A QUndoCommand to turn a card (change its facing).
    '''

    def __init__(self, model, cardId):
        '''
        Constructor.
        '''
        super(turnCardCommand, self).__init__()
        self.model = model
        self.cardId = cardId
    
    
    def redo(self):
        '''
        Performs or redoes the command.
        '''
        self.model.turnCard(self.cardId)
        
        
    def undo(self):
        '''
        Undoes the command.
        '''
        self.model.turnCardUndo(self.cardId)