'''
Created on 7 April 2014

@author: Sven, Bjorn, Martin
'''

from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QUndoStack

from model import boardModel, boardStacks
from view import solitaireWindow, boardView
from controller import communicator, moveCardCommand, turnCardCommand, reenterCardCommand
from animation import animationEngine

class gameStateController(QObject):
    '''
    The controller in a model--view--controller attern.
    It interprets signals from the other parts of the
    program and takes appropriate actions.
    '''

    def __init__(self):
        '''
        Constructor.
        '''
        super(gameStateController,self).__init__()
        
        # Initialize communicator (contains signals)
        self.com = communicator.communicator()
        
        # Create the main window, pass controller as parameter
        self.solWin = solitaireWindow.solitaireWindow("Solitaire", self)
        self.solWin.show()
        
        # Create an undo stack
        self.undoStack = QUndoStack()
        
        # Create an animation engine and push it onto a new thread
        self.animationEngine = animationEngine.animationEngine(self, self.solWin.centralWidget())
        self.animationThread = QThread()
        self.animationEngine.moveToThread(self.animationThread)
        
        # Start the new thread and thereby the animation engine
        self.animationThread.started.connect(self.animationEngine.startEngine)
        self.animationThread.start()

        # Connect animation signals to slots in the animation engine
        self.com.addFlipAnimationSignal.connect(self.animationEngine.addFlippingCards)
        self.com.addPulsatingAnimationSignal.connect(self.animationEngine.addPulsatingCard)
        self.com.removePulsatingAnimationSignal.connect(self.animationEngine.removePulsatingCard)
        
        # Send signal if possibility to undo/redo changes
        self.undoStack.canUndoChanged.connect(self.solWin.updateMenuUndo)
        self.undoStack.canRedoChanged.connect(self.solWin.updateMenuRedo)
        
        # Connect update signals to slots in view
        self.com.updateSignal.connect(self.solWin.bView.updateStacks)
        self.com.updateCardSignal.connect(self.solWin.bView.updateCard)
        self.com.updateAllCardsSignal.connect(self.solWin.bView.updateAllCards)
        
        # Create the model, pass controller as parameter
        self.model = boardModel.boardModel(self)
        
        
    def undo(self):
        '''
        Slot receiving undo signals.
        Calls the undo function of the undoStack.
        '''
        print("CONTROLLER: Undo: Performing undo operation.")
        self.undoStack.undo()
        
        
    def redo(self):
        '''
        Slot receiving redo signals.
        Calls the redo function of the undoStack.
        '''
        print("CONTROLLER: Redo: Performing redo operation.")
        self.undoStack.redo()

  
    def updateControllerAllCards(self, cardFaceUp):
        '''
        Slot receiving updates from the model regarding how cards
        are facing (up or down).
        '''
        print("CONTROLLER: updateControllerAllCards: Forward cardFaceUp from MODEL to BOARDVIEW.")
        self.com.updateAllCardsSignal.emit(cardFaceUp)


    def updateControllerStacks(self, stacks):
        '''
        Slot receiving updates of the stacks from the model.
        '''
        print("CONTROLLER: UpdateControllerStacks: Forward stacks from MODEL to BOARDVIEW.")
        self.com.updateSignal.emit(stacks)


    def updateControllerCard(self, cardId):
        '''
        Slot receiving signals regarding single cards
        whose facing should be changed.
        '''
        print("CONTROLLER: updateControllerCard: Forward card from MODEL to BOARDVIEW.")
        self.com.updateCardSignal.emit(cardId)
        
        
    def moveCard(self, fromStack, toStack, cardID):
        '''
        Slot receiving signals from view. Creates a move card command
        and pushes it onto the undo stack.
        '''
        print("CONTROLLER: moveCardCommand: Ask MODEL to move card ",
              cardID, " from ", fromStack, " to ", toStack, ".")
        
        aMoveCardCommand = moveCardCommand.moveCardCommand(self.model, fromStack, toStack, cardID)
        self.undoStack.push(aMoveCardCommand) # Undo stack automatically performs redo()
        
        
    def reenterCard(self):
        '''
        Slot receiving signals to move cards from the Drawable stack
        to the bottom of the Deck.
        '''
        aReenterCardCommand = reenterCardCommand.reenterCardCommand(self.model)
        self.undoStack.push(aReenterCardCommand)
       
        
    def turnCard(self, cardId):
        '''
        Slot receiving signals from view requesting the turning of a card.
        '''
        aTurnCardCommand = turnCardCommand.turnCardCommand(self.model, cardId)
        self.undoStack.push(aTurnCardCommand)

        
    def checkMove(self, fromStack, toStack, cardId):
        '''
        Function called from view requesting a check if move is valid or not.
        '''
        return self.model.checkMove(fromStack, toStack, cardId)

    
    def startNewGame(self):
        '''
        Slot receiving signals to start a new game.
        Clears the undoStack and creates a new model.
        '''
        self.undoStack.clear()
        self.model = boardModel.boardModel(self)
    
    
    def gameWonSlot(self):
        '''
        Slot receiving signals indicating that the game has been won.
        '''
        self.solWin.showGameWonDialog()
    
    
    def beginFlipMacro(self):
        '''
        Slot receiving signals to begin an undo macro when a flip animation
        is to be performed. The macro makes it possible to undo the whole operation
        in one step.
        '''
        self.undoStack.beginMacro("Flip cards")
    
    
    def endFlipMacro(self):
        '''
        Slot receiving signals to end an undo macro after a flip animation
        has been performed.
        '''
        self.undoStack.endMacro()
        
    
    def addFlipAnimation(self, cardList, startStack, endStack, startPosX, startPosY, endPosX,
                         cardOffsetX, cardWidth, cardHeight, scaleStep):
        '''
        Slot receiving signals to start a flip animation. The signals are
        forwarded to the animation engine.
        '''
        self.com.addFlipAnimationSignal.emit(cardList, startStack, endStack, startPosX,
                                             startPosY, endPosX, cardOffsetX, cardWidth,
                                             cardHeight, scaleStep)
    
    
    def addPulsatingAnimation(self, cardId):
        '''
        Slot receiving signals to start a pulsating animation. The signals are
        forwarded to the animation engine.
        '''
        self.com.addPulsatingAnimationSignal.emit(cardId)
    
    
    def removePulsatingAnimation(self, cardId):
        '''
        Slot receiving signals to stop a pulsating animation. The signals are
        forwarded to the animation engine.
        '''
        self.com.removePulsatingAnimationSignal.emit(cardId)