'''
Created on 7 apr 2014

@author: Sven, Bjorn

boardView is a QGraphicsView representing a solitaire board.
The boardView contains a QGraphicsScene that displays stacks (created in stackView.py) of cards (created in cardView.py).

'''

# Can remove lots of imports later, might use some of them soon
from PyQt5.QtCore import (QLineF, QMimeData, QPoint, QPointF, qrand, QRectF,
        qsrand, Qt, QTime, QTimeLine)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QTransform, QFont)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView)
from view import cardView

class boardView(QGraphicsView):
    '''
    classdocs
    '''
        
    def drawContent(self):
        '''
        set up the graphics scene and add items to it (stacks eventually, for now cards)
        '''
        
        # This is just a nice font, use any font you like, or none
        font=QFont('Decorative')
        font.setPointSize(25)

        #Draw white text in the center of the window
        centerText=QGraphicsTextItem('Solitaire')
        centerText.setFont(font)
        centerText.setDefaultTextColor(Qt.white)
        centerText.setPos(180,120)
        self.scene.addItem(centerText)
        
        #Set background color to dark green
        self.scene.setBackgroundBrush(Qt.darkGreen)
        
        #TODO Add stacks
        
        #Create and add cards (move to stackView)
        card1 = cardView.cardView()
        card1.setPos(10,10)
        self.scene.addItem(card1)
        
        #Create and add cards (move to stackView)
        card2 = cardView.cardView()
        card2.setPos(15,15)
        self.scene.addItem(card2)
        
        #Create and add cards (move to stackView)
        card3 = cardView.cardView()
        card3.setPos(350,150)
        self.scene.addItem(card3)
        
        

    def __init__(self, windowWidth, windowHeight):
        '''
        Constructor:
        Creates a graphicsScene, calls drawContent and sets the scene as active scene in boardView
        '''
        super(boardView,self).__init__()

        # Create a scene based on the parent's size
        # TODO TODO Scene never grows so far, fix resize event
        self.scene = QGraphicsScene(0, 0, windowWidth, windowHeight)
        
        # Call drawContent to draw stacks etc, then set scene as active in the view (boardView)
        self.drawContent()
        self.setScene(self.scene)