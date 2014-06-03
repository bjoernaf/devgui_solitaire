'''
Created on 10 maj 2014

@author: Sven
'''

from PyQt5.QtWidgets import QGraphicsScene

class boardScene(QGraphicsScene):
    '''
    A Scene to display in a QGraphicsView.
    Contains overrides of built-in functions
    dragMoveEvent, mouseMoveEvent and resizeEvent.
    '''
    
    def __init__(self, x, y, width, height, boardView):
        '''
        Creates a boardScene. Resize happens in resizeEvent.
        '''
        super(boardScene,self).__init__()
        self.boardView = boardView
    
    
    def dragMoveEvent(self, event):
        '''
        When a dragMoveEvent is received, update the position of
        the tempStack to the location of the event IFF the
        object being dragged is deemed to be a card.
        '''
        #If dragEvent originates from within Solitaire
        if event.source() != None:
            # Check that it contains a valid card id as text
            if event.mimeData().hasText() and "," in event.mimeData().text():
                # Update position of the tempStack
                self.boardView.tempStackView.updatePos(event.scenePos())
                self.boardView.hideFeedbackWindow()
        
        # Call super        
        QGraphicsScene.dragMoveEvent(self, event)
        
        
    def mouseMoveEvent(self, event):
        '''
        When the mouse is moved, update the position of tempStack.
        Ensures that the tempStack is never displayed at the wrong position.
        '''
        self.boardView.tempStackView.updatePos(event.scenePos())
        QGraphicsScene.mouseMoveEvent(self, event)
        
    def resizeEvent(self, event):
        '''
        Override of resizeEvent.
        Sets the size of the scene to the size of the resizeEvent.
        '''
        self.setSceneRect(0, 0, event.size().width(), event.size().height())