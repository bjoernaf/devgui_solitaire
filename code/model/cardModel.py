'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

class cardModel(object):
    '''
    Simple class to keep track of color and value for card. Used for rule checking.
    '''
    
    def __init__(self, color, value):
        '''
        Constructor
        '''
        self.color = color
        self.value = value
            
    def getColor(self):
        '''
        Returns card color
        '''
        return self.color
        
    def getValue(self):
        '''
        Returns card value
        '''
        return self.value
