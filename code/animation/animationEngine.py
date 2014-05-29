'''
Created on 12 maj 2014

@author: Sven, Martin
'''

from PyQt5.QtCore import QTimer
from animation import flippingCardsAnimation
from controller import communicator

class animationEngine(object):
    '''
    An engine controlling animations to be performed.
    The engine can handle several types of animations through
    different lists that are iterated over each time a timer
    timeouts. The respective animation function for each object
    is called upton to perform one step of the animation.
    '''

    def __init__(self, gameStateController):
        '''
        Constructor, sets up a timer to sync animations and
        create lists to contain objects that require animation.
        '''
        super(animationEngine, self).__init__()
        
        self.gameStateController = gameStateController
        
        # Lists of items to animate
        self.rotating = list()
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
        # For all objects in list rotating, call rotate
        for obj in self.rotating:
            obj.rotate()
        # For all objects in list flipping, call flip
        for obj in self.flipping:
            obj.flip()
        # For all objects in list pulsating, call pulsate
        for obj in self.pulsating:
            obj.pulsate()
            
    def addRotating(self, obj):
        '''
        Add obj to list rotating
        '''
        self.rotating.append(obj)
        
    def removeRotating(self, obj):
        '''
        If obj is in list rotating, remove it.
        '''
        if obj in self.rotating:
            self.rotating.remove(obj)
            
    def addFlippingCards(self, cardList, startStack, endStack, startPos, endPos,
                         cardOffsetX, scaleStep):
        '''
        Create a flipping cards animation and add it to the list flipping.
        '''
        animation = flippingCardsAnimation.flippingCardsAnimation(cardList,
                                                                  startStack,
                                                                  endStack,
                                                                  startPos,
                                                                  endPos,
                                                                  cardOffsetX,
                                                                  scaleStep,
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
