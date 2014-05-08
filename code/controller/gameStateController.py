'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from view import solitaireWindow
from view import sliderWindow
from model import boardModel

from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QUndoStack
from PyQt5.QtWidgets import QDialog

from controller import moveCardCommand
from controller import communicator
from view import boardView
from model import boardStacks


class gameStateController(object):
    '''
    gameStateController is the controller in an MVC pattern.
    It interprets signals from the view and calls appropriate method in the model.
    '''

    opacity = 100

    def __init__(self):
        '''face
        
        Constructor
        '''
        super(gameStateController,self).__init__()
        
        # Initialize communicator
        self.com = communicator.communicator()
        
        # Create the model, pass controller as parameter
        # TODO TODO REMOVE COMMENT WHEN MODEL WORKS
        self.model = boardModel.boardModel(self)
        
        # Create the main window (View), pass controller as parameter
        self.solWin = solitaireWindow.solitaireWindow("Solitaire", self)     
        
        self.solWin.show()
        
        self.opacity = 100
        self.slide = sliderWindow.sliderWindow("Opacity", self)
        self.slide.show()
        
        # Create undoStack
        self.undoStack = QUndoStack()
        # Send signal if possibility to undo/redo changes
        self.undoStack.canUndoChanged.connect(self.solWin.updateMenuUndo)
        self.undoStack.canRedoChanged.connect(self.solWin.updateMenuRedo)
        
        # Connect updateStacks to slot in model
        self.com.updateSignal.connect(self.solWin.bView.updateStacks)
        
        
        
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
        
    def updateControllerStacks(self, stacks):
        '''
        Slot receiving stack update from model
        '''
        # Forward stacks to view
        self.com.updateSignal.emit(stacks)
        
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

# === ADDED BY MARTIN
#       Makes sure that the cards are initially on the Deck stack, at the cost of
#       introducing an extra move from Drawable to Deck.

        print("--BEGIN MOVE--")
        self.moveCard(boardStacks.boardStacks.Drawable, boardStacks.boardStacks.Deck, 0)
        print("--END MOVE--")
        
        self.printOut()

        self.redo()

# === END ADDED BY MARTIN
            
#         print("--BEGIN MOVE--")
#         self.moveCard(boardStacks.boardStacks.Deck, boardStacks.boardStacks.Drawable, 39)
#         print("--END MOVE--")
#         
#         self.printOut()
#         
#         print("--BEGIN MOVE--")
#         self.moveCard(boardStacks.boardStacks.Deck, boardStacks.boardStacks.Drawable, 26)
#         print("--END MOVE--")
#         
#         self.printOut()
#         
#         print("--BEGIN MOVE--")
#         #board.moveCard(boardModel.boardStacks.Drawable, boardModel.boardStacks.Deck, 26)
#         self.undo()
#         print("--END MOVE--")
#         
#         
#         self.printOut()
#         
#         print("--BEGIN MOVE--")
#         self.redo()
#         print("--END MOVE--")
#         
#         self.printOut()
#         
#         print("--BEGIN MOVE--")
#         self.undo()
#         print("--END MOVE--")
#         
#         self.printOut()
        
        
    def printOut(self):
        '''
        Debug function that prints the drawable stack.
        '''
        print("--BEGIN PRINTOUT--")
        aList = self.model.getStack(boardStacks.boardStacks.Drawable)
        for i in range(0, len(aList)):
            aCard = self.model.getCard(aList[i])
            print(str(aCard.getColor()) + " : " + str(aCard.getValue()))
        print("--END PRINTOUT--")


    def getCard(self, cardId):
        '''
        Returns the cardModel representation of the card with id cardId.
        '''
        return self.model.getCard(cardId)


    def getStack(self, stackId):
        '''
        Returns a list of all card id:s in stack stackId, from bottom to top.
        '''
        return self.model.getStack(stackId)
