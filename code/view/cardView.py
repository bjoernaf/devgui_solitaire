'''
Created on 7 apr 2014

@author: Sven, Bjorn
cardView is an QGraphicsRectItem representing a card. 
'''

from PyQt5.QtCore import (
    Qt,
    QRectF,
    QMimeData,
    QPoint
)
from PyQt5.QtGui import (
    QFont,
    QDrag,
    QPixmap,
    #QFont, QColor, QPen, QPixmap, QPainter, QBrush
    QPainter,
    QCursor
)
from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsItem)
from view import communicator

import random

class cardView(QGraphicsItem):
    '''
    classdocs
    '''

    ## TODO: Smartare size
    cardWidth = 80
    cardHeight = 120
    cardXRad = 9.0
    cardYRad = 9.0
    
    opacity = 1.0


    def boundingRect(self):
        return QRectF(0, 0, self.cardWidth, self.cardHeight)
    
    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        self.com.signal.emit(self.color, self.value, self.pos())
        QGraphicsItem.mousePressEvent(self, event)
    
    def mouseMoveEvent(self, event):
        '''
        This is called when an object is moved with the mouse pressed down
        '''
        
        # Make object invisible during drag
        self.setVisible(False)
        
        #Create a drag event and a mime to go with it??
        drag = QDrag(event.widget())
        mime = QMimeData()
        drag.setMimeData(mime)
        mime.setText("Card")
        
        # Create a pixmap to paint the move on
        pixmap = QPixmap(self.cardWidth, self.cardHeight)
        
        # Create a painter for the pixmap
        painter = QPainter(pixmap)
        
        # Translate coord system (snygg flytt indikation typ)
        #painter.translate(5,5)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set opacity to 30%, paint and then set it to 100% again
        self.opacity = 0.3
        self.paint(painter, 0)
        painter.end()
        self.opacity = 1
        
        # Set Pixmap and HotSpot to mouse location
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos().toPoint())
        
        #Execute drag etc
        drag.exec_()
        self.setCursor(Qt.OpenHandCursor)
        
        QGraphicsItem.mouseMoveEvent(self, event)
 
 
    def mouseReleaseEvent(self, event):
        '''
        Override mouseReleaseEvent to send signal, then call default
        '''
        print("card mouse release event")
        #self.com.signal.emit(self.color, self.value, self.pos())
        self.setCursor(Qt.OpenHandCursor)
        QGraphicsItem.mouseReleaseEvent(self, event)
        
        
    def dropEvent(self, event):
        print("drop")
        self.opacity = 1.0
        
    def dragEnterEvent(self, event):
        print("drag")
    
    def paint(self, painter, option, widget=None): 
        '''
        Override of the default paint function to draw a rounded rectangle instead of a regular rectangle
        '''
        painter.setOpacity(self.opacity)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(0, 0, cardView.cardWidth, cardView.cardHeight, cardView.cardXRad, cardView.cardYRad, Qt.AbsoluteSize)
        txt = self.drawContent()
        painter.drawText(txt.boundingRect(), Qt.AlignCenter, txt.toPlainText())
           
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
        
        return cardNumber;
        
        #TODO add more stuff such as animation etc
    
    def __init__(self, gameStateController):
        '''
        Constructor:
        Creates the card with random color & value, then calls drawContent to draw items on the card
        '''
        super(cardView, self).__init__()
        
        # Create communicator, move somewhere else???
        self.com = communicator.communicator()
        # Connect slot (signalInterpreter) to signal (com.signal)
        self.com.signal.connect(gameStateController.signalInterpreter)
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        
        ## TODO: Anvand metoder i cardModel for getColor och getValue
        self.color = random.randint(1,4)
        self.value = random.randint(1,13)

        # Call function to draw stuff on the card        
        self.drawContent()       
        
        # ???
        self.shape()
        
        self.setFlags(QGraphicsItem.ItemIsSelectable);
        self.setFlag(QGraphicsItem.ItemIsMovable);
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges);
        self.setAcceptDrops(True)
        self.setCursor(Qt.OpenHandCursor)
        