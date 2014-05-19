'''
Created on 19 maj 2014

@author: Sven
'''

from PyQt5.QtWidgets import QUndoCommand

from model import boardModel

class reenterCardCommand(QUndoCommand):
    '''
    A QUndoCommand created to turn a card. (up / down)
    '''


    def __init__(self, model):
        '''
        Constructor
        '''
        super(reenterCardCommand, self).__init__()
        self.model = model
    
    
    def redo(self):
        '''
        Call to perform or redo a reenterCard Command
        '''
        self.numberOfCards = self.model.reenterCards()
        print("REECARDCOM: redo: Put", self.numberOfCards, "cards back on deck.")
                
        
    def undo(self):
        '''
        Call to undo a moveCardCommand
        '''
        print("REECARDCOM: undo: Returning", self.numberOfCards, "cards to drawable.")
        self.model.unReenterCards(self.numberOfCards)
        
