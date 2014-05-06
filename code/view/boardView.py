'''
Created on 7 apr 2014

@author: Sven, Bjorn

boardView is a QGraphicsView representing a solitaire board.
The boardView contains a QGraphicsScene that displays stacks (created in stackView.py) of cards (created in cardView.py).

'''

# Can remove lots of imports later, might use some of them soon
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QFont)
from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsScene, QGraphicsView)
from view import cardView, stackView

class boardView(QGraphicsView):
    '''
    classdocs
    '''
        
    def drawContent(self, gameStateController):
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
#        centerText.setPos(180,120)
        centerText.setPos(270, 170)
        self.scene.addItem(centerText)
        
        #Set background color to dark green
        self.scene.setBackgroundBrush(Qt.darkGreen)
        
        #TODO Add stacks
        
        #Create and add cards (move to stackView)
        card1 = cardView.cardView(gameStateController)
#        card1.setPos(10,10)
        card1.setPos(600, 10)
        self.scene.addItem(card1)
        
        #Create and add cards (move to stackView)
        card2 = cardView.cardView(gameStateController)
#        card2.setPos(25,30)
        card2.setPos(615, 30)
        self.scene.addItem(card2)
        
        #Create and add cards (move to stackView)
        #card3 = cardView.cardView(gameStateController)
        card3 = cardView.cardView(gameStateController)
#        card3.setPos(350,150)
        card3.setPos(630, 50)
        self.scene.addItem(card3)
        
        deckStackView = stackView.stackView(gameStateController)
        deckStackView.setPos(10, 120)
        self.scene.addItem(deckStackView)

        topLLStackView = stackView.stackView(gameStateController)
        topLLStackView.setPos(120, 10)
        self.scene.addItem(topLLStackView)        

        topMLStackView = stackView.stackView(gameStateController)
        topMLStackView.setPos(230, 10)
        self.scene.addItem(topMLStackView)
        
        topMRStackView = stackView.stackView(gameStateController)
        topMRStackView.setPos(340, 10)
        self.scene.addItem(topMRStackView)
        
        topRRStackView = stackView.stackView(gameStateController)
        topRRStackView.setPos(450, 10)
        self.scene.addItem(topRRStackView)

        bottomLLStackView = stackView.stackView(gameStateController)
        bottomLLStackView.setPos(120, 240)
        self.scene.addItem(bottomLLStackView)        

        bottomMLStackView = stackView.stackView(gameStateController)
        bottomMLStackView.setPos(230, 240)
        self.scene.addItem(bottomMLStackView)
        
        bottomMRStackView = stackView.stackView(gameStateController)
        bottomMRStackView.setPos(340, 240)
        self.scene.addItem(bottomMRStackView)
        
        bottomRRStackView = stackView.stackView(gameStateController)
        bottomRRStackView.setPos(450, 240)
        self.scene.addItem(bottomRRStackView)

    def __init__(self, windowWidth, windowHeight, gameStateController):
        '''
        Constructor:
        Creates a graphicsScene, calls drawContent and sets the scene as active scene in boardView
        '''
        super(boardView,self).__init__()
        

        # Create a scene based on the parent's size
        # TODO TODO Scene never grows so far, fix resize event
        self.scene = QGraphicsScene(0, 0, windowWidth, windowHeight)
        
        # Call drawContent to draw stacks etc, then set scene as active in the view (boardView)
        self.drawContent(gameStateController)
        self.setScene(self.scene)
        
    def updateStacks(self, stacks):
        '''
        Slot for signal in controller. Receives new stack content if changes have occured.
        '''
                
    def resizeEvent(self, event):
        '''
        Override of resizeEvent called from solWin to match size
        '''
        #print("BOARDVIEW: ResizeEvent")
        self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
        #print("BOARDVIEW: Actual size:", self.scene.width(), self.scene.height())
        QGraphicsView.resizeEvent(self, event)
