'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

class eventUndo(object):
    '''
    Stores past events on a stack for undo/redo
    '''
    
    eventStack = []


    def __init__(self):
        '''
        Constructor
        '''
        