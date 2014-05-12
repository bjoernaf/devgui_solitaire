'''
Created on 12 maj 2014

@author: Sven
'''
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QRectF

class rectangle(QGraphicsItem):
    '''
    classdocs
    '''


    def __init__(self, x, y, width, height):
        '''
        Constructor
        '''
        super(rectangle,self).__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def boundingRect(self):
        return QRectF(self.x, self.y, self.width+2, self.height+2)
    
    def paint(self, painter, options, widget=None):
        pen = QPen()
        pen.setWidth(3)
        painter.setBrush(Qt.blue)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(self.x, self.y, self.width, self.height)
        