'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from view import solitaireWindow
from model import boardModel

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QUndoStack

from controller import moveCardCommand

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
        
        # Create the model, pass controller as parameter
        # TODO TODO REMOVE COMMENT WHEN MODEL WORKS
        self.model = boardModel.boardModel()
        
        # Create undoStack
        self.undoStack = QUndoStack()
        
        # Create the main window (View), pass controller as parameter
        self.solWin = solitaireWindow.solitaireWindow("Solitaire", self)
        self.solWin.show()
        
        self.testUndo()
        
    def signalInterpreter(self, color, value, point):
        '''
        Receive a signal from the view and take appropriate action.
        '''
        print("Signal received in controller from card:")
        print("Color: ", color,  " Value: ",  value, " X-coord: ", point.x(), " Y-coord:", point.y())
        
    def undo(self):
        '''
        Slot receiving a signal from the Edit menu's undo function.
        Calls the undo function of the undoStack
        '''
        print("Controller: Undo()")
        self.undoStack.undo()
        
    def redo(self):
        '''
        Slot receiving a signal from the Edit menu's redo function.
        Calls the redo function of the undoStack
        TODO: Find out how this works
        '''
        print("Controller: Redo()")
        self.undoStack.redo()
        
    def moveCard(self, fromStack, toStack, cardID):
        '''
        Slot receiving signals from view. Creates a moveCardCommand(QUndoCommand)
        and pushes it on the undoStack.
        '''
        # Temporary print until implemented
        print("Controller: moveCardCommand(fromStack:" + str(fromStack) + ", toStack:" + str(toStack) + ", cardID:" + str(cardID) + ")")
        
        # Create moveCardCommand
        aMoveCardCommand = moveCardCommand.moveCardCommand(self.model, fromStack, toStack, cardID)
        
        # Push command to undoStack, undoStack automatically performs command redo()
        self.undoStack.push(aMoveCardCommand)
        
    def testUndo(self):
        '''
        Test undo and redo
        '''
        
        print("Co : No");
        for i in range(0,52):
            aCard = self.model.getCard(i)
            print(str(i) + ". " + str(aCard.getColor()) + " : " + str(aCard.getValue()))
            
        print("--BEGIN MOVE--")
        self.moveCard(boardModel.boardStacks.Deck, boardModel.boardStacks.Drawable, 39)
        print("--END MOVE--")
        
        self.printOut()
        
        print("--BEGIN MOVE--")
        self.moveCard(boardModel.boardStacks.Deck, boardModel.boardStacks.Drawable, 26)
        print("--END MOVE--")
        
        self.printOut()
        
        print("--BEGIN MOVE--")
        #board.moveCard(boardModel.boardStacks.Drawable, boardModel.boardStacks.Deck, 26)
        self.undo()
        print("--END MOVE--")
        
        
        self.printOut()
        
        print("--BEGIN MOVE--")
        self.redo()
        print("--END MOVE--")
        
        self.printOut()
        
        print("--BEGIN MOVE--")
        self.undo()
        print("--END MOVE--")
        
        self.printOut()
        
        
    def printOut(self):
        print("--BEGIN PRINTOUT--")
        aList = self.model.getStack(boardModel.boardStacks.Drawable)
        for i in range(0, len(aList)):
            aCard = self.model.getCard(aList[i])
            print(str(aCard.getColor()) + " : " + str(aCard.getValue()))
        print("--END PRINTOUT--")