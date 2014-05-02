'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

#from model import stackModel
from model import cardModel
from enum import Enum

class boardStacks(Enum):
    
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
    classdocs
    '''
    
    cardList = list()
    cardOrderDict = dict()
    
    Deck = None
    Drawable = None
    TopLL = None
    TopML = None
    TopMR = None
    TopRR = None
    BottomLL = None
    BottomML = None
    BottomMR = None
    BottomRR = None
    DragCard = None
    
    def findRootCardInStack(self, stack):
        for i in range(0, len(self.cardOrderDict)):
            if(self.cardOrderDict[i][0] == stack):
                print("MODEL: findRootCardInStack: Card " + str(i) + " is at the root of stack " + str(stack) + ".")
                return i
            
        print("MODEL: findRootCardInStack: Can not find root of stack " + str(stack) + ", stack is empty.")
        return None
    
    def findTopCardInStack(self, stack):
        
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard == None):
            print("MODEL: findTopCardInStack: Stack " + str(stack) + " is empty and has no top card.")
            return None
        else:
            while(self.cardOrderDict[oldCard][1] != None):
                oldCard = self.cardOrderDict[oldCard][1]
            
            print("MODEL: findTopCardInStack: Top card in stack " + str(stack) + " is card " + str(oldCard) + ".")
            return oldCard
    
    def moveCard(self, fromStack, toStack, card):
        
        print("MODEL: MoveCard: Entering moveCard with arguments (" + str(fromStack) + ", " + str(toStack) + ", " + str(card) + ").");
        print("MODEL: MoveCard: DEBUG: The fromStack argument doesn't do anything and should be removed --Bjorn")
        
        oldPrev = self.cardOrderDict[card][0]
        newPrev = self.findTopCardInStack(toStack)
        
        if(newPrev == None):
            self.cardOrderDict[card] = (toStack, self.cardOrderDict[card][1])
            print("MODEL: MoveCard: Move card " + str(card) + " to empty stack " + str(toStack) + ".");
        else:
            self.cardOrderDict[card] = (newPrev, self.cardOrderDict[card][1])
            self.cardOrderDict[newPrev] = (self.cardOrderDict[newPrev], card)
            print("MODEL: MoveCard: Move card " + str(card) + " to non-empty stack " + str(toStack) + ". Put on " + str(newPrev) + ".");
        
        try:
            self.cardOrderDict[oldPrev] = (self.cardOrderDict[oldPrev][0], None)
        except:
            print("MODEL: MoveCard: Stack " + str(oldPrev) + " is now empty.");
        
        print("MODEL: MoveCard: Finished.");

    def __init__(self):
        '''
        Constructor
        '''
        
        # Create cards in cardList
        for color in range(1, 5):
            for number in range(1,14):
                self.cardList.append(cardModel.cardModel(color, number))
        
        self.createSortedDeck()
        
        
    def createSortedDeck(self):
        self.cardOrderDict[0] = (boardStacks.Deck, 1);
        for i in range(1, len(self.cardList) - 1):
            self.cardOrderDict[i] = (i-1,i+1)
        self.cardOrderDict[len(self.cardList) - 1] = (len(self.cardList) - 2, None);
        
    
    def getCard(self, card):
        
        return self.cardList[card]
    
    def getStack(self, stack):
        
        oldCard = self.findRootCardInStack(stack)
        
        if(oldCard != None):
        
            stackList = [oldCard]
            while(self.cardOrderDict[oldCard][1] != None):
                oldCard = self.cardOrderDict[oldCard][1]
                stackList.append(oldCard)
            return stackList
        
        else:
            
            return []
            