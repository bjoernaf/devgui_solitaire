'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from view import solitaireWindow
#from model import boardModel

from PyQt5.QtCore import QPointF

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
        # self.model = boardModel.boardModel(self)
        
        # Create undo module & command stack
        # TODO TODO TODO
        
        # Create the main window (View), pass controller as parameter
        self.solWin = solitaireWindow.solitaireWindow("Solitaire", self)
        self.solWin.show()
        
    def signalInterpreter(self, color, value, point):
        '''
        Receive a signal from the view and take appropriate action.
        '''
        print("Signal received in controller from card:")
        print("Color: ", color,  " Value: ",  value, " X-coord: ", point.x(), " Y-coord:", point.y())
        
    def moveCard(self, fromStack, toStack, cardID):
        '''
        Slot receiving signals from view. Creates a moveCardCommand(QUndoCommand)
        and pushes it on the undoStack.
        '''
        # Temporary print until implemented
        print("Controller: moveCardCommand(fromStack:" + str(fromStack) + ", toStack:" + str(toStack) + ", cardID:" + str(cardID) + ")")
        
        # Create moveCardCommand
        
        # Push command to undoStack
        
        