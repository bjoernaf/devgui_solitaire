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
from model import boardStacks

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
        
        
        
        # Create stacks as
        # stackView.stackView(parent, gameStateController, boardStacks.boardStacks.STACKID, x-offset, y-offset, [faceUp])
        self.deckStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.Deck, 0, 0, False)
        self.deckStackView.setPos(10, 120)
        self.scene.addItem(self.deckStackView)
        
        self.drawableStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.Drawable, 8, 0)
        self.drawableStackView.setPos(10, 300)
        self.scene.addItem(self.drawableStackView)

        self.topLLStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.TopLL)
        self.topLLStackView.setPos(120, 10)
        self.scene.addItem(self.topLLStackView)        

        self.topMLStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.TopML)
        self.topMLStackView.setPos(230, 10)
        self.scene.addItem(self.topMLStackView)
        
        self.topMRStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.TopMR)
        self.topMRStackView.setPos(340, 10)
        self.scene.addItem(self.topMRStackView)
        
        self.topRRStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.TopRR)
        self.topRRStackView.setPos(450, 10)
        self.scene.addItem(self.topRRStackView)

        self.bottomLLStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.BottomLL)
        self.bottomLLStackView.setPos(120, 240)
        self.scene.addItem(self.bottomLLStackView)        

        self.bottomMLStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.BottomML)
        self.bottomMLStackView.setPos(230, 240)
        self.scene.addItem(self.bottomMLStackView)
        
        self.bottomMRStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.BottomMR)
        self.bottomMRStackView.setPos(340, 240)
        self.scene.addItem(self.bottomMRStackView)
        
        self.bottomRRStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.BottomRR)
        self.bottomRRStackView.setPos(450, 240)
        self.scene.addItem(self.bottomRRStackView)
        

    def __init__(self, windowWidth, windowHeight, gameStateController):
        '''
        Constructor:
        Creates a graphicsScene, calls drawContent and sets the scene as active scene in boardView
        '''
        super(boardView,self).__init__()
        
        self.cardList = list()
        # Create cards in cardList
        index = 0
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardView.cardView(gameStateController, color, number, index))
                index += 1
        
        # Get list of stacks
        

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
        print("BOARDVIREW: ", stacks)
        
        for key in stacks.keys():
            print(key)
            if(key == boardStacks.boardStacks.Deck):
                self.deckStackView.updateStackList(stacks[key])
            if(key == boardStacks.boardStacks.Drawable):
                self.drawableStackView.updateStackList(stacks[key])
            if(key == boardStacks.boardStacks.TopLL):
                self.topLLStackView.updateStackList(stacks[key])
                
    def resizeEvent(self, event):
        '''
        Override of resizeEvent called from solWin to match size
        '''
        #print("BOARDVIEW: ResizeEvent")
        self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
        #print("BOARDVIEW: Actual size:", self.scene.width(), self.scene.height())
        QGraphicsView.resizeEvent(self, event)
