'''
Created on 12 May 2014

@author: Sven, Martin
'''

from PyQt5.QtCore import QObject, QTimer
from animation import flippingCardsAnimation, pulsatingCardAnimation

class animationEngine(QObject):
    '''
    An engine controlling animations to be performed.
    The engine can handle several types of animations through
    different lists that are iterated over each time a timer
    timeouts. A function in each animation is called
    to perform one step of the animation.
    '''

    def __init__(self, gameStateController, boardView):
        '''
        Constructor.
        '''
        super(animationEngine, self).__init__()
        
        self.gameStateController = gameStateController
        self.boardView = boardView
        
        
    def startEngine(self):
        '''
        Sets up a timer to synchronize animations and creates animation lists.
        Not done in the constructor, since creating objects there might make
        them end up on the wrong (main) thread.
        '''
        # Animation lists
        self.flippingCards = list()
        self.pulsatingCards = list()

        # Animation timer
        self.timer = QTimer()
        # Connect timer signal to slot
        self.timer.timeout.connect(self.animate)
        # Start timer with 60+ timeouts per second
        self.timer.start(15)
        
        
    def animate(self):
        '''
        Makes all animations perform one step.
        '''
        for animation in self.flippingCards:
            animation.step()
        
        for animation in self.pulsatingCards:
            animation.step()
        
        
    def addFlippingCards(self, cardList, startStack, endStack, startPosX, startPosY, endPosX,
                         cardOffsetX, cardWidth, cardHeight, scaleStep):
        '''
        Starts a flipping cards animation.
        '''
        animation = flippingCardsAnimation.flippingCardsAnimation(cardList,
                                                                  startStack,
                                                                  endStack,
                                                                  startPosX,
                                                                  startPosY,
                                                                  endPosX,
                                                                  cardOffsetX,
                                                                  cardWidth,
                                                                  cardHeight,
                                                                  scaleStep,
                                                                  self.boardView,
                                                                  self.gameStateController,
                                                                  self)
        
        self.flippingCards.append(animation)
        
        
    def removeFlippingCards(self, animation):
        '''
        Stops a flipping cards animation.
        '''
        if animation in self.flippingCards:
            self.flippingCards.remove(animation)
        
        
    def addPulsatingCard(self, cardId):
        '''
        Starts a pulsating card animation.
        '''
        animation = pulsatingCardAnimation.pulsatingCardAnimation(cardId, self.boardView)
        self.pulsatingCards.append(animation)
        
        
    def removePulsatingCard(self, cardId):
        '''
        Stops a pulsating card animation.
        '''
        for animation in self.pulsatingCards:
            if animation.getCardId() == cardId:
                self.pulsatingCards.remove(animation)