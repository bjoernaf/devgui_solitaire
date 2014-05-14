'''
Created on 7 apr 2014

@author: Sven, Bjorn
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
    
    #cardList contains a list of all cards present in the game, and is used to reference cards by id numbers.
    cardList = list()
    
    #cardOrderDict keeps a linked list-like representation of the neighbors of each card.
    #Representation: cardOrderDict[currentCard] = (previousCard, nextCard)
    cardOrderDict = dict()
    
    
    count = 0
    
    
    def __init__(self, gameStateController):
        '''
        Constructor
        '''
        # Set up communicator
        self.com = communicator()
        # Connect signal to slot
        self.com.updateStackSignal.connect(gameStateController.updateControllerStacks)
        
        # Create cards in cardList
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardModel(color, number, True))
        
        # Create deck of cards and notify view
        #self.createRandomizedDeck() #createSortedDeck()
        self.createSolitaireGame()
        self.com.updateStackSignal.emit(self.getStackDict())
        
        
    def moveCard(self, fromStack, toStack, card):
        '''
        Slot for receiving MoveCard events from Controller.
        Moves card to stack toStack, and updates all references to keep representation sane.
        '''

        #self.count += 1        
        #if(self.count % 2 == 0):
        #    return False
        
        print("MODEL     : MoveCard: Entering moveCard with arguments (", fromStack, ", ", toStack, ", ", card, ")");
        
        # Make sure the tempStack is not used in model.
        if(fromStack == boardStacks.tempStack or toStack == boardStacks.tempStack):
        	print("MODEL     : MoveCard: Sanity check: Attempted to use tempStack in MODEL -- ABORTING.")
        	return False
        
        # Make sure that the card is not moved to the same stack.
        if(fromStack == toStack):
        	print("MODEL     : MoveCard: Sanity check: Source and Destination stacks are the same -- ABORTING.")
        	return False
        
        # Make sure fromStack is sane.
        if(self.findStackOfCard(card) != fromStack):
            print("MODEL     : MoveCard: Sanity check: Card", card, "is NOT in Stack", fromStack, " -- ABORTING.")
            return False
        
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
        
        # Create dictionary and send in signal to controller
        print("MODEL     : MoveCard: Sending stacks to CONTROLLER.");
        self.com.updateStackSignal.emit(self.getStackDict())
        
        return True
        
        
    def createSortedDeck(self):
        '''
        Adds all cards in self.cardList to the Deck in order.
        '''
        self.cardOrderDict[0] = (boardStacks.Deck, 1)
        for i in range(1, len(self.cardList) - 1):
            self.cardOrderDict[i] = (i-1,i+1)
        self.cardOrderDict[len(self.cardList) - 1] = (len(self.cardList) - 2, None)

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
        self.cardList[deckOfCards[0]].faceup = True
        
        self.cardOrderDict[deckOfCards[1]] = (boardStacks.Bottom2, deckOfCards[2])
        self.cardOrderDict[deckOfCards[2]] = (deckOfCards[1], None)

        self.cardOrderDict[deckOfCards[3]] = (boardStacks.Bottom3, deckOfCards[4])
        self.cardOrderDict[deckOfCards[4]] = (deckOfCards[3], deckOfCards[5])
        self.cardOrderDict[deckOfCards[5]] = (deckOfCards[4], None)

        self.cardOrderDict[deckOfCards[6]] = (boardStacks.Bottom4, deckOfCards[7])
        self.cardOrderDict[deckOfCards[7]] = (deckOfCards[6], deckOfCards[8])
        self.cardOrderDict[deckOfCards[8]] = (deckOfCards[7], deckOfCards[9])
        self.cardOrderDict[deckOfCards[9]] = (deckOfCards[8], None)

        self.cardOrderDict[deckOfCards[10]] = (boardStacks.Bottom5, deckOfCards[11])
        self.cardOrderDict[deckOfCards[11]] = (deckOfCards[10], deckOfCards[12])
        self.cardOrderDict[deckOfCards[12]] = (deckOfCards[11], deckOfCards[13])
        self.cardOrderDict[deckOfCards[13]] = (deckOfCards[12], deckOfCards[14])
        self.cardOrderDict[deckOfCards[14]] = (deckOfCards[13], None)

        self.cardOrderDict[deckOfCards[15]] = (boardStacks.Bottom6, deckOfCards[16])
        self.cardOrderDict[deckOfCards[16]] = (deckOfCards[15], deckOfCards[17])
        self.cardOrderDict[deckOfCards[17]] = (deckOfCards[16], deckOfCards[18])
        self.cardOrderDict[deckOfCards[18]] = (deckOfCards[17], deckOfCards[19])
        self.cardOrderDict[deckOfCards[19]] = (deckOfCards[18], deckOfCards[20])
        self.cardOrderDict[deckOfCards[20]] = (deckOfCards[19], None)

        self.cardOrderDict[deckOfCards[21]] = (boardStacks.Bottom7, deckOfCards[22])
        self.cardOrderDict[deckOfCards[22]] = (deckOfCards[21], deckOfCards[23])
        self.cardOrderDict[deckOfCards[23]] = (deckOfCards[22], deckOfCards[24])
        self.cardOrderDict[deckOfCards[24]] = (deckOfCards[23], deckOfCards[25])
        self.cardOrderDict[deckOfCards[25]] = (deckOfCards[24], deckOfCards[26])
        self.cardOrderDict[deckOfCards[26]] = (deckOfCards[25], deckOfCards[27])
        self.cardOrderDict[deckOfCards[27]] = (deckOfCards[26], None)

        # Add first card
        self.cardOrderDict[deckOfCards[28]] = (boardStacks.Deck, deckOfCards[29])

        # Add all but last
        for i in range(29, len(deckOfCards)-1):
            self.cardOrderDict[deckOfCards[i]] = (deckOfCards[i-1], deckOfCards[i+1])
            
        # Add last card
        self.cardOrderDict[deckOfCards[len(deckOfCards)-1]] = (deckOfCards[len(deckOfCards)-2], None)


    def createRandomizedDeck(self):
    	'''
    	Adds all cards in self.cardList to the Deck in random order.
    	'''
    	
    	# Create list of all cards, from which we can remove added cards.
    	deckOfCards = []
    	for i in range(0, 52):
    		deckOfCards.append(i)
    	random.shuffle(deckOfCards)
    	
    	# Add first card
    	self.cardOrderDict[deckOfCards[0]] = (boardStacks.Deck, deckOfCards[1])
    	
    	# Add all but last
    	for i in range(1, len(deckOfCards)-1):
    		self.cardOrderDict[deckOfCards[i]] = (deckOfCards[i-1], deckOfCards[i+1])
    		
    	# Add last card
    	self.cardOrderDict[deckOfCards[len(deckOfCards)-1]] = (deckOfCards[len(deckOfCards)-2], None)
    	
    		
    def findStackOfCard(self, card):
        '''
        Returns the stack card belongs to.
        '''
        tempCard = card
        
        while(self.cardOrderDict[tempCard][0] >= 0):
            tempCard = self.cardOrderDict[tempCard][0]
        
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
    
    
    def getStackDict(self):
        '''
        Creates a dictionary with (stackID, list[cardID]) and returns it
        '''
        stackDict = dict()
        
        for stack in vars(boardStacks):
            if not callable(stack) and not stack.startswith("__") and not getattr(boardStacks, stack) == -30:
                stackDict[getattr(boardStacks, stack)] = self.getStack(getattr(boardStacks, stack))
            
        return stackDict
    