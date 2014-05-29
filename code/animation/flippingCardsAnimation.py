'''
Created on 18 maj 2014

@author: martin
'''

from PyQt5.QtCore import QPointF

from view import communicator

class flippingCardsAnimation(object):
    '''
    An animation that shows cards flipping to the right (from one stack to another).
    '''


    def __init__(self, cardList, startStack, endStack, startPos, endPos,
                 cardOffsetX, scaleStep, gameStateController, animationEngine):
        '''
        Constructor
        '''
        self.cardList = cardList
        self.startStack = startStack
        self.endStack = endStack
        self.startPos = startPos
        self.endPos = endPos
        self.cardOffsetX = cardOffsetX
        self.gameStateController = gameStateController
        self.animationEngine = animationEngine
        self.scaleStep = scaleStep
        
        # Set which card to flip first
        self.cardListIndex = 0

        topCard = self.cardList[0] # All cards to be flipped are supposed to have the same size
        self.cardWidth = topCard.getCardWidth()
        self.cardHeight = topCard.getCardHeight()

        # Rotate the cards so that the flipping will be performed
        # in the right direction
        newXCardPosition = self.startPos.x() + self.cardWidth
        newYCardPosition = self.startPos.y() + self.cardHeight        
        for card in self.cardList:
            card.setRotation(180)
            card.setPos(newXCardPosition, newYCardPosition)

        # Set the position where half of the flipping should be performed and
        # the distance to move the card in each step
        self.middlePos = QPointF(newXCardPosition + (self.endPos.x() - newXCardPosition) / 2,
                                 self.startPos.y())
        self.moveStep = (self.middlePos.x() - newXCardPosition) * -self.scaleStep
        
        self.com = communicator.communicator()
        self.com.turnCardSignal.connect(self.gameStateController.turnCard)
        self.com.moveCardSignal.connect(self.gameStateController.moveCard)
        self.com.endFlipMacroSignal.connect(self.gameStateController.endFlipMacro)

        
    def flip(self):
        '''
        Performs one step in the flipping animation and removes the animation
        from the animation engine if the end of the animation has been reached.
        '''
        flipCard = self.cardList[self.cardListIndex]
        transform = flipCard.transform()
        scaleFactor = transform.m11() + self.scaleStep
        
        if scaleFactor <= 0.0: # Flipping of current card is half-finished 
            self.com.turnCardSignal.emit(flipCard.id)
            flipCard.setRotation(0)
            flipCard.setZValue(self.cardListIndex) # The end stack is supposed to be empty
            scaleFactor = 0.0
            flipCard.setPos(self.middlePos)
            self.scaleStep = -self.scaleStep
        elif scaleFactor >= 1.0: # Flipping of current card is finished
            scaleFactor = 1.0
            flipCard.setPos(self.endPos)
        else:
            newPos = QPointF(flipCard.scenePos().x() + self.moveStep,
                             flipCard.scenePos().y())
            flipCard.setPos(newPos)
        
        transform.setMatrix(scaleFactor, transform.m12(), transform.m13(),
                            transform.m21(), transform.m22(), transform.m23(),
                            transform.m31(), transform.m32(), transform.m33())
        flipCard.setTransform(transform)
        
        # If the current card flipping is finished, move to the next card
        # to be flipped. If all cards have been flipped, stop the animation
        # and update the model.
        if scaleFactor == 1.0:
            if self.cardListIndex == len(self.cardList) - 1:
                self.animationEngine.removeFlipping(self)
                self.com.moveCardSignal.emit(self.startStack, self.endStack,
                                             flipCard.id)
                self.com.endFlipMacroSignal.emit()
            else:
                self.cardListIndex = self.cardListIndex + 1
                self.scaleStep = -self.scaleStep
                self.middlePos = QPointF(self.middlePos.x() + self.cardOffsetX / 2,
                                         self.startPos.y())
                self.endPos = QPointF(self.endPos.x() + self.cardOffsetX, self.startPos.y())
                self.moveStep = (self.middlePos.x() - (self.startPos.x() + self.cardWidth)) * -self.scaleStep