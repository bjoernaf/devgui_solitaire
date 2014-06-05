'''
Created on 2 June 2014

@author: Sven
'''
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

class feedbackWindow(QGraphicsTextItem):
    '''
    This class is a window that shows feedback from the model
    on why a card move is invalid. It should only be attached
    to the tempStack.
    '''

    def __init__(self, text, parent = None):
        '''
        Creates a feedbackWindow with text and parent relation.
        '''
        super(feedbackWindow, self).__init__(text, parent)
        
        # Set the width and color of the window
        self.setTextWidth(120)
        self.setDefaultTextColor(Qt.red)
        
        # Create a shadow effect and attach it to the window
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(5)
        self.setGraphicsEffect(shadow)
        
    def paint(self, painter, options, widget = None):
        '''
        Override of paintEvent to create text background.
        '''
        # Set the brush properties
        painter.setBrush(QColor(230, 255, 150, 255))
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Paint a slightly transparent rounded rectangle
        painter.setOpacity(0.9)
        painter.drawRoundedRect(self.boundingRect(), 5, 5, Qt.AbsoluteSize)
        
        # Call super class to write the text
        painter.setOpacity(1.0)
        QGraphicsTextItem.paint(self, painter, options, widget)
        