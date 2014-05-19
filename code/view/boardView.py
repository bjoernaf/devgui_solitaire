'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin

boardView is a QGraphicsView representing a solitaire board.
The boardView contains a QGraphicsScene that displays stacks
(created in stackView.py) of cards (created in cardView.py).
'''

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem
from view import cardView, stackView, boardScene, communicator
from model import boardStacks
from animation import animationEngine

class boardView(QGraphicsView):
    '''
    classdocs
    '''
    
        
    def __init__(self, windowWidth, windowHeight, gameStateController):
        '''
        Constructor:
        Creates a graphicsScene, calls drawContent and sets the scene
        as active scene in boardView
        '''
        super(boardView,self).__init__()
        
        # List to store all cards in
        self.cardList = list()
        
        # Create cards in cardList
        index = 0
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardView.cardView(gameStateController,
                                                       self, color, number,
                                                       index, False))
                index += 1
        
        self.gameStateController = gameStateController
        
        self.com = communicator.communicator()
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        
        # Load image for back of cards, red as default
        self.setBackImage("backRed")
        
        # Create animationEngine
        self.animationEngine = animationEngine.animationEngine(gameStateController)

        # Create a scene based on the parent's size
        self.scene = boardScene.boardScene(0, 0, windowWidth, windowHeight, self)
        
        # Ensure initialization of opacity.
        self.setOpacity(100)
        
        # Call drawContent to draw stacks etc, then set scene as active in the view (boardView)
        self.drawContent(gameStateController)
        self.setScene(self.scene)
    
    def updateAllCards(self, cardFaceUp):
        '''
        Slot for signal which updates the facing of the cards
        '''
        for cardId in range(0, 52):
            self.cardList[cardId].faceup = cardFaceUp[cardId]
            # Update movable status depending on faceUp value
            # NOTE: Only if the card belongs to a stack
            if self.cardList[cardId].parentItem() != None:
                # If not in Deck, set correct itemIsMovable
                if self.cardList[cardId].parentItem().id != boardStacks.boardStacks.Deck:
                    self.cardList[cardId].setFlag(QGraphicsItem.ItemIsMovable, cardFaceUp[cardId])
                # Else, set itemIsMovable to false
                else:
                    self.cardList[cardId].setFlag(QGraphicsItem.ItemIsMovable, False)
    
    def updateCard(self, cardId):
        '''
        Slot for signal which updates the facing of one card
        '''
        self.cardList[cardId].faceup = not self.cardList[cardId].faceup
        self.cardList[cardId].setFlag(QGraphicsItem.ItemIsMovable, self.cardList[cardId].faceup)
        
        '''
        if self.cardList[cardId].parentItem() != None:
                # If not in Deck, set correct itemIsMovable
                if self.cardList[cardId].parentItem().id != boardStacks.boardStacks.Deck:
                    self.cardList[cardId].setFlag(QGraphicsItem.ItemIsMovable, self.cardList[cardId].faceup)
                # Else, set itemIsMovable to false
                else:
                    self.cardList[cardId].setFlag(QGraphicsItem.ItemIsMovable, False)
        '''
           
        
    def updateStacks(self, stacks):
        '''
        Slot for signal in controller. Receives new stack content if changes have
        occurred. Notifies each stack of its new content.
        '''
        print("BOARDVIEW : updateStacks: New stacks from MODEL:", stacks)
        
        # Clear the temp stack.
        self.clearTempStack()
        
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
                
            else:
                print("BOARDVIEW : UpdateStacks: INVALID STACK:", key)
                
                
    def drawContent(self, gameStateController):
        '''
        set up the graphics scene and add items to it
        '''
        
        #Draw white text in the center of the window
#        font=QFont('Decorative')
#        font.setPointSize(25)
#        centerText=QGraphicsTextItem('Solitaire')
#        centerText.setFont(font)
#        centerText.setDefaultTextColor(Qt.white)
#        centerText.setPos(310, 170)
#        self.scene.addItem(centerText)
        
        #Set background color to dark green
        self.scene.setBackgroundBrush(Qt.darkGreen)
        
        # Create stacks as
        # stackView.stackView(parent, gameStateController, boardStacks.boardStacks.STACKID, x-offset, y-offset, [faceUp])
        self.deckStackView = stackView.stackView(self, gameStateController,
                                                 boardStacks.boardStacks.Deck,
                                                 0, 0, False)
        self.deckStackView.setPos(10, 10)
        self.scene.addItem(self.deckStackView)
        
        self.drawableStackView = stackView.stackView(self, gameStateController,
                                                     boardStacks.boardStacks.Drawable,
                                                     20, 0)
        self.drawableStackView.setPos(120, 10)
        self.scene.addItem(self.drawableStackView)

        self.topLLStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopLL,
                                                  0, 0)
        self.topLLStackView.setPos(340, 10)
        self.scene.addItem(self.topLLStackView)        

        self.topMLStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopML,
                                                  0, 0)
        self.topMLStackView.setPos(450, 10)
        self.scene.addItem(self.topMLStackView)
        
        self.topMRStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopMR,
                                                  0, 0)
        self.topMRStackView.setPos(560, 10)
        self.scene.addItem(self.topMRStackView)
        
        self.topRRStackView = stackView.stackView(self, gameStateController,
                                                  boardStacks.boardStacks.TopRR,
                                                  0, 0)
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
        
        # The tempStack with no location and temporarily hidden
        self.tempStackView = stackView.stackView(self, gameStateController,
                                                 boardStacks.boardStacks.tempStack)
        self.scene.addItem(self.tempStackView)
        self.tempStackView.hide()
        # Initialize the tempstack
        self.clearTempStack()

    
    def flipCards(self):
        # Detach the cards to flip from the deck
        flipNumber = 3
        oldDeckStack = self.deckStackView.getStack()
        oldDeckStackLength = len(oldDeckStack)
        splitIndex = oldDeckStackLength - flipNumber
        newDeckStack = oldDeckStack[:splitIndex]
        self.deckStackView.updateStackList(newDeckStack)
        
        # Create a list of the cards to flip
        flipCards = list()
        for i in range(splitIndex, oldDeckStackLength):
            flipCardId = oldDeckStack[i]
            flipCard = self.cardList[flipCardId]
            flipCardPos = flipCard.scenePos() # Necessary?
            flipCard.setParentItem(None)
            flipCard.setPos(flipCardPos) # Necessary?
            flipCards.append(flipCard)
        flipCards.reverse()
        
        # Find the end position of the flip
        drawableStackPosition = self.drawableStackView.scenePos()
        drawableStackSize = len(self.drawableStackView.getStack())
        endPos = QPointF(drawableStackPosition.x() + 5 + 20 * drawableStackSize,
                         drawableStackPosition.y() + 5) # Do this less hard-codedly
        #print("endPos: " + str(endPos))
        
        # Pass the cards to flip, the start stack, the end stack,
        # and the end position to the animation engine
        scaleStep = -0.05
        self.animationEngine.addFlippingCards(flipCards, boardStacks.boardStacks.Deck,
                                              boardStacks.boardStacks.Drawable,
                                              endPos, scaleStep)
                

    def updateTempStack(self, cardid, stackid):
        '''
        Updates the contents of the temp stack.
        '''
        
        
        if(stackid == boardStacks.boardStacks.Deck):
            newStacks = self.splitStackOnCard(cardid, self.deckStackView.getStack())
            self.deckStackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Drawable):
            newStacks = self.splitStackOnCard(cardid, self.drawableStackView.getStack())
            self.drawableStackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.TopLL):
            newStacks = self.splitStackOnCard(cardid, self.topLLStackView.getStack())
            self.topLLStackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.TopML):
            newStacks = self.splitStackOnCard(cardid, self.topMLStackView.getStack())
            self.topMLStackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.TopMR):
            newStacks = self.splitStackOnCard(cardid, self.topMRStackView.getStack())
            self.topMRStackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.TopRR):
            newStacks = self.splitStackOnCard(cardid, self.topRRStackView.getStack())
            self.topRRStackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom1):
            newStacks = self.splitStackOnCard(cardid, self.bottom1StackView.getStack())
            self.bottom1StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom2):
            newStacks = self.splitStackOnCard(cardid, self.bottom2StackView.getStack())
            self.bottom2StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom3):
            newStacks = self.splitStackOnCard(cardid, self.bottom3StackView.getStack())
            self.bottom3StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom4):
            newStacks = self.splitStackOnCard(cardid, self.bottom4StackView.getStack())
            self.bottom4StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom5):
            newStacks = self.splitStackOnCard(cardid, self.bottom5StackView.getStack())
            self.bottom5StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom6):
            newStacks = self.splitStackOnCard(cardid, self.bottom6StackView.getStack())
            self.bottom6StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        elif(stackid == boardStacks.boardStacks.Bottom7):
            newStacks = self.splitStackOnCard(cardid, self.bottom7StackView.getStack())
            self.bottom7StackView.updateStackList(newStacks[0])
            self.tempStackView.updateStackList(newStacks[1])
        else:
            print("BOARDVIEW : UpdateTempStack: INVALID STACK!!", stackid)
            return
        
        # TODO: Purpouse of line below? Does not work unless commented
        #self.tempStackView.updateStackList([cardid])
        self.tempStackRoot = cardid
        self.tempStackFromStack = stackid
        
    
    def cancelTempStack(self):
        '''
        Return the data on the temp stack to the previous stack.
        '''
        
        if(self.tempStackRoot > 0):
        
            if(self.tempStackFromStack == boardStacks.boardStacks.Deck):
                self.deckStackView.updateStackList(self.deckStackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Drawable):
                self.drawableStackView.updateStackList(self.drawableStackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.TopLL):
                self.topLLStackView.updateStackList(self.topLLStackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.TopML):
                self.topMLStackView.updateStackList(self.topMLStackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.TopMR):
                self.topMRStackView.updateStackList(self.topMRStackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.TopRR):
                self.topRRStackView.updateStackList(self.topRRStackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom1):
                self.bottom1StackView.updateStackList(self.bottom1StackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom2):
                self.bottom2StackView.updateStackList(self.bottom2StackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom3):
                self.bottom3StackView.updateStackList(self.bottom3StackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom4):
                self.bottom4StackView.updateStackList(self.bottom4StackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom5):
                self.bottom5StackView.updateStackList(self.bottom5StackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom6):
                self.bottom6StackView.updateStackList(self.bottom6StackView.getStack() + self.tempStackView.getStack())
            elif(self.tempStackFromStack == boardStacks.boardStacks.Bottom7):
                self.bottom7StackView.updateStackList(self.bottom7StackView.getStack() + self.tempStackView.getStack())
            else:
                print("BOARDVIEW : CancelTempStack: INVALID STACK!!", self.tempStackFromStack)
                return
        
            self.clearTempStack()
    
    
    def clearTempStack(self):
        '''
        Clear the temporary stack.
        '''
        self.tempStackView.updateStackList([])
        self.tempStackRoot = -1
        
        
    def tempStackVisible(self, isVisible):
        '''
        Shows the tempStack if isVisible = True
        Hides the tempStack if isVisible = False
        '''
        if isVisible == True:
            self.tempStackView.show()
        elif isVisible == False:
            self.tempStackView.hide()
        else:
            print("Error")
        

    def splitStackOnCard(self, cardid, stack):
        '''
        INTERNAL: Split a stack list, returning both halves, where the second list
        starts at cardid.
        '''
        if(cardid in stack):
            return (stack[0:stack.index(cardid)], stack[stack.index(cardid):])
                
                
    def resizeEvent(self, event):
        '''
        Override of resizeEvent called from solWin to match size
        '''
        self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
        QGraphicsView.resizeEvent(self, event)
        
    def repaintCards(self):
        '''
        Trigger a repaint (update()) of all cards in boardView.
        '''
        for card in self.cardList:
            card.update()

    def setOpacity(self, opacity):
        '''
        Set the opacity of cards.
        '''
        
        self.cardOpacity = opacity
        self.repaintCards()
        
    def getOpacity(self):
    	'''
    	Returns the opacity of cards.
    	'''
    	return self.cardOpacity
 
    def setBackImage(self, image):
        '''
        Sets the back image according to images/image.png
        Also acts as receiving slot from control panel
        '''
        self.backImage = QImage("images/" + image + ".png")
        self.backImage = self.backImage.scaled(80, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.repaintCards()