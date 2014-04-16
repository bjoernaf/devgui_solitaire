'''
Created on 7 apr 2014

@author: Sven, Bjorn
cardView is an QGraphicsRectItem representing a card. 
'''

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsRectItem)

import random

class cardView(QGraphicsRectItem):
    '''
    classdocs
    '''

    ## TODO: Smartare size
    cardWidth = 80
    cardHeight = 120
    cardXRad = 9.0
    cardYRad = 9.0
    
    
    def paint(self, painter, option, widget=None): 
        '''
        Override of the default paint function to draw a rounded rectangle instead of a regular rectangle
        ''' 
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(0, 0, cardView.cardWidth, cardView.cardHeight, cardView.cardXRad, cardView.cardYRad, Qt.AbsoluteSize)
        
    # Override boundingRect ????
    
    def drawContent(self):
        '''
        Draw the contents of the card
        '''
        
        # Set font and size
        font=QFont('Decorative')
        font.setPointSize(8)
        
        #Add red card value to upper left corner of it's parent (self), TEMPORARY STUFF
        cardNumber = QGraphicsTextItem(str(self.value))
        cardNumber.setFont(font)
        cardNumber.setDefaultTextColor(Qt.red)
        cardNumber.setPos(3,3)
        cardNumber.setParentItem(self)
        
        #TODO add more stuff such as animation etc
    
    def __init__(self):
        '''
        Constructor:
        Creates the card with random color & value, then calls drawContent to draw items on the card
        '''
        super(cardView, self).__init__()
        
        ## TODO: Anvand metoder i cardModel for getColor och getValue
        self.color = random.randint(1,4)
        self.value = random.randint(1,13)

        # Call function to draw stuff on the card        
        self.drawContent()       
        
        # ???
        self.shape()