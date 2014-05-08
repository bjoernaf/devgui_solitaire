'''
@author: Max
'''

'''
Basic imports, save to use later.
from PyQt5.QtCore import (QLineF, QMimeData, QPoint, QPointF, qrand, QRectF,
        qsrand, Qt, QTime, QTimeLine)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QTransform, QFont)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView, QApplication)
'''

from PyQt5.QtCore import (QSettings, QSize, QVariant, QPoint)
from PyQt5.QtWidgets import (QMainWindow, QAction, QMessageBox, QSlider, QVBoxLayout)
from PyQt5.Qt import Qt

slider_opacity = 100;

class TransSlider(QSlider):
    def __init__(self, gsc):
        super(TransSlider, self).__init__(Qt.Horizontal)
        self.gsc = gsc
    
    def mouseMoveEvent(self, pos):
        super(TransSlider, self).mouseMoveEvent(pos)
        self.gsc.opacity = self.sliderPosition()
        print("slider moved")
        print(self.sliderPosition())


class sliderWindow(QMainWindow):
    '''
    solitaireWindow is a QMainWindow. It has a menu
    '''

    def __init__(self, title, gameStateController):
        '''
        Init function, create a graphicsScene spawning a boardView and attach it to a graphicsView
        '''
               
        super(sliderWindow,self).__init__()
               
        self.sone = TransSlider(gameStateController)
        self.sone.setRange(0,100)
        self.sone.setValue(100)
        self.setCentralWidget(self.sone)
        self.setWindowTitle(title)
        #self.sone.valueChanged.connect(self.sliderChanged)
