'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
glassView is an QGraphicsItem representing a tutorial. 
'''

from PyQt5.QtCore import Qt, QRectF, QMimeData, QPointF, QSize
from PyQt5.QtGui import QDrag, QFont, QPainter, QImage
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsDropShadowEffect

class glassView(QGraphicsItem):
    '''
    Class to create and display one single card in the QGraphicsView
    '''

    def __init__(self, gameStateController, boardView, width, height):
        '''
        Constructor:
        Creates a Card in the GraphicsView.
        Also loads the appropriate image for the card.
        '''
        super(glassView, self).__init__()
        
        self.height = height
        self.width = width
        
        # Save game state controller instance
        self.gsc = gameStateController
        self.boardView = boardView
                

    def boundingRect(self):
        '''
        Returns a bounding rectangle for the tutorial glass pane.
        '''
        return QRectF(0, 0, self.width, self.height) 
    
    def paint(self, painter, option, widget=None): 
        '''
        Override of the default paint function.
        Draws a rounded rectangle representing a card.
        Draws card number and card color symbol in upper
        and lower right corner.
        '''
        
        # Set opacity to paint entire card with
        painter.setOpacity(0.3)
        
        # Set painter rendering mode
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set font and color
        painter.setPen(Qt.black)
        painter.setBrush(Qt.black)
        font = QFont("Helvetica")
        font.setBold(True)
        painter.setFont(font)
        
        # Draw the glass panel
        painter.drawRoundedRect(self.boundingRect(), 8, 8, Qt.AbsoluteSize)
    
        # Put text on it!
        painter.setPen(Qt.white)
        painter.setOpacity(1)
        painter.drawText(16, 190, "Turned up cards can be drawn to new locations.")
        painter.drawText(350, 175, "Place cards of matching color in order on the top stacks, starting with ace.")
        painter.drawText(80, 550, "Place lower cards of opposite color on higher cards. Cannot skip cards.")
        painter.drawText(8, 175, "Double click the deck to draw new cards.")
        
        
    def resizeEvent(self, event):
        '''
        Override of resizeEvent.
        Called from boardView to match size of scene and glass pane
        '''
        # Get scene position
        x = self.scenePos().x()
        y = self.scenePos().y()
        
        # Set width and height to cover scene properly
        # Scene width or height - 2 * relative scene position
        self.width = event.size().width() - 2*x
        self.height = event.size().height() - 2*y
#       

