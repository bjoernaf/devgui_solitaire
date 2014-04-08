'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

class cardModel(object):
    '''
    classdocs
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
        