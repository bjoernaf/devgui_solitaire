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

    # Define card size and corner rounding
    # TODO: Smartare size?
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
        '''
        Returns a bounding rectangle covering the entire card.
        '''
        return QRectF(0, 0, self.cardWidth, self.cardHeight)
    
    def mousePressEvent(self, event):
        '''
        Override mousePressEvent
        When the mouse is pressed, change the cursor to a closed hand.
        '''
        self.setCursor(Qt.ClosedHandCursor)
        self.com.signal.emit(self.color, self.value, self.pos())
        QGraphicsItem.mousePressEvent(self, event)
        
    def mouseReleaseEvent(self, event):
        '''
        Override mouseReleaseEvent
        Changes cursor to open hand.
        '''
        self.setCursor(Qt.OpenHandCursor)
        QGraphicsItem.mouseReleaseEvent(self, event)
    
    def mouseMoveEvent(self, event):
        '''
        This is called when an object is moved with the mouse pressed down.
        A drag event and a pixmap is created. The pixmap is attached to a painter
        that paints the card while it is being dragged.
        '''
        
        #Create a drag event with attached mime data containing the card id
        drag = QDrag(event.widget())
        mime = QMimeData()
        drag.setMimeData(mime)
        mime.setText(str(self.id))
        
        # Signal emitted when target of drop changes (to none specifically)
        drag.targetChanged.connect(self.tcSlot)
        
        # Set drag stack to show on top to avoid repainting NOT NESSECARY?
        #self.gsc.solWin.bView.dragCardStackView.setZValue(1)
        
        # TODO: RIMLIGT ATT ANVANDA PARENT? --BJORN
        # Emit a signal to the controller that a card is being moved
        self.com.moveCardSignal.emit(self.parentItem().stackId, boardStacks.boardStacks.DragCard, self.id)
        
        # Show the dragCardStackView (tempStack)
        self.parentItem().show()
        
        # TODO: Old paint method, remove when sure it won't be needed
        '''
        # Create a pixmap to paint the moving card on
        pixmap = QPixmap(self.cardWidth, self.cardHeight)
        pixmap.fill(Qt.transparent)
        
        # Create a painter for the pixmap
        painter = QPainter(pixmap)
        
        # Translate coord system (snygg flytt indikation typ)
        #painter.translate(5,5)
        
        # Call the paint function with the created painter
        self.paint(painter, 0)
        painter.end()
        
        # Set Pixmap and HotSpot to mouse location
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos().toPoint())
        '''
        
        #Execute drag etc
        drag.exec_()
        self.setCursor(Qt.OpenHandCursor)
        
    def dragEnterEvent(self, event):
        '''
        Run when a drag object enters the bounding rectangle of a card.
        Forward event to the parent of the card, the stack it's currently on.
        '''
        self.parentItem().dragEnterEvent(event)
    
    def dropEvent(self, event):
        '''
        Run when an accepted event is dropped on the card.
        Forward event to the parent of the card, the stack it's currently on.
        '''
        self.parentItem().dropEvent(event)
    
    def paint(self, painter, option, widget=None): 
        '''
        Override of the default paint function.
        Draws a rounded rectangle representing a card.
        Draws card number and card color symbol in upper
        and lower right corner.
        '''
        # Set opacity to paint entire card with
        painter.setOpacity(self.gsc.opacity/100.0)
        
        # Set pen and color to paint card with
        painter.setPen(Qt.black)
        painter.setBrush(Qt.white)
        
        # Paint a rounded, anti-aliased rectangle representing the card
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
                
    def tcSlot(self, target):
        '''
        Slot receiving signal when target of QDrag is changed.
        If target is None, drop has not happened and move to tempStack should be undone.
        '''
        # If drop has failed
        if target == None:
            # Undo move to temp stack
            self.gsc.undo()
            # Hide the drag stack again
            self.gsc.solWin.bView.dragCardStackView.hide()

    
    def __init__(self, gameStateController, color, value, cardId):
        '''
        Constructor:
        Creates a Card in the GraphicsView.
        Also loads the appropriate image for the card.
        '''
        super(cardView, self).__init__()
        
        # Create communicator, move somewhere else???
        self.com = communicator.communicator()
        # Connect slot (signalInterpreter) to signal (com.signal)
        self.com.signal.connect(gameStateController.signalInterpreter)
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        
        # Store color, value and card id
        self.color = color
        self.value = value
        self.id = cardId
        
        # Save game state controller instance
        self.gsc = gameStateController  
        
        # Load image
        self.loadImage(self.color)  

        # Set flags (flag | flag | flag...) and cursor type       
        self.setFlag(self.ItemIsMovable)
        self.setCursor(Qt.OpenHandCursor)
        
        # TODO: Currently not working to drop on cards.
        # If enabled, tries to drop on self since tempStack is at mouse location with self as card
        #self.setAcceptDrops(True)
        