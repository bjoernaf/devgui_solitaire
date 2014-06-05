'''
Created on 5 June 2014

@author: Martin, Sven
'''

from PyQt5.QtCore import QObject
from animation import communicator


class pulsatingCardAnimation(QObject):
    '''
    An animation that makes the edge of a card pulsate.
    '''


    def __init__(self, cardId, boardView):
        '''
        Constructor
        '''
        super(pulsatingCardAnimation, self).__init__()
        
        self.cardId = cardId
        self.blurRadius = 1
        self.increaseBlurRadius = True
        
        self.com = communicator.communicator()
        self.com.pulsateCardSignal.connect(boardView.pulsateCard)
        
        
    def getCardId(self):
        '''
        Returns the id of the animated card.
        '''
        
        return self.cardId
        
        
    def step(self):
        '''
        Performs one step in the pulsating animation. The animation is implemented
        using a white QGraphicsDropShadowEffect where increased blurRadius blurs the edges
        of the effect.
        '''
        
        # If blur radius is not at edge values, increase or decrease it
        if self.blurRadius > 1 and self.blurRadius < 59:
            if self.increaseBlurRadius == True:
                self.blurRadius = self.blurRadius + 1
            else:
                self.blurRadius = self.blurRadius - 1
        # If blur radius has reached 1, change to increasing blur radius
        elif self.blurRadius == 1:
            self.increaseBlurRadius = True
            self.blurRadius = self.blurRadius + 1
        # If blur radius has reached 59, change to decreasing blur radius
        elif self.blurRadius == 59:
            self.increaseBlurRadius = False
            self.blurRadius = self.blurRadius - 1
        else:
            print("PULSATING CARD ANIMATION: Error, wrong blur radius!")
                    
        # Update the card view
        self.com.pulsateCardSignal.emit(self.cardId, self.blurRadius)