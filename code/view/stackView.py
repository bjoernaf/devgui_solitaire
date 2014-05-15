'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
'''

from model import boardStacks

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import (QGraphicsItem)
from view import communicator, cardView

class stackView(QGraphicsItem):
    '''
    Class to display stacks
    '''
    
    penWidth = 4
    width = 90.0
    height = 130.0
    xRadius = 9
    yRadius = 9
    
    rectx = penWidth/2
    recty = penWidth/2 
    rectWidth = width + penWidth
    rectHeight = height + penWidth


    def __init__(self, boardView, gameStateController, id, x_offset = 0, y_offset = 5, faceUp = True):
        '''
        Constructor
        '''
        super(stackView, self).__init__()
        
        # The id of the stack (negative int as defined in boardStacks)
        self.id = id

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
        
        # Accept drops on the stacks unless stack is tempStack
        if self.id != boardStacks.boardStacks.tempStack:
            self.setAcceptDrops(True)
        
        
    def updateStackList(self, cardList):
        '''
        Slot called by controller when the model has changed.
        Gives the stack a new set of cards.
        '''
        self.stackCardList = cardList
        self.setParents()
        
        
    def getid(self):
        '''
        Returns id
        '''
        return self.id
        
    def getStack(self):
        '''
    	Returns the card list of the stack.
    	'''
        return self.stackCardList

    def paint(self, painter, option, widget=None):
        '''
        Override of paint function. Paints a custom rounded rectangle
        representing a stack location.
        '''
        if self.id != boardStacks.boardStacks.tempStack:
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
        '''
        return QRectF(self.rectx, self.recty,
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
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
            
            
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
        if(fromStack == self.id):
            self.boardView.cancelTempStack()
        else:
            self.boardView.clearTempStack()
            self.com.moveCardSignal.emit(fromStack, self.id, cardId)
        
        # Hide the drag stack again
        self.boardView.tempStackVisible(False)
        
        
    def setParents(self):
        '''
        Sets the stack as parent for all cards.
        Sets the position of the card to display a stack properly.
        Makes sure the cards are displayed in the correct order.
        '''
        offset_x = 5
        offset_y = 5
        index = 0
        for card in self.stackCardList:
            self.boardView.cardList[card].setPos(offset_x, offset_y)
            self.boardView.cardList[card].setParentItem(self)
            self.boardView.cardList[card].setZValue(index)
            offset_x += self.offset_x
            offset_y += self.offset_y
            index += 1
        self.update()
        
        
    def updatePos(self, pos):
        '''
        Called by boardScene, used to track mouse position
        '''
        # Translate received position to the middle of the stack, then update Pos
        x = pos.x() - self.width/2
        y = pos.y() - self.height/2
        truePos = QPointF(x, y)
        self.setPos(truePos)
                