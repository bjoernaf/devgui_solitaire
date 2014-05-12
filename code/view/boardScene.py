'''
Created on 10 maj 2014

@author: Sven
'''

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent

class boardScene(QGraphicsScene):
    '''
    A Scene to display in q QGraphicsView
    Only contains override of mouseMoveEvent to detect cursor position
    '''
    def __init__(self, x, y, width, height, gsc):
        super(boardScene,self).__init__()
        self.gameStateController = gsc
    
    def dragMoveEvent(self, event):
        '''
        When drag object is moved, update the position of dragCardStackView
        if it's a card that is moving.
        '''
        #If DragEvent originates from within Solitaire
        if event.source() != None:
            # Check that it contains a valid card id as text
            if event.mimeData().hasText() and "," in event.mimeData().text():
                # Update position of the dragStack
                self.gameStateController.solWin.bView.dragCardStackView.updatePos(event.scenePos())
       			
        # Call super        
        QGraphicsScene.dragMoveEvent(self, event)
        
    def mouseMoveEvent(self, event):
        '''
        When the mouse is moved, update the position of dragCardStackView.
        '''
        self.gameStateController.solWin.bView.dragCardStackView.updatePos(event.scenePos())
        QGraphicsScene.mouseMoveEvent(self, event)