'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from view import solitaireWindow
from model import boardModel

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QUndoStack

from controller import moveCardCommand
from controller import communicator
from view import boardView
from model import boardStacks

class gameStateController(object):
    '''
    gameStateController is the controller in an MVC pattern.
    It interprets signals from the view and calls appropriate method in the model.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(gameStateController,self).__init__()
        
        self.opacity = 100
        
        # Initialize communicator
        self.com = communicator.communicator()
        
        # Create the main window (View), pass controller as parameter
        self.solWin = solitaireWindow.solitaireWindow("Solitaire", self)
        self.solWin.show()
        
        # Create undoStack
        self.undoStack = QUndoStack()
        
        # Send signal if possibility to undo/redo changes
        self.undoStack.canUndoChanged.connect(self.solWin.updateMenuUndo)
        self.undoStack.canRedoChanged.connect(self.solWin.updateMenuRedo)
        
        # Connect updateSignal to slot in view
        self.com.updateSignal.connect(self.solWin.bView.updateStacks)
        
        #Connect updateCardSignal to slot in view
        self.com.updateCardSignal.connect(self.solWin.bView.updateCard)
        
        self.com.updateAllCardsSignal.connect(self.solWin.bView.updateAllCards)
        
        # Create the model, pass controller as parameter
        self.model = boardModel.boardModel(self)
        
        
    def undo(self):
        '''
        Slot receiving a signal from the Edit menu's undo function.
        Calls the undo function of the undoStack
        '''
        print("CONTROLLER: Undo: Performing undo operation.")
        self.undoStack.undo()
        
        
    def redo(self):
        '''
        Slot receiving a signal from the Edit menu's redo function.
        Calls the redo function of the undoStack
        TODO: Find out how this works
        '''
        print("CONTROLLER: Redo: Performing redo operation.")
        self.undoStack.redo()
  
    def updateControllerAllCards(self, cardFaceUp):
        print("CONTROLLER: updateControllerAllCards: Forward cardFacUp from MODEL to BOARDVIEW.")
        self.com.updateAllCardsSignal.emit(cardFaceUp)    
        
    def updateControllerStacks(self, stacks):
        '''
        Slot receiving stack update from model
        '''
        # Forward stacks to view
        print("CONTROLLER: UpdateControllerStacks: Forward stacks from MODEL to BOARDVIEW.")
        self.com.updateSignal.emit(stacks)

    def updateControllerCard(self, cardId):
        '''
        Slot receiving card update from model
        '''
        # Forward stacks to view
        print("CONTROLLER: updateControllerCard: Forward card from MODEL to BOARDVIEW.")
        self.com.updateCardSignal.emit(cardId)
        
        
    def moveCard(self, fromStack, toStack, cardID):
        '''
        Slot receiving signals from view. Creates a moveCardCommand(QUndoCommand)
        and pushes it on the undoStack.
        '''

        print("CONTROLLER: moveCardCommand: Ask MODEL to MoveCard(", fromStack, ",", toStack, ",", cardID, ")")
        
        # Create moveCardCommand
        aMoveCardCommand = moveCardCommand.moveCardCommand(self.model, fromStack, toStack, cardID)
        
        # Push command to undoStack, undoStack automatically performs command redo()
        self.undoStack.push(aMoveCardCommand)
        
    def turnCard(self, cardID):
        '''
        Slot receiving signal from view requesting the turning of a card.
        '''
        self.model.turnCard(cardID)