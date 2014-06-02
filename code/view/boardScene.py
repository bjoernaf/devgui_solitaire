'''
Created on 10 maj 2014

@author: Sven
'''

from PyQt5.QtWidgets import QGraphicsScene

class boardScene(QGraphicsScene):
    '''
    A Scene to display in a QGraphicsView
    Only contains override of mouseMoveEvent to detect cursor position
    '''
    
    def __init__(self, x, y, width, height, boardView):
        '''
        Constructor
        '''
        super(boardScene,self).__init__()
        self.boardView = boardView
    
    
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
                self.boardView.tempStackView.updatePos(event.scenePos())
        
        # Call super        
        QGraphicsScene.dragMoveEvent(self, event)
        
        
    def mouseMoveEvent(self, event):
        '''
        When the mouse is moved, update the position of dragCardStackView.
        '''
        self.boardView.tempStackView.updatePos(event.scenePos())
        QGraphicsScene.mouseMoveEvent(self, event)
        
    def resizeEvent(self, event):
        '''
        Override of resizeEvent.
        Called from boardView to forward size changes.
        '''
        self.setSceneRect(0, 0, event.size().width(), event.size().height())