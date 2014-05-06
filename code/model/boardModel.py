'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

from model import cardModel
#from enum import Enum
from model import communicator

class boardStacks(object):
    '''
    This class contains the id numbers of the stacks, for use in the internal representation and API
    to the board model itself.
    '''
    
    Deck = -1
    Drawable = -2
    
    TopLL = -11
    TopML = -12
    TopMR = -13
    TopRR = -14
    
    BottomLL = -21
    BottomML = -22
    BottomMR = -23
    BottomRR = -24
    
    DragCard = -30


class boardModel(object):
    '''
    The main part of the model, which keeps track of where the cards are located, and offers an interface
    to move cards between stacks.
    '''
    
    'cardList contains a list of all cards present in the game, and is used to reference cards by id numbers.'
    cardList = list()
    
    'cardOrderDict keeps a linked list-like representation of the neighbors of each card.'
    'Representation: cardOrderDict[currentCard] = (previousCard, nextCard)'
    cardOrderDict = dict()
    
    
    def __init__(self, gameStateController):
        '''
        Constructor
        '''
        
        self.gameStateController = gameStateController
        
        # Create cards in cardList
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardModel.cardModel(color, number))
        
        self.createSortedDeck()
        
        # Set up communicator
        self.com = communicator.communicator()
        # Connect signal to slot
        self.com.updateSignal.connect(gameStateController.updateStacks)
        
    
    def findRootCardInStack(self, stack):
        '''
        Finds the bottom-most card belonging to stack and returns it.
        '''
        for i in range(0, len(self.cardOrderDict)):
            if(self.cardOrderDict[i][0] == stack):
                print("MODEL: findRootCardInStack: Card " + str(i) + " is at the root of stack " + str(stack) + ".")
                return i
            
        print("MODEL: findRootCardInStack: Can not find root of stack " + str(stack) + ", stack is empty.")
        return None
    
    
    def findTopCardInStack(self, stack):
        '''
        Returns the top-most card belonging to stack.
        '''
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard == None):
            print("MODEL: findTopCardInStack: Stack " + str(stack) + " is empty and has no top card.")
            return None
        else:
            while(self.cardOrderDict[oldCard][1] != None):
                oldCard = self.cardOrderDict[oldCard][1]
            
            print("MODEL: findTopCardInStack: Top card in stack " + str(stack) + " is card " + str(oldCard) + ".")
            return oldCard
    
    
    def findStackOfCard(self, card):
        '''
        Returns the stack card belongs to.
        '''
        tempCard = card

        while(self.cardOrderDict[tempCard][0] >= 0):
            tempCard = self.cardOrderDict[tempCard][0]
        
        return self.cardOrderDict[tempCard][0]
        
    def getCard(self, card):
        '''
        Returns the cardModel representing card.
        '''
        
        return self.cardList[card]
    
    
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
    
    
    def moveCard(self, fromStack, toStack, card):
        '''
        Moves card to stack toStack, and updates all references to keep representation sane.
        '''
        
        print("MODEL: MoveCard: Entering moveCard with arguments (" + str(fromStack) + ", " + str(toStack) + ", " + str(card) + ").");
        
        'Make sure fromStack is sane.'
        if(self.findStackOfCard(card) != fromStack):
            print("MODEL: MoveCard: Sanity check: Card " + str(card) + " is NOT in Stack " + str(fromStack) + " -- ABORTING.")
            return False
        else:
            print("MODEL: MoveCard: Sanity check: Card " + str(card) + " is in Stack " + str(fromStack) + " -- continue.")
        
        'These are the cards that will be affected by the move, in addition to card.'
        oldPrev = self.cardOrderDict[card][0]
        newPrev = self.findTopCardInStack(toStack)
        
        'Ensure that we keep the previous and next relationships sane.'
        if(newPrev == None):
            self.cardOrderDict[card] = (toStack, self.cardOrderDict[card][1])
            print("MODEL: MoveCard: Move card " + str(card) + " to empty stack " + str(toStack) + ".");
        else:
            self.cardOrderDict[card] = (newPrev, self.cardOrderDict[card][1])
            self.cardOrderDict[newPrev] = (self.cardOrderDict[newPrev][0], card)
            print("MODEL: MoveCard: Move card " + str(card) + " to non-empty stack " + str(toStack) + ". Put on " + str(newPrev) + ".");
        
        try:
            self.cardOrderDict[oldPrev] = (self.cardOrderDict[oldPrev][0], None)
        except:
            print("MODEL: MoveCard: Stack " + str(oldPrev) + " is now empty.");
        
        print("MODEL: MoveCard: Finished.");
        
        # Create dictionary and send in signal to controller
        self.com.updateSignal.emit(1, self.getStackDict())
        
        return True
        
        
    def createSortedDeck(self):
        '''
        Adds all cards in self.cardList to the Deck.
        '''
        self.cardOrderDict[0] = (boardStacks.Deck, 1);
        for i in range(1, len(self.cardList) - 1):
            self.cardOrderDict[i] = (i-1,i+1)
        self.cardOrderDict[len(self.cardList) - 1] = (len(self.cardList) - 2, None);
        
    def getStackDict(self):
        '''
        Creates a dictionary with (stackID, list[cardID]) and returns it
        '''
        stackDict = dict()
        
        for stack in vars(boardStacks):
            if not callable(stack) and not stack.startswith("__"):
                stackDict[getattr(boardStacks, stack)] = self.getStack(getattr(boardStacks, stack))
            
        return stackDict
