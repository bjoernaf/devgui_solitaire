'''
Created on 2 May 2014

@author: Sven
'''

from PyQt5.QtWidgets import QUndoCommand

from model import boardModel

class moveCardCommand(QUndoCommand):
    '''
    A QUndoCommand to move a card from one stack to another
    with options to undo and redo.
    '''

    def __init__(self, model, fromStack, toStack, cardID):
        '''
        Constructor.
        '''
        super(moveCardCommand, self).__init__()
        self.model = model
        self.fromStack = fromStack
        self.toStack = toStack
        self.cardID = cardID
    
    
    def redo(self):
        '''
        Perform or redoes the command.
        '''
        self.model.moveCard(self.fromStack, self.toStack, self.cardID)
        
        
    def undo(self):
        '''
        Undoes the command
        '''
        self.model.moveCard(self.toStack, self.fromStack, self.cardID)