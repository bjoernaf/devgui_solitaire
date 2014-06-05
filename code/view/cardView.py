'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin 
'''

from PyQt5.QtCore import Qt, QRectF, QMimeData, QPointF, QSize
from PyQt5.QtGui import QDrag, QFont, QPainter, QImage, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsDropShadowEffect
from model import boardStacks
from view import communicator


class cardView(QGraphicsItem):
    '''
    cardView is a QGraphicsItem representing a playing card.
    '''

    # Define card size and corner rounding
    cardWidth = 80
    cardHeight = 120
    cardXRad = 9.0
    cardYRad = 9.0
    
    # Bounding rectangles to paint card number and images in
    boundingValueLeft = QRectF(4, 3, 12, 15)
    boundingValueRight = QRectF(-cardWidth + 4, -cardHeight + 3, 12, 15)
    imagePosLeft = QPointF(4, 16)
    imagePosRight = QPointF(-cardWidth + 4, -cardHeight + 16)
    imageSize = QSize(12,12) # Size of corner images


    def __init__(self, gameStateController, boardView, color, value, cardId, faceup):
        '''
        Constructor:
        Creates a card in the GraphicsView.
        '''
        super(cardView, self).__init__()
        
        # Create communicator to handle signals
        self.com = communicator.communicator()
        
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        self.com.turnCardSignal.connect(gameStateController.turnCard)
        self.com.reenterCardSignal.connect(gameStateController.reenterCard)
        self.com.beginFlipMacroSignal.connect(gameStateController.beginFlipMacro)
        self.com.addPulsatingAnimationSignal.connect(gameStateController.addPulsatingAnimation)
        self.com.removePulsatingAnimationSignal.connect(gameStateController.removePulsatingAnimation)
        
        # Store color, value, cardId and faceup status
        self.color = color
        self.value = value
        self.id = cardId
        self.faceup = faceup
        
        # Set front side type, True paints detailed image
        self.detailedFront = True
        
        # Save gameStateController and boardView instance
        self.gsc = gameStateController
        self.boardView = boardView
        
        # Load corner image (spades, hearts etc)
        self.loadImage(self.color)

        # Set item to accept hoverEvents
        self.setAcceptHoverEvents(True)
        
        # Set up effect to use when animating pulsate and connect it to the cardView
        self.pulsateEffect = QGraphicsDropShadowEffect()
        self.pulsateEffect.setColor(Qt.white)
        self.pulsateEffect.setOffset(0, 0)
        self.setGraphicsEffect(self.pulsateEffect)
    
    
    def getCardWidth(self):
        '''
        Returns the width of the card.
        '''
        return self.cardWidth
    
    
    def getCardHeight(self):
        '''
        Returns the height of the card.
        '''
        return self.cardHeight
    
    
    def illegalDropSlot(self, target):
        '''
        Slot receiving signal when target of QDrag is changed.
        If target is None, a legal drop has not happened and
        move to tempStack should be undone.
        '''
        # If drop has failed
        if target == None:
            # Undo move to temp stack
            self.boardView.tempStackVisible(False)
            print("CARDVIEW  : IllegalDropSlot: Illegal drop, cancel drag.")
            self.boardView.cancelTempStack()


    def mousePressEvent(self, event):
        '''
        Override mousePressEvent.
        Changes cursor style when appropriate.
        '''
        parentStack = self.parentItem()
        # Complicated way of checking if the standard cursor of the card is an open hand
        if (self.faceup == True and
            not (parentStack.getid() == boardStacks.boardStacks.Drawable and
                 self.id != parentStack.topCardId())):
            self.setCursor(Qt.ClosedHandCursor)
        QGraphicsItem.mousePressEvent(self, event)
    

    def mouseDoubleClickEvent(self, event):
        '''
        Override mouseDoubleClickEvent.
        '''
        # If card is in Deck
        if self.parentItem().getid() == boardStacks.boardStacks.Deck:
            # Begin a command macro, so that the whole process of flipping cards
            # from Deck to Drawable can be undone in one step
            self.com.beginFlipMacroSignal.emit()
            
            # Move all current cards from Drawable to Deck
            self.com.reenterCardSignal.emit()
            
            # Flip new cards from Deck to Drawable
            self.boardView.flipCards()
            
        # Else if the card is at the top of it's stack
        elif self.id == self.parentItem().topCardId():
            # Attempt to turn the card
            self.com.turnCardSignal.emit(self.id)   
            
        # Else, simply call super     
        else:
            QGraphicsItem.mouseDoubleClickEvent(self, event)

            
    def mouseReleaseEvent(self, event):
        '''
        Override mouseReleaseEvent.
        Changes cursor to open hand.
        '''
        self.setCursor(Qt.OpenHandCursor)
        QGraphicsItem.mouseReleaseEvent(self, event)
    
    
    def mouseMoveEvent(self, event):
        '''
        This is called when an object is moved with the mouse pressed down.
        A drag event is created with mimeData representing the card info.
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
    
        # Show the tempStack
        self.boardView.tempStackVisible(True)
    
        # Execute drag etc
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
        If card is facing down, draw back of card.
        '''
        # Set opacity to paint entire card with
        painter.setOpacity(self.boardView.cardOpacity/100.0)
        
        # Set painter rendering mode
        painter.setRenderHint(QPainter.Antialiasing)
        
        # If the card is facing up, draw card and details
        if(self.faceup == True):
            
            # If front side image exists and detailed mode is set
            if self.detailedFront == True and self.image.isNull() == False:
                # Draw detailed image
                if self.parentItem() != None:
                    # # Special color and opacity for tempStack when being dragged
                    if type(self.parentItem().paintColor) is QColor:
                        painter.setBrush(self.parentItem().paintColor)
                        painter.setOpacity(painter.opacity()*0.6)
                        painter.drawImage(self.boundingRect(), self.image)
                        painter.drawRoundedRect(self.boundingRect(), 3, 3, Qt.AbsoluteSize)
                    # If paintColor is white
                    else:
                        painter.drawImage(self.boundingRect(), self.image)
                else:
                    painter.drawImage(self.boundingRect(), self.image)
               
            # Else, paint simple front side
            else:
                # Paint a rounded, anti-aliased rectangle representing the card
                painter.setPen(Qt.black)
                painter.setBrush(Qt.white)
                
                # Special color and opacity for tempStack when being dragged
                if self.parentItem() != None:
                    if self.parentItem().id == boardStacks.boardStacks.tempStack:
                        if type(self.parentItem().paintColor) is QColor:
                            painter.setBrush(self.parentItem().paintColor)
                            painter.setOpacity(painter.opacity()*0.85)
    
                painter.drawRoundedRect(self.boundingRect(), self.cardXRad, self.cardYRad, Qt.AbsoluteSize)
        
                # Card value: Set font style and color
                font = QFont("Helvetica")
                font.setBold(True)
                painter.setFont(font)
                if self.color in range(2,4):
                    painter.setPen(Qt.red)
                
                # Paint upper left text and image
                painter.drawText(self.boundingValueLeft, Qt.AlignTop | Qt.AlignHCenter, self.toValueString(self.value))
                painter.drawImage(self.imagePosLeft, self.smallImage)
            
                #Paint lower right text and image
                painter.rotate(180)
                painter.drawText(self.boundingValueRight, Qt.AlignTop | Qt.AlignHCenter, self.toValueString(self.value))
                painter.drawImage(self.imagePosRight, self.smallImage)
            
        # If the card is facing down, draw the back image
        else:
            painter.drawImage(self.boundingRect(), self.boardView.backImage)
    
    
    def boundingRect(self):
        '''
        Returns a bounding rectangle covering the entire card.
        '''
        return QRectF(0, 0, self.cardWidth, self.cardHeight)
        
        
    def loadImage(self, color):
        '''
        Loads a large front side image and a small card color image.
        If small image is loaded successfully, it is scaled to proper size.
        '''
        # Load large image
        self.image = QImage("images/front/" + str(self.color) + str(self.value) + ".png")
        if self.image.isNull():

            print("CARDVIEW  : loadImage: Error loading front image " + str(self.color) + str(self.value) + ".png")
            
        # Load small image and scale if it exists
        self.smallImage = QImage("images/" + str(self.color) + "_simpleSmall.png")
        if self.smallImage.isNull():
            print("CARDVIEW  : loadImage: Error loading image" + str(self.color) + "_simpleSmall.png")
        else:
            self.smallImage = self.smallImage.scaled(self.imageSize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)   
        
        
    def setImage(self, imageType):
        '''
        Sets whether or not to paint detailed front side.
        '''
        if imageType == "Detailed":
            self.detailedFront = True
        else:
            self.detailedFront = False
        # Queue repaint of card
        self.update()
     

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
        Starts a pulsating animation.
        '''
        # If the card is the top card in the stack, start a pulsating animation.
        if self.parentItem() != None:
            if self.id == self.parentItem().topCardId():
                # Enable the pulsating animation effect
                self.pulsateEffect.setEnabled(True)

                # Make the animation engine animate the card
                self.com.addPulsatingAnimationSignal.emit(self.id)
        
        
    def hoverLeaveEvent(self, event):
        '''
        Catches when the mouse leaves the hover area above the cardView.
        Stops a pulsating animation.
        '''
        # Disable the pulsating animation effect and reset the blur radius
        self.pulsateEffect.setEnabled(False)
        self.pulsateEffect.setBlurRadius(1)
        
        # Stop the animation engine from animating the card
        self.com.removePulsatingAnimationSignal.emit(self.id)
        
        
    def pulsate(self, blurRadius):
        '''
        Makes the card take one step in a pulsating animation.
        The animation is implemented using a white QGraphicsDropShadowEffect
        where increased blurRadius blurs the edges of the effect.
        '''
        self.graphicsEffect().setBlurRadius(blurRadius)
        
        
    def updateToolTip(self):
        '''
        Updates tooltip of a card to display appropriate text.
        '''
        # If card faces up, show no tooltip
        if self.faceup == True:
            self.setToolTip("")
        else:
            self.setToolTip("Double-click to flip card")