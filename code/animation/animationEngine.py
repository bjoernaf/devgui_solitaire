'''
Created on 12 May 2014

@author: Sven, Martin
'''

from PyQt5.QtCore import QObject, QTimer, QThread
from PyQt5.QtWidgets import QApplication
from animation import flippingCardsAnimation
from controller import communicator

class animationEngine(QObject):
    '''
    An engine controlling animations to be performed.
    The engine can handle several types of animations through
    different lists that are iterated over each time a timer
    timeouts. The respective animation function for each object
    is called upon to perform one step of the animation.
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
        Sets up a timer to sync animations and creates lists to contain objects
        that require animation.
        '''
        
        self.flipping = list()
        self.pulsating = list()

        # Animation timer
        self.timer = QTimer()
        # Connect timer signal to slot
        self.timer.timeout.connect(self.animate)
        # Start timer with 60+ timeouts per second
        self.timer.start(15)
        
        
    def animate(self):
        '''
        Call animation method for objects in animation lists
        '''
        # For all objects in list flipping, call flip
        for obj in self.flipping:
            obj.flip()
        # For all objects in list pulsating, call pulsate
        for obj in self.pulsating:
            obj.pulsate()
        
        
    def addFlippingCards(self, cardList, startStack, endStack, startPosX, startPosY, endPosX,
                         cardOffsetX, cardWidth, cardHeight, scaleStep):
        '''
        Create a flipping cards animation and add it to the list flipping.
        '''
        print("animationEngine/addFlippingCards: MY THREAD IS ", QThread.currentThread())
        print("animationEngine/addFlippingCards: MY MAIN THREAD IS ", QApplication.instance().thread())
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
        
        self.flipping.append(animation)
        
        
    def removeFlipping(self, obj):
        '''
        If obj is in list flipping, remove it.
        '''
        if obj in self.flipping:
            self.flipping.remove(obj)
        
        
    def addPulsating(self, obj):
        '''
        Add obj to list of obj that pulsate when animated
        '''
        self.pulsating.append(obj)
        
        
    def removePulsating(self, obj):
        '''
        If obj is in list pulsating, remove it
        '''
        if obj in self.pulsating:
            self.pulsating.remove(obj)