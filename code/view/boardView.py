'''
Created on 7 apr 2014

@author: Sven, Bjorn, Martin
'''

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem
from view import cardView, stackView, boardScene, communicator, glassView
from model import boardStacks
from animation import animationEngine

class boardView(QGraphicsView):
    '''
    boardView is a QGraphicsView representing a solitaire board.
    The boardView contains a QGraphicsScene that displays stacks
    (created in stackView.py) of cards (created in cardView.py).
    '''
    
        
    def __init__(self, windowWidth, windowHeight, gameStateController):
        '''
        Constructor:
        Creates cards (cardView) and adds them to cardList.
        Creates a graphicsScene, calls drawContent and sets the scene
        as active scene in boardView.
        '''
        super(boardView,self).__init__()
        
        # List to store all cards in
        self.cardList = list()
        
        # Create cards in cardList
        index = 0
        for color in range(1, 5):
            for number in range(1, 14):
                self.cardList.append(cardView.cardView(gameStateController,
                                                       self, color, number,
                                                       index, False))
                index += 1
        
        # Store a reference to gameStateController
        self.gameStateController = gameStateController
        
        #=======================================================================
        # # Create an animation engine and push it onto a new thread
        # self.animationEngine = animationEngine.animationEngine(self.gameStateController, self)
        # self.animationThread = QThread()
        # self.animationEngine.moveToThread(self.animationThread)
        # 
        # # Start the new thread and thereby the animation engine
        # self.animationThread.started.connect(self.animationEngine.startEngine)
        # self.animationThread.start()
        #=======================================================================
        
        # Create a communicator and connect relevant signals to slots
        self.com = communicator.communicator()
        self.com.moveCardSignal.connect(gameStateController.moveCard)
        self.com.addFlipAnimationSignal.connect(gameStateController.addFlipAnimation)

        # Create a scene based on the parent's size
        self.scene = boardScene.boardScene(0, 0, windowWidth, windowHeight, self)
        
        # Ensure initialization of opacity.
        self.setOpacity(100)
        
        # Store card style and back image
        self.cardStyle = "Detailed"
        self.cardBackImage = "backRed"
        
        # Call drawContent to draw stacks etc, then set scene as active in the view (boardView)
        self.drawContent(gameStateController)
        self.setScene(self.scene)
    
    def updateAllCards(self, cardFaceUp):
        '''
        Slot for signal which updates the facing of all cards in cardList,
        and sets their movable flag to the value of faceup.
        '''
        # Loop over all cards
        for cardId in range(0, 52):
            # set new faceup value for cardId and repaint it
            self.cardList[cardId].faceup = cardFaceUp[cardId]
            self.cardList[cardId].update()
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
        Slot for signal which updates the facing of one card,
        and sets it's movable flag to the value of faceUp.
        Also calls for a card tooltip update.
        '''
        print("Received update signal for card " + str(cardId))
        self.cardList[cardId].faceup = not self.cardList[cardId].faceup
        self.cardList[cardId].setFlag(QGraphicsItem.ItemIsMovable, self.cardList[cardId].faceup)
        self.cardList[cardId].updateToolTip()   
        
    def updateStacks(self, stacks):
        '''
        Slot for an update signal in Controller.
        @param stacks: The card stack structure
        Calls for each stack to update the list of cards
        belonging to that stack.
        '''
        print("BOARDVIEW : updateStacks: New stacks from MODEL:", stacks)
        
        # Clear the temp stack.
        self.clearTempStack()
        
        # Iterate over all stacks
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

        # Enable interaction (actually only necessary if the update is the result of a flip,
        # which disables interaction)
        items = self.scene.items()
        for item in items:
            item.setEnabled(True)
                
                
    def drawContent(self, gameStateController):
        '''
        Adds glassView and all stacks to the scene.
        '''
        
        #Set background color to dark green
        self.scene.setBackgroundBrush(Qt.darkGreen)
        
        # Add glass pane tutorial to boardview.
        self.glassView = glassView.glassView(gameStateController, self, self.width(), self.height())
        self.glassView.setPos(1, 1)
        self.glassView.setZValue(100) # Just to show on top of rest, 100 not important.
        self.glassView.hide()
        self.tutorialVisible = False
        self.scene.addItem(self.glassView)
        
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
        '''
        Flips up to three cards from stack Deck to stack Drawable.
        '''
        
        # Disables scene interaction during the flip
        items = self.scene.items()
        for item in items:
            item.setEnabled(False)
        
        # Detach the correct number of cards to flip from the Deck
        oldDeckStack = self.deckStackView.getStack()
        oldDeckStackLength = len(oldDeckStack)
        if oldDeckStackLength < 3:
            flipNumber = oldDeckStackLength
        else:
            flipNumber = 3
        splitIndex = oldDeckStackLength - flipNumber
        newDeckStack = oldDeckStack[:splitIndex]
        self.deckStackView.updateStackList(newDeckStack)

        # Create a list of the cards to flip
        flipCards = list()
        for i in range(splitIndex, oldDeckStackLength):
            flipCardId = oldDeckStack[i]
            flipCard = self.cardList[flipCardId]
            scenePos = flipCard.scenePos()         
            flipCard.setParentItem(None)
            flipCard.setPos(scenePos) # Seems necessary in order to stop the card from moving
            flipCard.hoverLeaveEvent(0) # Forces removal from pulsating animation list.
            flipCards.append(flipCardId)
        flipCards.reverse()

        # Find the start and end position of the flip
        startPos = self.cardList[oldDeckStack[0]].scenePos()
        startPosX = startPos.x()
        startPosY = startPos.y()
        drawableStackPosition = self.drawableStackView.scenePos()
        endPos = QPointF(drawableStackPosition.x() + self.drawableStackView.getDistanceX(),
                         drawableStackPosition.y() + self.drawableStackView.getDistanceY())
        endPosX = endPos.x()
        
        # Find the x offset between subsequent cards in the end stack
        cardOffsetX = self.drawableStackView.getCardOffsetX()

        # Find the size of the cards to flip (all cards are supposed to have the same size)
        topCard = self.cardList[flipCards[0]]
        cardWidth = topCard.getCardWidth()
        cardHeight = topCard.getCardHeight()

        # Determines how quick the animation is
        scaleStep = -0.05
        
        # Pass the cards to flip, the start stack, the end stack, the start position,
        # the end position, the card offset, the card size, and the scale step to the
        # animation engine
        self.com.addFlipAnimationSignal.emit(flipCards, boardStacks.boardStacks.Deck,
                                             boardStacks.boardStacks.Drawable,
                                             startPosX, startPosY, endPosX, cardOffsetX,
                                             cardWidth, cardHeight, scaleStep)
        
        
    def setCardZValue(self, flipCardId, zValue):
        '''
        Sets the z value of a card.
        '''
        
        card = self.cardList[flipCardId]
        card.setZValue(zValue)     
        
        
    def transformCard(self, flipCardId, pos, rotation, scaleFactor):
        '''
        Moves, rotates and scales a card (as part of a flipping animation).
        '''
        
        card = self.cardList[flipCardId]
        card.setPos(pos)
        card.setRotation(rotation)
        transform = card.transform()
        transform.setMatrix(scaleFactor, transform.m12(), transform.m13(),
                            transform.m21(), transform.m22(), transform.m23(),
                            transform.m31(), transform.m32(), transform.m33())
        card.setTransform(transform)

    
    def pulsateCard(self, cardId, blurRadius):
        '''
        Makes a card take one step in a pulsating animation.
        '''
        
        card = self.cardList[cardId]
        card.pulsate(blurRadius)


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
        
        self.tempStackRoot = cardid
        self.tempStackFromStack = stackid
        
    
    def cancelTempStack(self):
        '''
        Return the data on the temp stack to the stack it came from.
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
        Clear the tempStack.
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
            print("STACKVIEW : TEMPSTACK: Error")
        

    def splitStackOnCard(self, cardid, stack):
        '''
        INTERNAL: Split a stack list, returning both halves, where the second list
        starts at cardid.
        '''
        if(cardid in stack):
            return (stack[0:stack.index(cardid)], stack[stack.index(cardid):])
                
                
    def resizeEvent(self, event):
        '''
        Override of resizeEvent.
        Forwards resizeEvent to scene and glassView
        to ensure the size relation is kept.
        '''
        self.scene.resizeEvent(event)
        self.glassView.resizeEvent(event)
        QGraphicsView.resizeEvent(self, event)


    def repaintCards(self):
        '''
        Trigger a repaint (update()) of all cards in boardView.
        '''
        for card in self.cardList:
            card.update()


    def setOpacity(self, opacity):
        '''
        Set the opacity of cards, then trigger a repaint of all cards.
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
        Also acts as receiving slot from control panel theme selection.
        '''
        self.backImage = QImage("images/" + image + self.cardStyle + ".png")
        if self.backImage != None:
            # Scale image to fit card
            self.backImage = self.backImage.scaled(80, 120, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            print("BOARDVIEW : ERROR loading back image.")
        # Trigger repaint of all cards
        self.repaintCards()
        
        
    def setFrontImage(self, image):
        '''
        Iterates over all cards and calls setImage.
        Also acts as receiving slot from control panel card selection.
        '''
        # Store card style
        self.cardStyle = image
        for card in self.cardList:
            card.setImage(image)

    def showTutorial(self):
        '''
        Shows tutorial window on top of everything else.
        Sets visible flag to True.
        '''
        self.glassView.show()
        self.tutorialVisible = True
        
    def hideTutorial(self):
        '''
        Hides tutorial window and sets visible flag to False.
        '''
        self.glassView.hide()
        self.tutorialVisible = False
        
    def isTutorialVisible(self):
        '''
        Returns the value of tutorialVisible
        '''
        return self.tutorialVisible
    
    def updateFeedbackWindow(self, feedback):
        '''
        Call for tempStack to display a window with card move info feedback.
        '''
        self.tempStackView.updateFeedbackWindow(feedback)
        
    def hideFeedbackWindow(self):
        '''
        Call for tempStack to hide the feedback window.
        '''
        self.tempStackView.hideFeedbackWindow()
        
    def updatePaintColor(self, color):
        '''
        Sets the paint color of the tempStack to color
        '''
        self.tempStackView.updatePaintColor(color)
