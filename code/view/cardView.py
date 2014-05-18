'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
cardView is an QGraphicsItem representing a card. 
'''

from PyQt5.QtCore import Qt, QRectF, QMimeData
from PyQt5.QtGui import QDrag, QFont, QPainter, QImage
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsDropShadowEffect
from model import boardStacks
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
    boundingValueRight = QRectF(-cardWidth + 4, -cardHeight + 3, 12, 15)
    boundingImageLeft = QRectF(5.3, 16, 10, 10)
    boundingImageRight = QRectF(-cardWidth + 5.3, -cardHeight + 16, 10, 10)


    def __init__(self, gameStateController, boardView, color, value, cardId, faceup):
        '''
        Constructor:
        Creates a Card in the GraphicsView.
        Also loads the appropriate image for the card.
        '''
        super(cardView, self).__init__()
        
        # Create communicator, move somewhere else???
        self.com = communicator.communicator()
        
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        self.com.turnCardSignal.connect(gameStateController.turnCard)
        
        # Store color, value and card id
        self.color = color
        self.value = value
        self.id = cardId
        self.faceup = faceup
        
        # Save game state controller instance
        self.gsc = gameStateController
        self.boardView = boardView
        
        # Load image
        self.loadImage(self.color)

        self.setAcceptHoverEvents(True)
        # Martin: Since movability and cursor should depend on the current
        # stack of the card, the settings below has been moved to
        # stackView.setParents(). 
        # Set flags (flag | flag | flag...) and cursor type
#        self.setFlags(self.ItemIsMovable)
#        self.setCursor(Qt.OpenHandCursor)
        
        # TODO: Currently not working to drop on cards.
        # If enabled, tries to drop on self since tempStack is at mouse location with self as card
        #self.setAcceptDrops(True)
        
        # Set up effect to use when animating pulsate and connect it to the cardView
        self.pulsateEffect = QGraphicsDropShadowEffect()
        self.pulsateEffect.setColor(Qt.white)
        self.pulsateEffect.setOffset(0,0)
        self.pulsateIncrease = True # True increasing, False decreasing
        self.setGraphicsEffect(self.pulsateEffect)
        
        #print("card created")

    def illegalDropSlot(self, target):
        '''
        Slot receiving signal when target of QDrag is changed.
        If target is None, drop has not happened and move to tempStack should be undone.
        '''
        # If drop has failed
        if target == None:
            # Undo move to temp stack
            self.boardView.tempStackVisible(False)
            print("CARDVIEW  : IllegalDropSlot: Illegal drop, cancel drag.")
            self.boardView.cancelTempStack()


    def mousePressEvent(self, event):
        '''
        Override mousePressEvent
        When the mouse is pressed, change the cursor to a closed hand.
        '''
        if self.parentItem().getid() != boardStacks.boardStacks.Deck:
            self.setCursor(Qt.ClosedHandCursor)
        QGraphicsItem.mousePressEvent(self, event)
        
        #self.faceup = not self.faceup
        self.com.turnCardSignal.emit(self.id)
    

    def mouseDoubleClickEvent(self, event):
        if self.parentItem().getid() == boardStacks.boardStacks.Deck:
            self.boardView.flipCards()
        else:
            QGraphicsItem.mouseDoubleClickEvent(self, event)

            
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
        A drag event is created.
        '''
        
        # Create a drag event with attached mime data containing the card id and fromstack
        drag = QDrag(event.widget())
        mime = QMimeData()
        drag.setMimeData(mime)
        mime.setText(str(self.id) + "," + str(self.parentItem().id))
        
        # Signal emitted when target of drop changes (to none specifically)
        drag.targetChanged.connect(self.illegalDropSlot)
        
        # Put the dragged cards on the temp stack, to draw under mouse cursor.
        self.boardView.updateTempStack(self.id, self.parentItem().id)
        
        # Show the dragCardStackView (tempStack)
        self.boardView.tempStackVisible(True)
        
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
        if(self.faceup == True):
            painter.setBrush(Qt.white)
        else:
            painter.setBrush(Qt.red)
        
        # Paint a rounded, anti-aliased rectangle representing the card
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(0, 0, self.cardWidth, self.cardHeight, self.cardXRad, self.cardYRad, Qt.AbsoluteSize)

        if(self.faceup == True):        
            # Card value: Set font style and color
            font = QFont("Helvetica")
            font.setBold(True)
            painter.setFont(font)
            if self.color in range(2,4):
                painter.setPen(Qt.red)
                
            # Paint upper left text and image
            painter.drawText(self.boundingValueLeft, Qt.AlignTop | Qt.AlignHCenter, self.toValueString(self.value))
            painter.drawImage(self.boundingImageLeft, self.image)
        
            #Paint lower right text and image
            painter.rotate(180)
            painter.drawText(self.boundingValueRight, Qt.AlignTop | Qt.AlignHCenter, self.toValueString(self.value))
            painter.drawImage(self.boundingImageRight, self.image)
            
        
    def boundingRect(self):
        '''
        Returns a bounding rectangle covering the entire card.
        '''
        return QRectF(0, 0, self.cardWidth, self.cardHeight)    
    
    def loadImage(self, color):
        '''
        Loads an image from file with color.png as filename.
        Stores image in self.image
        '''
        self.image = QImage("images/" + str(self.color) + "_small.png")
        self.image = self.image.scaledToHeight(10)
        if self.image.isNull():
            print("CARDVIEW  : loadImage: Error loading image")
            
    def rotate(self):
        '''
        Rotate something
        '''
        print("Rotating...")
            
    def toValueString(self, value):
        '''
        Returns correct string corresponding to a card value
        '''
        return {
                1: "A",
                11: "J",
                12: "Q",
                13: "K",
                }.get(value, str(value))
             
    def hoverEnterEvent(self, event):
        '''
        Catches when the mouse enters the hover area above the cardView.
        '''
        # Add the card to the pulsating animation engine list
        self.boardView.animation.addPulsating(self)
        
    def hoverLeaveEvent(self, event):
        '''
        Catches when the mouse leaves the hover area above the cardView.
        '''
        # Remove the card from the pulsating animation engine list
        self.boardView.animation.removePulsating(self)
        self.resetAnimation()
        
    def pulsate(self):
        '''
        Animate the card to pulsate. The animation is implemented
        using a white QGraphicsDropShadowEffect where increased
        blurRadius blurs the edges of the effect.
        '''
        # Store the current blurRadius
        currentBlur = self.pulsateEffect.blurRadius()
        
        # If currentBlur is not at edge values, increase or decrease it
        if currentBlur > 0 and currentBlur < 59:
            if self.pulsateIncrease == True:
                self.pulsateEffect.setBlurRadius(currentBlur+1)
            else:
                self.pulsateEffect.setBlurRadius(currentBlur-1)
        # If currentBlur has reached 0, change to increasing Blur
        elif currentBlur == 0:
            self.pulsateIncrease = True
            self.pulsateEffect.setBlurRadius(currentBlur+1)
        # If currentblur has reached 59, change to decreasing Blur
        elif currentBlur == 59:
            self.pulsateIncrease = False
            self.pulsateEffect.setBlurRadius(currentBlur-1)
        else:
            print("CARDVIEW: PULSATE: Error, wrong blurRadius!")
        
        # Enable blur effect if disabled
        if self.pulsateEffect.isEnabled() == False:
            self.pulsateEffect.setEnabled(True)
        
    def resetAnimation(self):
        '''
        Resets all animations to original state.
        Add more animations if necessary.
        '''
        # Disable pulsating animation and reset it
        self.pulsateEffect.setEnabled(False)
        self.pulsateEffect.setBlurRadius(0)

