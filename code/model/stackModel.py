'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

class stackModel(object):
    '''
    Class describing a stack
    '''

    ### TODO: upsideDown? Se API nar det ar skrivet

    def __init__(self):
        '''
        Constructor
        '''
        self.stack = []
        
    def putCard(self, card):
        '''
        Puts a card on the stack
        '''
        self.stack.append(card)
        
    def drawCard(self):
        '''
        Draws the top card from the stack
        '''
        return self.stack.pop()
    
    def splitStack(self, numCards):
        '''
        splits a stack by drawing numCards of cards from the top, returning a stack with the top numCards cards.
        '''
        returnStack = []
        for i in range(1, numCards):
            returnStack.append(self.stack.pop())
        returnStack.reverse()
        
        return returnStack
    
    def appendStack(self, appStack):
        '''
        Appends appStack to the end of stack.
        '''
        self.stack.extend(appStack)
    