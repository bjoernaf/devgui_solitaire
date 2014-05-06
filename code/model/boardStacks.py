'''
Created on 6 maj 2014

@author: Sven, Bjorn, Martin
'''

class boardStacks(object):
    '''
    This class contains the id numbers of the stacks, for use in the internal representation and API
    to the board model itself.
    '''
    
    Deck = -1
    Drawable = -2
    
    TopLL = -11
    TopML = -12
    TopMR = -13
    TopRR = -14
    
    BottomLL = -21
    BottomML = -22
    BottomMR = -23
    BottomRR = -24
    
    DragCard = -30