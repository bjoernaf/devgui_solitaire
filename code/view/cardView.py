'''
Created on 7 apr 2014

@author: Sven, Bjorn
cardView is an QGraphicsRectItem representing a card. 
'''
from model import boardStacks

from PyQt5.QtCore import (
    Qt,
    QRectF,
    QMimeData,
    #QPoint
)
from PyQt5.QtGui import (
    #QFont,
    QDrag,
    QPixmap,
    #QFont, QColor, QPen, QPixmap, QPainter, QBrush
    QPainter
)
from PyQt5.QtWidgets import QGraphicsItem
from view import communicator

class cardView(QGraphicsItem):
    '''
    Class to create and display one single card in the QGraphicsView
    '''

    ## TODO: Smartare size
    cardWidth = 80
    cardHeight = 120
    cardXRad = 9.0
    cardYRad = 9.0
    
    # Opacity flag used in paint function
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
        
        # TODO: Make object invisible during drag
        #self.setVisible(False)
        
        #Create a drag event and a mime to go with it??
        drag = QDrag(event.widget())
        mime = QMimeData()
        drag.setMimeData(mime)
        mime.setText(str(self.id))
        
        # TODO: RIMLIGT ATT ANVANDA PARENT? --BJORN
        self.com.moveCardSignal.emit(self.parentItem().stackId, boardStacks.boardStacks.DragCard, self.id)
        
        # Create a pixmap to paint the move on
        pixmap = QPixmap(self.cardWidth, self.cardHeight)
        pixmap.fill(Qt.transparent)
        
        # Create a painter for the pixmap
        painter = QPainter(pixmap)
        
        # Translate coord system (snygg flytt indikation typ)
        #painter.translate(5,5)
        
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
 
 
    def mouseReleaseEvent(self, event):
        '''
        Override mouseReleaseEvent to send signal, then call default
        '''
        print("card mouse release event")
        #self.com.signal.emit(self.color, self.value, self.pos())
        self.setCursor(Qt.OpenHandCursor)
        QGraphicsItem.mouseReleaseEvent(self, event)
        
    
    def paint(self, painter, option, widget=None): 
        '''
        Override of the default paint function to draw a rounded rectangle instead of a regular rectangle
        '''
        painter.setOpacity(self.opacity)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(0, 0, self.cardWidth, self.cardHeight, self.cardXRad, self.cardYRad, Qt.AbsoluteSize)
        
        #TODO print in correct color etc
        painter.drawText(5, 15, str(self.value))

    
    def __init__(self, gameStateController, color, value, cardId):
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
        self.color = color
        self.value = value
        self.id = cardId     
        
        # ???
        self.shape()
        
        self.setFlags(QGraphicsItem.ItemIsSelectable);
        self.setFlag(QGraphicsItem.ItemIsMovable);
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges);
        self.setCursor(Qt.OpenHandCursor)
        