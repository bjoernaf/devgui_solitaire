'''
Created on 7 April 2014

@author: Sven, Bjorn, Max, Martin
'''

from .cardModel import cardModel
from .communicator import communicator
from .boardStacks import boardStacks

# Allows us to randomize deck.
import random

class boardModel(object):
    '''
    The main part of the model, which keeps track of where the cards are located, and offers an interface
    to move cards between stacks.
    '''
    
    def __init__(self, gsController):
        '''
        Constructor
        '''
        # Set up communicator
        self.com = communicator()
        
        # Connect signals to slot
        self.com.updateStackSignal.connect(gsController.updateControllerStacks)
        self.com.updateCardSignal.connect(gsController.updateControllerCard)
        self.com.updateAllCardsSignal.connect(gsController.updateControllerAllCards)
        self.com.gameWonSignal.connect(gsController.gameWonSlot)
        
        #cardList contains a list of all cards present in the game, and is used to reference cards by id numbers.
        self.cardList = list()
        
        #cardOrderDict keeps a linked list-like representation of the neighbors of each card.
        #Representation: cardOrderDict[currentCard] = (previousCard, nextCard)
        self.cardOrderDict = dict()
        
        # cardFaceUp keeps a list of how the cards are facing (up/down)
        self.cardFaceUp = list()
        
        # Create cards in cardList and facing status
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardModel(color, number))
                self.cardFaceUp.append(False)
                       
        # Create deck of cards and notify view
        self.createSolitaireGame()
        self.com.updateAllCardsSignal.emit(self.cardFaceUp)
        self.com.updateStackSignal.emit(self.getStackDict())
    
    
    def checkWin(self):
        '''
        Checks if the board is in a winning state.
        '''
        
        # Count the number of cards in the top stacks (that are in order)
        count = 0
        for i in range(-14, -10):
            card = self.findRootCardInStack(i)
            if(card != None):
                count += 1 # Count the root card.
                while(self.cardOrderDict[card][1] == card+1):
                    card = self.cardOrderDict[card][1]
                    count += 1 # Count all the other cards on the stack.
                    
        # Debug message
        print("MODEL     : checkWin:", count, "of 52 cards in winning position.")
        
        # The game is won when all 52 cards are in the winning position
        return (count == 52)
    
    
    def checkMove(self, fromStack, toStack, card):
        '''
        The rule checking function. This could be abstracted into a rule class.
        '''
        # If target is source, allow move
        if fromStack == toStack:
            return True, ""
        # If target is Deck
        if(toStack == -1):
            return False, "Can't place cards on this stack!"
        # If target is Drawable
        elif(toStack == -2):
            return False, "Can't place cards on this stack!"
        
        # If target is one of the top stacks
        elif(toStack >= -14 and toStack <= -11): 
            #You may not move more than one card each time to the top stacks
            if(self.cardOrderDict[card][1] != None):
                return False, "Move one card at a time to this stack!"
            
            topCard = self.findTopCardInStack(toStack)
            
            if(topCard == None):
                # Only aces are accepted as first card
                if(self.cardList[card].value != 1):
                    return False, "Only an Ace can be placed at the bottom of this stack!"         
            else:
                # The cards must be the same color
                if(self.cardList[card].color != self.cardList[topCard].color):
                    return False, "Only cards of the same color allowed!"
                
                # The order must be increasing
                if(self.cardList[card].value - self.cardList[topCard].value != 1):
                    return False, "Cards must be placed in increasing order!"
        
        # Bottom stacks
        else:               
            topCard = self.findTopCardInStack(toStack)
            
            #Can't place a stack on a back-turned card.
            if(topCard == None):
                if(card != 12 and card != 25 and card != 38 and card != 51):
                    # Can only place kings as root of bottom stacks.
                    return False, "Only a King can be placed at the bottom of this stack!"           
            else:
                if(self.cardFaceUp[topCard] == False):
                    return False, "Flip this card first!"
                
                color1 = self.cardList[topCard].color
                indexdif = card - topCard
                
                #Is the card a king?   
                #only allow placing of cards of different color and value 1
                if(color1 == 1):
                    if(indexdif != 12 and indexdif != 25):
                        return False, "Cards in decreasing order only!"
                elif(color1 == 2):
                    if(indexdif != -14 and indexdif != 25):
                        return False, "Cards in decreasing order only!"
                elif(color1 == 3):
                    if(indexdif != -27 and indexdif != 12):
                        return False, "Cards in decreasing order only!"
                elif(color1 == 4):
                    if(indexdif != -14 and indexdif != -27):
                        return False, "Cards in decreasing order only!"
           
        return True, ""
    
    
    def turnCard(self, cardId): 
        '''
        Turns a card in the model if allowed.
        Signals the controller that the turn is completed.
        ''' 
        _, top = self.cardOrderDict[cardId]
        #If the card is turned upside down
        if self.cardFaceUp[cardId] == False:
            # If the card is the top card or the card is on the deck stack
            if top == None or self.findStackOfCard(cardId) == boardStacks.Deck:
                # Turn the card and emit the signal
                self.cardFaceUp[cardId] = True
                print("MODEL     : turnCard: Sending update signal to boardView.")
                self.com.updateCardSignal.emit(cardId)
        else:
            print("MODEL     : turnCard: Turning of card disallowed.")
    
    
    def turnCardUndo(self, cardId):
        '''
        Turns a card in the model back if allowed. (RE-turn, result of undo)
        Signals the controller that the turn is completed.
        ''' 
        print("MODEL     : turnCardUndo: ASKING TO UNDO TURN OF CARD " + str(cardId))
        _, top = self.cardOrderDict[cardId]
        #If the card is turned up
        if self.cardFaceUp[cardId] == True:
            # If the card is the top card or the card is on the drawable stack
            if top == None or self.findStackOfCard(cardId) == boardStacks.Deck:
                # Turn the card and emit the signal
                self.cardFaceUp[cardId] = False
                print("MODEL     : turnCardUndo: Sending update signal to boardView.")
                self.com.updateCardSignal.emit(cardId)    
        else:
            print("MODEL     : turnCardUndo: Turning of card disallowed.")

        
    def moveCard(self, fromStack, toStack, card, allowUseOfTempStack = False):
        '''
        Slot for receiving MoveCard events from Controller.
        Moves card to stack toStack, and updates all references to keep 
        representation sane.
        
        Can be used internally in boardModel, in which case the use of the temp
        stack can be allowed. This should not be done externally.
        '''
        
        # if(self.checkMove(fromStack, toStack, card) == False):
        #     return False
        
        print("MODEL     : MoveCard: Entering moveCard with arguments (", fromStack, ", ", toStack, ", ", card, ")");
        
        # Make sure the tempStack is not used in model.
        if((fromStack == boardStacks.tempStack or toStack == boardStacks.tempStack) and allowUseOfTempStack == False):
            print("MODEL     : MoveCard: Sanity check: Attempted to use tempStack in MODEL -- ABORTING.")
            return False
        else:
            print("MODEL     : MoveCard: Permitting use of tempStack in MODEL.")
        
        # Make sure that the card is not moved to the same stack.
        if(fromStack == toStack):
            print("MODEL     : MoveCard: Sanity check: Source and Destination stacks are the same -- ABORTING.")
            return False
        
        # Make sure fromStack is sane.
        if(self.findStackOfCard(card) != fromStack):
            print("MODEL     : MoveCard: Sanity check: Card", card, "is NOT in Stack", fromStack, " -- ABORTING.")
            return False

        # Make sure that cards that are to be moved from Drawable to Deck
        # are placed in the right (reverse) order
        if (fromStack == boardStacks.Drawable and toStack == boardStacks.Deck):
            self.reverseStack(fromStack)
            card = self.findRootCardInStack(fromStack)

        # These are the cards that will be affected by the move, in addition to card.
        oldPrev = self.cardOrderDict[card][0]
        newPrev = self.findTopCardInStack(toStack)
        
        # Ensure that we keep the previous and next relationships sane.
        if(newPrev == None):
            self.cardOrderDict[card] = (toStack, self.cardOrderDict[card][1])
            print("MODEL     : MoveCard: Move card", card, "to empty stack", toStack);
        else:
            self.cardOrderDict[card] = (newPrev, self.cardOrderDict[card][1])
            self.cardOrderDict[newPrev] = (self.cardOrderDict[newPrev][0], card)
            print("MODEL     : MoveCard: Move card", card, "to non-empty stack", toStack, ". Previous top:", newPrev);
        
        try:
            self.cardOrderDict[oldPrev] = (self.cardOrderDict[oldPrev][0], None)
        except:
            print("MODEL     : MoveCard: Stack", oldPrev, "is now empty.");

        # Make sure that cards that have been move from Deck to Drawable show up
        # in the right (reverse) order
        if (fromStack == boardStacks.Deck and toStack == boardStacks.Drawable):
            self.reverseStack(toStack)
        
        # Create dictionary and send in signal to controller
        if(allowUseOfTempStack):
            print("MODEL     : MoveCard: Using tempstack, not sending to controller.")
        else:
            print("MODEL     : MoveCard: Sending stacks to CONTROLLER.")
            self.com.updateStackSignal.emit(self.getStackDict())
        
        # Send the gameWon signal if this move finishes the game.
        if(self.checkWin()):
            print("MODEL     : moveCard: Winning condition reached -- sending GameWonSignal.")
            self.com.gameWonSignal.emit()
        
        return True
        
        
    def reenterCards(self):
        '''
        Moves all Drawable cards to the bottom of the Deck.
        '''
        bottomDrawCard = self.findRootCardInStack(boardStacks.Drawable)
        bottomDeckCard = self.findRootCardInStack(boardStacks.Deck)
        
        print("MODEL     : reenterCards: Bottom Draw: ", bottomDrawCard)
        
        if(bottomDrawCard == None):
            # There is nothing to move.
            return 0
        
        # Turn the cards face down before returning them to the Deck
        drawableStackList = self.getStack(boardStacks.Drawable)
        for cardId in drawableStackList:
            print("MODEL     : reenterCards: Turning", cardId)
            self.cardFaceUp[cardId] = False
            self.com.updateCardSignal.emit(cardId)
        
        if(bottomDeckCard == None):
            # The Deck stack is empty, so we just move the cards here.
            self.moveCard(boardStacks.Drawable, boardStacks.Deck, bottomDrawCard)
        else:
            # We insert the cards between the Deck and bottom of Deck, via the
            # temp stack.
            self.moveCard(boardStacks.Deck, boardStacks.tempStack, bottomDeckCard, True)
            self.moveCard(boardStacks.Drawable, boardStacks.Deck, bottomDrawCard, True)
            self.moveCard(boardStacks.tempStack, boardStacks.Deck, bottomDeckCard, True)
        
        # Create dictionary and send in signal to controller
        print("MODEL     : reenterCards: Sending stacks to CONTROLLER.")
        self.com.updateStackSignal.emit(self.getStackDict())
        
        # Return the number of affected cards, for use with undo.
        return self.findNumberOfCardsBeforeCardInStack(boardStacks.Deck, bottomDeckCard)
        
        
    def unReenterCards(self, amount):
        '''
        Move the bottom amount cards to Drawable from Deck.
        '''
        
        newDeckRoot = self.findNthCardInStack(boardStacks.Deck, amount)
        newDrawableRoot = self.findRootCardInStack(boardStacks.Deck)
        
        self.moveCard(boardStacks.Deck, boardStacks.tempStack, newDeckRoot, True)
        self.moveCard(boardStacks.Deck, boardStacks.Drawable, newDrawableRoot)

        # Turn the cards face up after returning them to Drawable
        drawableStackList = self.getStack(boardStacks.Drawable)
        for cardId in drawableStackList:
            self.cardFaceUp[cardId] = True
            self.com.updateCardSignal.emit(cardId)

        self.moveCard(boardStacks.tempStack, boardStacks.Deck, newDeckRoot, True)
        
        
    def createSolitaireGame(self):
        '''
        Create a solitaire game
        '''
        # Create list of all cards, from which we can remove added cards.
        deckOfCards = []
        for i in range(0, 52):
            deckOfCards.append(i)
        random.shuffle(deckOfCards) 
        
        self.cardOrderDict[deckOfCards[0]] = (boardStacks.Bottom1, None)
        self.cardFaceUp[deckOfCards[0]] = True
        
        self.cardOrderDict[deckOfCards[1]] = (boardStacks.Bottom2, deckOfCards[2])
        self.cardOrderDict[deckOfCards[2]] = (deckOfCards[1], None)
        self.cardFaceUp[deckOfCards[2]] = True

        self.cardOrderDict[deckOfCards[3]] = (boardStacks.Bottom3, deckOfCards[4])
        self.cardOrderDict[deckOfCards[4]] = (deckOfCards[3], deckOfCards[5])
        self.cardOrderDict[deckOfCards[5]] = (deckOfCards[4], None)
        self.cardFaceUp[deckOfCards[5]] = True

        self.cardOrderDict[deckOfCards[6]] = (boardStacks.Bottom4, deckOfCards[7])
        self.cardOrderDict[deckOfCards[7]] = (deckOfCards[6], deckOfCards[8])
        self.cardOrderDict[deckOfCards[8]] = (deckOfCards[7], deckOfCards[9])
        self.cardOrderDict[deckOfCards[9]] = (deckOfCards[8], None)
        self.cardFaceUp[deckOfCards[9]] = True

        self.cardOrderDict[deckOfCards[10]] = (boardStacks.Bottom5, deckOfCards[11])
        self.cardOrderDict[deckOfCards[11]] = (deckOfCards[10], deckOfCards[12])
        self.cardOrderDict[deckOfCards[12]] = (deckOfCards[11], deckOfCards[13])
        self.cardOrderDict[deckOfCards[13]] = (deckOfCards[12], deckOfCards[14])
        self.cardOrderDict[deckOfCards[14]] = (deckOfCards[13], None)
        self.cardFaceUp[deckOfCards[14]] = True

        self.cardOrderDict[deckOfCards[15]] = (boardStacks.Bottom6, deckOfCards[16])
        self.cardOrderDict[deckOfCards[16]] = (deckOfCards[15], deckOfCards[17])
        self.cardOrderDict[deckOfCards[17]] = (deckOfCards[16], deckOfCards[18])
        self.cardOrderDict[deckOfCards[18]] = (deckOfCards[17], deckOfCards[19])
        self.cardOrderDict[deckOfCards[19]] = (deckOfCards[18], deckOfCards[20])
        self.cardOrderDict[deckOfCards[20]] = (deckOfCards[19], None)
        self.cardFaceUp[deckOfCards[20]] = True

        self.cardOrderDict[deckOfCards[21]] = (boardStacks.Bottom7, deckOfCards[22])
        self.cardOrderDict[deckOfCards[22]] = (deckOfCards[21], deckOfCards[23])
        self.cardOrderDict[deckOfCards[23]] = (deckOfCards[22], deckOfCards[24])
        self.cardOrderDict[deckOfCards[24]] = (deckOfCards[23], deckOfCards[25])
        self.cardOrderDict[deckOfCards[25]] = (deckOfCards[24], deckOfCards[26])
        self.cardOrderDict[deckOfCards[26]] = (deckOfCards[25], deckOfCards[27])
        self.cardOrderDict[deckOfCards[27]] = (deckOfCards[26], None)
        self.cardFaceUp[deckOfCards[27]] = True

        # Add first card
        self.cardOrderDict[deckOfCards[28]] = (boardStacks.Deck, deckOfCards[29])
        self.cardFaceUp[deckOfCards[28]] = False

        # Add all but last
        for i in range(29, len(deckOfCards)-1):
            self.cardOrderDict[deckOfCards[i]] = (deckOfCards[i-1], deckOfCards[i+1])
            self.cardFaceUp[deckOfCards[i]] = False
            
        # Add last card
        self.cardOrderDict[deckOfCards[len(deckOfCards)-1]] = (deckOfCards[len(deckOfCards)-2], None)
        self.cardFaceUp[deckOfCards[len(deckOfCards)-1]] = False
    
    
    def findStackOfCard(self, card):
        '''
        Returns the stack card belongs to.
        '''
        tempCard = card
        
        while(self.cardOrderDict[tempCard][0] >= 0):
            tempCard = self.cardOrderDict[tempCard][0]
        
        # Debug message
        print("MODEL     : findStackOfCard:", card, "is in stack", self.cardOrderDict[tempCard][0])
        
        return self.cardOrderDict[tempCard][0]

    
    def findRootCardInStack(self, stack):
        '''
        Finds the bottom-most card belonging to stack and returns it.
        '''
        
        # Loop through data structure to find stack.
        for i in range(0, len(self.cardOrderDict)):
            if(self.cardOrderDict[i][0] == stack):
                return i
            
        return None
    
    
    def findTopCardInStack(self, stack):
        '''
        Returns the top-most card belonging to stack.
        '''
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard == None):
            return None
        else:
            # Iterate through stack until top card found.
            while(self.cardOrderDict[oldCard][1] != None):
                oldCard = self.cardOrderDict[oldCard][1]
            
            return oldCard
            
            
    def findNthCardInStack(self, stack, Nth):
        '''
        Returns the Nth card from root belonging to stack.
        '''
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard == None):
            return None
        elif(Nth == 0):
            return oldCard
        else:
            cardNumber = 0
            # Iterate through stack until top card found.
            while(self.cardOrderDict[oldCard][1] != None):
                oldCard = self.cardOrderDict[oldCard][1]
                cardNumber += 1
                if(cardNumber == Nth):
                    return oldCard
            
            print("MODEL     : findNthCardInStack: cardnumber:", cardNumber, "nth:", Nth)
            return None            
            
    
    def findNumberOfCardsBeforeCardInStack(self, stack, card):
        '''
        Returns the number of cards before card in stack.
        '''
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard == None):
            return 0
        else:
            numberOfCards = 1
            # Iterate through stack until top card found.
            while(self.cardOrderDict[oldCard][1] != None and self.cardOrderDict[oldCard][1] != card):
                oldCard = self.cardOrderDict[oldCard][1]
                numberOfCards += 1
                
            return numberOfCards
    
    
    def getStack(self, stack):
        '''
        Returns a list of cards, from bottom to top that make up a stack.
        '''
        
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard != None):
            stackList = [oldCard]
            while(self.cardOrderDict[oldCard][1] != None):
                oldCard = self.cardOrderDict[oldCard][1]
                stackList.append(oldCard)
            return stackList
        else:
            return []
    
    
    def reverseStack(self, stack):
        '''
        Reverses the order of the cards in a stack.
        '''
        stackList = self.getStack(stack)
        stackSize = len(stackList)
        
        if(stackSize < 2):
            # Trivially reversed.
            return
        
        card = stackList[stackSize - 1]
        nextCard = stackList[stackSize - 2]
        self.cardOrderDict[card] = (stack, nextCard)
        
        for i in range(stackSize - 2, -1, -1):
            prevCard = card
            card = nextCard
            if i == 0:
                nextCard = None
            else:
                nextCard = stackList[i - 1]
            self.cardOrderDict[card] = (prevCard, nextCard)
    
    def getStackDict(self):
        '''
        Creates a dictionary with (stackID, list[cardID]) and returns it
        '''
        stackDict = dict()
        
        for stack in vars(boardStacks):
            if not callable(stack) and not stack.startswith("__") and not getattr(boardStacks, stack) == -30:
                stackDict[getattr(boardStacks, stack)] = self.getStack(getattr(boardStacks, stack))
            
        return stackDict