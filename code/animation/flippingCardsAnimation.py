'''
Created on 18 maj 2014

@author: martin
'''

from PyQt5.QtCore import QPointF

from view import communicator

class flippingCardsAnimation(object):
    '''
    An animation that shows cards flipping from one stack to another.
    '''


    def __init__(self, cardList, startStack, endStack, endPos,
                 scaleStep, gameStateController, animationEngine):
        '''
        Constructor
        '''
        self.cardList = cardList
        self.startStack = startStack
        self.endStack = endStack
        self.endPos = endPos
        self.gameStateController = gameStateController
        self.animationEngine = animationEngine

        self.scaleStep = scaleStep
        self.middlePos = QPointF(95 + (self.endPos.x() - 95) / 2, 15) # Do this in a less hard-coded way
        #print("Original middlePos: " + str(self.middlePos))
        self.moveStep = (self.middlePos.x() - 95) * -self.scaleStep # Do this in a less hard-coded way
        #print("Original moveStep: " + str(self.moveStep))
        
        self.cardListIndex = 0
        
        # Rotate the cards so that the flipping will be performed
        # in the right direction
        for card in self.cardList:
            card.setRotation(180)
            card.setPos(95, 135) # Do this in a less hard-coded way
        
        self.zValueList = list()
        for card in self.cardList:
            self.zValueList.append(card.zValue())
        self.zValueList.reverse()
        
        self.com = communicator.communicator()
        self.com.turnCardSignal.connect(self.gameStateController.turnCard)
        self.com.moveCardSignal.connect(self.gameStateController.moveCard)

        
    def flip(self):
        '''
        Performs one step in the flipping animation and removes the animation
        from the animation engine if the end of the animation has been reached.
        '''
        flipCard = self.cardList[self.cardListIndex]
#        print("METHOD flip")
#        print("Card: " + str(flipCard.id))
#        print("Position: " + str(flipCard.pos()))
#        print("Move step: " + str(self.moveStep))
        transform = flipCard.transform()
        scaleFactor = transform.m11() + self.scaleStep
#        print("Scale factor: " + str(scaleFactor))
        if scaleFactor <= 0.0: # Flipping of current card is half-finished 
#            print("Flipping half-finished.")
#            print("Current position: " + str(flipCard.pos()))
#            print("Middle position: " + str(self.middlePos))            
            self.com.turnCardSignal.emit(flipCard.id)
            flipCard.setRotation(0)
            flipCard.setZValue(self.zValueList[self.cardListIndex]) # Good?
            scaleFactor = 0.0
            flipCard.setPos(self.middlePos)
            self.scaleStep = -self.scaleStep
        elif scaleFactor >= 1.0: # Flipping of current card is finished
#            print("Flipping finished.")
#            print("Current position: " + str(flipCard.pos()))
#            print("End position: " + str(self.endPos))
            scaleFactor = 1.0
            flipCard.setPos(self.endPos)
        else:
            newPos = QPointF(flipCard.scenePos().x() + self.moveStep,
                             flipCard.scenePos().y())
            #print("newPos: " + str(newPos))
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
            else:
                self.cardListIndex = self.cardListIndex + 1
                #print("New cardListIndex: " + str(self.cardListIndex))
                self.scaleStep = -self.scaleStep
                # do below stuff in less hard-coded way
                self.middlePos = QPointF(self.middlePos.x() + 10, 15)
                #print("New middlePos: " + str(self.middlePos))
                self.endPos = QPointF(self.endPos.x() + 20, 15)
                #print("New endPos: " + str(self.endPos))
                self.moveStep = (self.middlePos.x() - 95) * -self.scaleStep
                #print("New moveStep: " + str(self.moveStep))