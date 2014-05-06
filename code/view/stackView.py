'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
'''

from model import boardStacks

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import (QGraphicsItem)
from view import communicator, cardView

class stackView(QGraphicsItem):
    '''
    Class to display stacks
    '''
    
    penWidth = 4
    width = 90
    height = 130
    xRadius = 9
    yRadius = 9
    
    rectx = penWidth/2
    recty = penWidth/2 
    rectWidth = width + penWidth
    rectHeight = height + penWidth

    def __init__(self, parent, gameStateController, stackId, x_offset = 0, y_offset = 5, faceUp = True):
        '''
        Constructor
        '''
        super(stackView, self).__init__()
        
        # The id of the stack (negative int as defined in boardStacks)
        self.stackId = stackId

        # The cards in the stack.
        self.stackCardList = list()
        
        self.offset_x = x_offset
        self.offset_y = y_offset
        self.parent = parent
        
        # Create communicator
        self.com = communicator.communicator()
        # Connect slot (moveCard) to signal (com.moveCardSignal).
        # Call as self.com.moveCardSignal.emit(fromStack, toStack, cardID)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        
        # Accept drops on the stacks
        self.setAcceptDrops(True)
        
        #Create and add cards (move to stackView)
        #card3 = cardView.cardView(gameStateController)
        #card = cardView.cardView(gameStateController)
        print(parent)
        parent.cardList[2].setPos(5,5)
        parent.cardList[2].setParentItem(self)
#        card3.setPos(350,150)
        #card.setPos(5, 5)
        #card.setParentItem(self)
        

    def boundingRect(self):
        '''
        Override defining the bounding rectangle for a stack
        '''
        return QRectF(self.rectx, self.recty,
                      self.rectWidth, self.rectHeight) 
    
        
    def getStackId(self):
        '''
        Returns stackId
        '''
        return self.stackId

    def paint(self, painter, option, widget=None):
        '''
        Override of paint function. Paints a custom rounded rectangle
        representing a stack location.
        '''
        pen = QPen()
        pen.setStyle(Qt.DashLine)
        pen.setColor(Qt.white)
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawRoundedRect(0, 0, 90, 130, 9.0, 9.0, Qt.AbsoluteSize)
        painter.setPen(Qt.white)
        
        
    def dragEnterEvent(self, event):
        '''
        Run when a drag object enters the bounding rectangle of a stack
        Set event to accepted, drop will then generate dropEvent
        '''
        if int(event.mimeData().text()) < 52:
            event.setAccepted(True)
            print("Event drop accepted")
        else:
            print("Event drop ignored")
            
    def dropEvent(self, event):
        '''
        DropEvent when an item is dropped on the stack
        '''
        print("Dropped cardId " + event.mimeData().text())
        
        cardId = int(event.mimeData().text())
        
        # Update stack to add moved cards
        self.com.moveCardSignal.emit(boardStacks.boardStacks.DragCard, self.stackId, cardId)

    def updateStackList(self, cardList):
        '''
        Give the stack a new set of cards.
        '''
        
        self.stackCardList = cardList
        self.setParents()
        
    def setParents(self):
        offset_x = 0
        offset_y = 0
        for card in self.stackCardList:
            offset_x += self.offset_x
            offset_y += self.offset_y
            self.parent.cardList[card].setPos(offset_x, offset_y)
            self.parent.cardList[card].setParentItem(self)
        self.update()