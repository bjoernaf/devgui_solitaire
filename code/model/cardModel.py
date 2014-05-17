'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

class cardModel(object):
    '''
    classdocs
    '''
    # Martin: The lines below don't seem to do anything useful,
    # so I comment them out.
#    color = None
#    value = None
#    faceup = False
    
    def __init__(self, color, value, faceup = False):
        '''
        Constructor
        '''
        self.color = color
        self.value = value
        self.faceup = faceup
            
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
        
    def faceIsUp(self):
        '''
        Returns faceup value
        '''
        return self.faceup