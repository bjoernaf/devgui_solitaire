'''
Created on 7 April 2014

@author: Sven, Bjorn, Martin
'''

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QColor, QImage
from PyQt5.QtWidgets import QGraphicsItem
from view import communicator, feedbackWindow
from model import boardStacks

class stackView(QGraphicsItem):
    '''
    Class extending QGraphicsItem.
    stackView is a stack to place cards (cardView) on.
    '''
    
    # Stack size and attributes
    penWidth = 4
    width = 90.0
    height = 130.0
    xRadius = 9
    yRadius = 9
    
    # Bounding rectangle size
    rectx = penWidth/2
    recty = penWidth/2 
    rectWidth = width + penWidth
    rectHeight = height + penWidth
    
    # Distances between stack edge and bottom card
    distance_x = 5
    distance_y = 5


    def __init__(self, boardView, gameStateController, stackId,
                 x_offset = 0, y_offset = 30, faceUp = True):
        '''
        Constructor:
        Creates a stack containing a list to place cards in.
        '''
        super(stackView, self).__init__()
        
        # The id of the stack (negative int as defined in boardStacks)
        self.id = stackId

        # The cards in the stack.
        self.stackCardList = list()
        
        # Set card placement rules.
        self.offset_x = x_offset
        self.offset_y = y_offset
        
        # Set up parent objects
        self.boardView = boardView
        self.gameStateController = gameStateController
        
        # Create communicator
        self.com = communicator.communicator()
        
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        
        # Accept drops on the stacks unless stack is the deck or the tempStack
        if self.id != boardStacks.boardStacks.tempStack:
            self.setAcceptDrops(True)
            
        # Load image to use as stack edge
        self.loadImage()
        
        # If the stack is tempStack, create a feedbackWindow but hide it
        if self.id == boardStacks.boardStacks.tempStack:
            self.feedbackWindow = feedbackWindow.feedbackWindow("", self)
            self.feedbackWindow.setPos(90,0)
            self.feedbackWindow.setZValue(90)
            self.feedbackWindow.hide()
        
        # Color to use for all cards in the stack
        self.paintColor = Qt.white
        
        
    def updateStackList(self, cardList):
        '''
        Slot called by controller when the model has changed.
        Gives the stack a new set of cards.
        '''
        # Store received list and update properties for each card in the list
        self.stackCardList = cardList
        self.setParents()

        # If the stack is empty
        if self.stackCardList == []:
            # If the stack is a topStack
            if self.id <= boardStacks.boardStacks.TopLL and self.id >= boardStacks.boardStacks.TopRR:
                self.setToolTip("Place an Ace here.")
            # If the stack is a bottomStack
            elif self.id <= boardStacks.boardStacks.Bottom1 and self.id >= boardStacks.boardStacks.Bottom7:
                self.setToolTip("Place a King here.")
        else:
            self.setToolTip("")
        
        
    def getid(self):
        '''
        Returns stack id
        '''
        return self.id
    
        
    def getStack(self):
        '''
    	Returns the card list of the stack.
    	'''
        return self.stackCardList
    
    
    def getDistanceX(self):
        '''
        Returns the x distance between the stack edge and the bottom card.
        '''
        return self.distance_x
    
    
    def getDistanceY(self):
        '''
        Returns the y distance between the stack edge and the bottom card.
        '''
        return self.distance_x
    
    
    def getCardOffsetX(self):
        '''
        Returns the x distance between subsequent cards in the stack.
        '''
        return self.offset_x
    
    
    def paint(self, painter, option, widget=None):
        '''
        Override of paint function. Paints a custom rounded rectangle
        representing a stack location.
        '''
        # Draw border for all stacks but Deck and tempStack
        if (self.id != boardStacks.boardStacks.tempStack and
            self.id != boardStacks.boardStacks.Deck):
            
            # If the border image exists, draw it
            if not self.image.isNull():
                painter.drawImage(self.boundingRect(), self.image)
            # Else, draw simplified border
            else:
                pen = QPen()
                pen.setStyle(Qt.DashLine)
                pen.setColor(Qt.white)
                pen.setWidth(4)
                painter.setPen(pen)
                painter.drawRoundedRect(0, 0, 90, 130, 9.0, 9.0, Qt.AbsoluteSize)
                painter.setPen(Qt.white)
        
        
    def boundingRect(self):
        '''
        Override defining the bounding rectangle for a stack
        to account for thicker painted borders
        '''
        return QRectF(-self.rectx, -self.recty,
                      self.rectWidth, self.rectHeight) 

        
    def dragEnterEvent(self, event):
        '''
        Run when a drag object enters the bounding rectangle of a stack
        Set event to accepted, drop will then generate dropEvent
        '''
        #If DragEvent originates from within Solitaire
        if event.source() != None:            
            
            # Check that it contains a valid card id as text
            if event.mimeData().hasText() and "," in event.mimeData().text():
                
                # Extract metadata from the card being moved
                rawMetaData = event.mimeData().text().split(",")
                cardId = int(rawMetaData[0])
                fromStack = int(rawMetaData[1])
                
                # Ask model whether the move is valid or not
                moveAllowed, declineReason = self.gameStateController.checkMove(fromStack, self.id, cardId)
                if moveAllowed == True:
                    # If move is allowed, accept the event and paint tempStack green
                    event.accept()
                else:
                    # If move is not allowed, display reason and paint tempStack red
                    event.ignore()
                    self.boardView.updateFeedbackWindow(declineReason)
                    self.boardView.updatePaintColor(QColor(255, 100, 100))
            else:
                # Ignore move if invalid object is being dragged
                event.ignore()
        else:
            # Ignore move if object dragged originates from outside of Solitaire
            event.ignore()
            
        QGraphicsItem.dragEnterEvent(self, event)
        
        
    def dropEvent(self, event):
        '''
        DropEvent when an item is dropped on the stack
        '''
        # Extract metadata from dropped card.
        rawMetaData = event.mimeData().text().split(",")
        cardId = int(rawMetaData[0])
        fromStack = int(rawMetaData[1])
        
        print("STACKVIEW : dropEvent: Dropped card (", cardId, ",", fromStack, ")")
        
        # Update stack to add moved cards, unless same stack.
        if(fromStack == self.id): # or self.id == boardStacks.boardStacks.Deck):
            self.boardView.cancelTempStack()
        else:
            self.boardView.clearTempStack()
            self.com.moveCardSignal.emit(fromStack, self.id, cardId)
        
        # Hide the drag stack again
        self.boardView.tempStackVisible(False)
        
        
    def setParents(self):
        '''
        Sets the stack as parent for all cards.
        Sets the position of the cards to display a stack properly.
        Makes sure the cards are displayed in the correct order.
        Sets movability and cursor of the cards.
        '''
        # Base offset for first card in a stack
        offset_x = self.distance_x
        offset_y = self.distance_y
        index = 0
        
        # Iterate over all cards on the stack. Set position, parents and flags.
        for card in self.stackCardList:
            self.boardView.cardList[card].setPos(offset_x, offset_y)
            self.boardView.cardList[card].setParentItem(self)
            self.boardView.cardList[card].setZValue(index)
            
            # Set the cursor of the card
            if (self.boardView.cardList[card].faceup == False or
                 (self.id == boardStacks.boardStacks.Drawable and card != self.topCardId())):
                self.boardView.cardList[card].setFlag(QGraphicsItem.ItemIsMovable, False)
                self.boardView.cardList[card].setCursor(Qt.ArrowCursor)
            else:
                self.boardView.cardList[card].setFlag(QGraphicsItem.ItemIsMovable, True)
                self.boardView.cardList[card].setCursor(Qt.OpenHandCursor)
            
            # Inherit drop capabilities from the stack
            self.boardView.cardList[card].setAcceptDrops(self.acceptDrops())
            
            # Update offset for next card
            offset_x += self.offset_x
            # Reduce Y Offset if too many cards are on the stack
            if len(self.stackCardList) > 7:
                offset_y += self.offset_y/(len(self.stackCardList)*0.14)
            else:
                offset_y += self.offset_y
                
            # Increase index
            index += 1
            
            # If the card is the top card, set its tooltip
            if card == self.stackCardList[-1]:
                self.boardView.cardList[card].updateToolTip()
            
        # Repaint stack
        self.update()
        
        
    def updatePos(self, pos):
        '''
        Updates the position of the stack to truePos.
        Should only be called for tempStack.
        '''
        # Translate received position to the middle of the stack, then update Pos
        x = pos.x() - self.width/2
        y = pos.y() - self.height/2
        truePos = QPointF(x, y)
        self.setPos(truePos)
        
        
    def topCardId(self):
        '''
        Returns the card id of the top card
        '''
        if self.stackCardList != []:
            return self.stackCardList[-1]
        
        
    def updateFeedbackWindow(self, reason):
        '''
        Updates the text of the feedbackWindow and shows it.
        '''
        self.feedbackWindow.setPlainText(reason)
        if not self.feedbackWindow.isVisible():
            self.feedbackWindow.show()
        
        
    def hideFeedbackWindow(self):
        '''
        Hides the feedbackWindow if it is visible.
        Calls paintColor to set white color.
        '''
        if self.feedbackWindow.isVisible():
            self.feedbackWindow.hide()
        
        if self.paintColor != Qt.white:
            self.updatePaintColor(Qt.white)
        
        
    def updatePaintColor(self, color):
        '''
        Sets the color the painter should use to
        paint all cards with.
        '''
        self.paintColor = color
        
        
    def loadImage(self):
        '''
        Loads the image to be used for the stack border-
        '''
        if self.id == boardStacks.boardStacks.Drawable:
            self.image = QImage("images/stackDrawable.png")
        else:
            self.image = QImage("images/stackRegular.png")