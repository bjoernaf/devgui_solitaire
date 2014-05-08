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
    QSize,
    #QPoint
)
from PyQt5.QtGui import (
    QDrag,
    QPixmap,
    QFont, 
    #QColor, QPen, QBrush
    QPainter,
    QImage
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
       
    # Bounding rectangles to paint card number and images in
    boundingValueLeft = QRectF(4, 3, 12, 15)
    boundingValueRight = QRectF(-cardWidth+4, -cardHeight+3, 12, 15)
    boundingImageLeft = QRectF(5.3, 16, 10, 10)
    boundingImageRight = QRectF(-cardWidth+5.3, -cardHeight+16, 10, 10)


    def boundingRect(self):
        return QRectF(0, 0, self.cardWidth, self.cardHeight)
    
    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)
        self.com.signal.emit(self.color, self.value, self.pos())
        QGraphicsItem.mousePressEvent(self, event)
        print(self.gsc.opacity)
    
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
        self.paint(painter, 0)
        painter.end()
        
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
        painter.setOpacity(self.gsc.opacity/100.0)
        
        # Set pen and color to paint card with
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        
        # Paint a rounded anti-aliased rectangle and fill it with white representing the card
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(0, 0, self.cardWidth, self.cardHeight, self.cardXRad, self.cardYRad, Qt.AbsoluteSize)
        
        # Card value: Set font style and color
        font = QFont("Helvetica")
        font.setBold(True)
        painter.setFont(font)
        if self.color in range(2,4):
            painter.setPen(Qt.red)
            
        # Paint upper left text and image
        painter.drawText(self.boundingValueLeft, Qt.AlignTop | Qt.AlignHCenter, self.toStr(self.value))
        painter.drawImage(self.boundingImageLeft, self.image)
        
        #Paint lower right text and image
        painter.rotate(180)
        painter.drawText(self.boundingValueRight, Qt.AlignTop | Qt.AlignHCenter, self.toStr(self.value))
        painter.drawImage(self.boundingImageRight, self.image)
        
        
    def loadImage(self, color):
        '''
        Loads an image from file with color.png as filename.
        Stores image in self.image
        '''
        self.image = QImage("images/" + str(self.color) + "_small.png")
        self.image = self.image.scaledToHeight(10)
        if self.image.isNull():
            print("Error loading image")
            
    def toStr(self, value):
        '''
        Returns correct string corresponding to a card value
        '''
        return {
                1: "A",
                11: "J",
                12: "Q",
                13: "K",
                }.get(value, str(value))

    
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
        
        #save game state controller instance
        self.gsc = gameStateController  
        
        # Load image
        self.loadImage(self.color)  
        
        # ???
        self.shape()
        
        self.setFlags(QGraphicsItem.ItemIsSelectable);
        self.setFlag(QGraphicsItem.ItemIsMovable);
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges);
        self.setCursor(Qt.OpenHandCursor)
        