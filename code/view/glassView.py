'''
Created on 7 April 2014

@author: Sven, Bjorn
'''

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtWidgets import QGraphicsItem

class glassView(QGraphicsItem):
    '''
    glassView is a QGraphicsItem representing a tutorial.
    '''

    def __init__(self, width, height):
        '''
        Constructor:
        Creates the glassView and stores parameters
        '''
        super(glassView, self).__init__()
        
        # Save height and width
        self.height = height
        self.width = width
                

    def boundingRect(self):
        '''
        Returns a bounding rectangle for the tutorial glass pane.
        '''
        return QRectF(0, 0, self.width, self.height) 
    
    
    def paint(self, painter, option, widget=None): 
        '''
        Override of the default paint function.
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
        '''
        # Get scene position
        x = self.scenePos().x()
        y = self.scenePos().y()
        
        # Set width and height to cover scene properly
        # Scene width or height - 2 * relative scene position
        self.width = event.size().width() - 2*x
        self.height = event.size().height() - 2*y