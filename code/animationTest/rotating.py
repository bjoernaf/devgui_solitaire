'''
Created on 12 maj 2014

@author: Sven
'''

from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt

class rotating(object):
    '''
    classdocs
    '''
    def __init__(self, animationObject, parent):
        '''
        Constructor
        '''
        super(rotating, self).__init__()
        self.ao = animationObject
        self.tf = QTransform()
        self.parent = parent
        
        
    def animate(self):
        '''
        animerar
        '''
        self.tf.rotate(1)
        self.ao.setTransform(self.tf)
        self.parent.update()
        