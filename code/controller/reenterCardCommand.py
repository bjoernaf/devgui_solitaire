'''
Created on 19 May 2014

@author: Sven
'''

from PyQt5.QtWidgets import QUndoCommand


class reenterCardCommand(QUndoCommand):
    '''
    A QUndoCommand to move cards from the Drawable stack to the bottom of the Deck.
    '''

    def __init__(self, model):
        '''
        Constructor.
        '''
        super(reenterCardCommand, self).__init__()
        self.model = model
    
    
    def redo(self):
        '''
        Performs or redoes the command.
        '''
        self.numberOfCards = self.model.reenterCards()
        print("REECARDCOM: redo: Put", self.numberOfCards, "cards back on Deck.")
                
        
    def undo(self):
        '''
        Undoes the command.
        '''
        print("REECARDCOM: undo: Returning", self.numberOfCards, "cards to Drawable.")
        self.model.unReenterCards(self.numberOfCards)