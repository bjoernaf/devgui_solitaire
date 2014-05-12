'''
Created on 2 maj 2014

@author: Sven
'''

from PyQt5.QtWidgets import QUndoCommand

from model import boardModel

class moveCardCommand(QUndoCommand):
    '''
    A QUndoCommand created to move a card(cardModel) from one stack to another
    with options to undo and redo.
    '''


    def __init__(self, model, fromStack, toStack, cardID):
        '''
        Constructor
        '''
        super(moveCardCommand, self).__init__()
        self.model = model
        self.fromStack = fromStack
        self.toStack = toStack
        self.cardID = cardID
    
    
    def redo(self):
        '''
        Call to perform or redo a moveCardCommand
        '''
        self.model.moveCard(self.fromStack, self.toStack, self.cardID)
        
        
    def undo(self):
        '''
        Call to undo a moveCardCommand
        '''
        self.model.moveCard(self.toStack, self.fromStack, self.cardID)
        