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
from view import cardView, stackView, boardScene
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
        centerText.setPos(310, 170)
        self.scene.addItem(centerText)
        
        #Set background color to dark green
        self.scene.setBackgroundBrush(Qt.darkGreen)
        
        # Create stacks as
        # stackView.stackView(parent, gameStateController, boardStacks.boardStacks.STACKID, x-offset, y-offset, [faceUp])
        self.deckStackView = stackView.stackView(self, gameStateController,
                                                 boardStacks.boardStacks.Deck, 0, 0, False)
        self.deckStackView.setPos(10, 10)
        self.scene.addItem(self.deckStackView)
        
        self.drawableStackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Drawable, 8, 0)
        self.drawableStackView.setPos(120, 10)
        self.scene.addItem(self.drawableStackView)

        self.topLLStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopLL, 0, 0)
        self.topLLStackView.setPos(340, 10)
        self.scene.addItem(self.topLLStackView)        

        self.topMLStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopML, 0, 0)
        self.topMLStackView.setPos(450, 10)
        self.scene.addItem(self.topMLStackView)
        
        self.topMRStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopMR, 0, 0)
        self.topMRStackView.setPos(560, 10)
        self.scene.addItem(self.topMRStackView)
        
        self.topRRStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopRR, 0, 0)
        self.topRRStackView.setPos(670, 10)
        self.scene.addItem(self.topRRStackView)

        self.bottom1StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom1)
        self.bottom1StackView.setPos(10, 240)
        self.scene.addItem(self.bottom1StackView)        

        self.bottom2StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom2)
        self.bottom2StackView.setPos(120, 240)
        self.scene.addItem(self.bottom2StackView)
        
        self.bottom3StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom3)
        self.bottom3StackView.setPos(230, 240)
        self.scene.addItem(self.bottom3StackView)
        
        self.bottom4StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom4)
        self.bottom4StackView.setPos(340, 240)
        self.scene.addItem(self.bottom4StackView)

        self.bottom5StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom5)
        self.bottom5StackView.setPos(450, 240)
        self.scene.addItem(self.bottom5StackView)
        
        self.bottom6StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom6)
        self.bottom6StackView.setPos(560, 240)
        self.scene.addItem(self.bottom6StackView)
        
        self.bottom7StackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Bottom7)
        self.bottom7StackView.setPos(670, 240)
        self.scene.addItem(self.bottom7StackView)
        
        # The dragCardStack with no location and temporarily hidden
        self.dragCardStackView = stackView.stackView(self, gameStateController, boardStacks.boardStacks.DragCard)
        self.scene.addItem(self.dragCardStackView)
        self.dragCardStackView.hide()    

    def __init__(self, windowWidth, windowHeight, gameStateController):
        '''
        Constructor:
        Creates a graphicsScene, calls drawContent and sets the scene as active scene in boardView
        '''
        super(boardView,self).__init__()
        
        # List to store all cards in
        self.cardList = list()
        
        # Create cards in cardList
        index = 0
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardView.cardView(gameStateController, color, number, index))
                index += 1

        # Create a scene based on the parent's size
        self.scene = boardScene.boardScene(0, 0, windowWidth, windowHeight, gameStateController)
        
        # Call drawContent to draw stacks etc, then set scene as active in the view (boardView)
        self.drawContent(gameStateController)
        self.setScene(self.scene)
        
    def updateStacks(self, stacks):
        '''
        Slot for signal in controller. Receives new stack content if changes have occured.
        Notifies each stack of it's new content.
        '''
        print("BOARDVIEW: ", stacks)
        
        for key in stacks.keys():
            if(key == boardStacks.boardStacks.Deck):
                self.deckStackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Drawable):
                self.drawableStackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.TopLL):
                self.topLLStackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.TopML):
                self.topMLStackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.TopMR):
                self.topMRStackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.TopRR):
                self.topRRStackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom1):
                self.bottom1StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom2):
                self.bottom2StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom3):
                self.bottom3StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom4):
                self.bottom4StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom5):
                self.bottom5StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom6):
                self.bottom6StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.Bottom7):
                self.bottom7StackView.updateStackList(stacks[key])
            elif(key == boardStacks.boardStacks.DragCard):
                self.dragCardStackView.updateStackList(stacks[key])
                
                
    def resizeEvent(self, event):
        '''
        Override of resizeEvent called from solWin to match size
        '''
        #print("BOARDVIEW: ResizeEvent")
        self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
        #print("BOARDVIEW: Actual size:", self.scene.width(), self.scene.height())
        QGraphicsView.resizeEvent(self, event)
