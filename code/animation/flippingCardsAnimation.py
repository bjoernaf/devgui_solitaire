'''
Created on 18 May 2014

@author: Martin
'''

from PyQt5.QtCore import QObject, QPointF, QThread
from PyQt5.QtWidgets import QApplication
from animation import communicator


class flippingCardsAnimation(QObject):
    '''
    An animation that shows cards flipping to the right (from one stack to another).
    '''


    def __init__(self, cardList, startStack, endStack, startPosX, startPosY, endPosX,
                 cardOffsetX, cardWidth, cardHeight, scaleStep, boardView, gameStateController,
                 animationEngine):
        '''
        Constructor
        '''
        super(flippingCardsAnimation, self).__init__()
        
        self.cardList = cardList
        self.startStack = startStack
        self.endStack = endStack
        self.startPosX = startPosX
        self.startPosY = startPosY
        self.cardOffsetX = cardOffsetX
        self.cardWidth = cardWidth
        self.scaleStep = scaleStep
        self.animationEngine = animationEngine

        # Set up all signals
        self.com = communicator.communicator()
        self.com.turnCardSignal.connect(gameStateController.turnCard)
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        self.com.endFlipMacroSignal.connect(gameStateController.endFlipMacro)
        self.com.transformCardSignal.connect(boardView.transformCard)
        self.com.setCardZValueSignal.connect(boardView.setCardZValue)
        
        # Set which card to flip first
        self.cardListIndex = 0

        self.flipCard = self.cardList[self.cardListIndex]
        
        # Set the original horizontal scaling
        self.scaleFactor = 1.0
        
        # Position and rotate the cards so that the flipping will be performed
        # in the right direction
        self.rotatedStartPos = QPointF(self.startPosX + self.cardWidth,
                                       self.startPosY + cardHeight)
        self.currentPos = self.rotatedStartPos
        self.rotation = 180
        for card in self.cardList:
            self.com.transformCardSignal.emit(card, self.currentPos, self.rotation,
                                              self.scaleFactor)

        # Set the position where half of the flipping should be performed and
        # the distance to move the card in each step
        self.middlePos = QPointF(self.currentPos.x() + (endPosX - self.currentPos.x()) / 2,
                                 self.startPosY)
        self.moveStep = (self.middlePos.x() - self.currentPos.x()) * -self.scaleStep
        
        # Set the end position
        self.endPos = QPointF(endPosX, self.startPosY)
        
        
    def step(self):
        '''
        Performs one step in the flipping animation and removes the animation
        from the animation engine if the end of the animation has been reached.
        '''
        print("flippingCardsAnimation/flip: MY THREAD IS ", QThread.currentThread())
        print("flippingCardsAnimation/flip: MY MAIN THREAD IS ", QApplication.instance().thread())

        self.scaleFactor = self.scaleFactor + self.scaleStep        
        
        if self.scaleFactor <= 0.0: # Flipping of current card is half-finished 
            self.com.turnCardSignal.emit(self.flipCard)
            self.currentPos = self.middlePos
            self.rotation = 0
            self.scaleFactor = 0.0
            self.scaleStep = -self.scaleStep
            self.com.setCardZValueSignal.emit(self.flipCard, self.cardListIndex)
                # The end stack is supposed to be empty, so this will place the cards
                # in the right order
        elif self.scaleFactor >= 1.0: # Flipping of current card is finished
            self.scaleFactor = 1.0
            self.currentPos = self.endPos
        else:
#            flipCard.testThread() # Temporarily added
            self.currentPos = QPointF(self.currentPos.x() + self.moveStep, self.currentPos.y())
            
        # Update the card view
        self.com.transformCardSignal.emit(self.flipCard, self.currentPos, self.rotation,
                                          self.scaleFactor)
        
        # If the current card flipping is finished, move to the next card
        # to be flipped. If all cards have been flipped, stop the animation
        # and update the model.
        if self.scaleFactor == 1.0:
            if self.cardListIndex == len(self.cardList) - 1:
                self.animationEngine.removeFlippingCards(self)
                self.com.moveCardSignal.emit(self.startStack, self.endStack, self.flipCard)
                self.com.endFlipMacroSignal.emit()
            else:
                self.cardListIndex = self.cardListIndex + 1
                self.flipCard = self.cardList[self.cardListIndex]
                self.currentPos = self.rotatedStartPos
                self.rotation = 180
                self.scaleStep = -self.scaleStep
                self.middlePos = QPointF(self.middlePos.x() + self.cardOffsetX / 2,
                                         self.startPosY)
                self.endPos = QPointF(self.endPos.x() + self.cardOffsetX, self.startPosY)
                self.moveStep = (self.middlePos.x() - (self.startPosX + self.cardWidth)) * -self.scaleStep