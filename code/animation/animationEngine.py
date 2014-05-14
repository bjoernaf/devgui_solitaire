'''
Created on 12 maj 2014

@author: Sven, Martin
'''

from PyQt5.QtCore import QTimer

class animationEngine(object):
    '''
    stuff
    '''

    def __init__(self):
        '''
        Constructor, sets up a timer to sync animations.
        '''
        super(animationEngine, self).__init__()
        
        # Animation timer
        self.timer = QTimer()
        # Connect timer signal to slot
        self.timer.timeout.connect(self.animate)
        
        # Lists of items to animate
        self.rotating = list()
        self.flipping = list()
        
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
        