'''
Created on 13 apr 2014

@author: Sven, Bjorn, Max
'''

'''
Basic imports, save to use later.
from PyQt5.QtCore import (QLineF, QMimeData, QPoint, QPointF, qrand, QRectF,
        qsrand, Qt, QTime, QTimeLine)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QTransform, QFont)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView, QApplication)
'''

from PyQt5.QtCore import (QSettings, QSize, QVariant, QPoint, Qt)
from PyQt5.QtWidgets import (QDialog, QAction, QLabel, QFrame, QVBoxLayout, QLabel)
from PyQt5.QtGui import QIcon

from view import boardView
from view import transSlider

class controlPanel(QDialog):
    '''
    Control panel dialog.
    '''
    
    winTitle = "Control panel"


    def __init__(self, boardView):
        '''
        Init function
        '''
        
        super(controlPanel,self).__init__()

        self.boardView = boardView

        self.setWindowTitle(self.winTitle)
        
        # Set up settings to store properties (width, height etc)
        settings = QSettings()
        
        self.frame = QFrame(self)
        self.layout = QVBoxLayout()
        
        self.label = QLabel('Card transparency:')
        
        # Create a transparency slider for the cards
        self.slide = transSlider.transSlider(self.boardView)
        self.slide.setFixedWidth(200)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slide)
        
        self.frame.setLayout(self.layout)
        
        # Get position, and move window accordingly
        position = settings.value("ControlPanel/Position", QVariant(QPoint(0, 0)))
        self.move(position)
        
    
    def showEvent(self, event):
        '''
        Overrides showEvent to set size of window on first open.
        '''
        self.adjustSize()
        self.setFixedSize(self.size())
        
    
    def closeEvent(self, event):
        '''
        Overrides closeEvent to provide confirm dialogue and save settings
        '''
        
        print("CONTROLPAN: Close control panel")
         