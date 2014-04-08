'''
Created on 7 apr 2014

@author: Sven
'''

from PyQt5 import *
from PyQt5.QtGui import *
from view import boardView

class solitaireWindow(QtWidgets.QMainWindow):
    '''
    classdocs
    '''
    
    winTitle = ""
    
    ' Move to config file in a later step '
    windowWidth = 500
    windowHeight = 300

    def __init__(self, title):
        '''
        Constructor
        '''
        super(solitaireWindow,self).__init__()
        
        # Window stuff
        self.winTitle = title
        self.createUI()
        self.setGeometry(self.windowWidth, self.windowHeight, self.windowWidth, self.windowHeight)
        
        # Draw the main board.
        bView = boardView.boardView(self)
        
        # Menu items
        menuFile = self.menuBar().addMenu('File')
        menuEdit = self.menuBar().addMenu('Edit')
        menuHelp = self.menuBar().addMenu('Help')
        
        self.show()
        
    def createUI(self):
        self.setWindowTitle(self.winTitle)

    #def resizeEvent(self, event):
    #    self.windowWidth = event.size().width
    #    self.windowHeight = event.size().height
        
    #def getWindowWidth(self):
    #    return self.windowWidth
    
    #def getWindowHeight(self):
    #    return self.windowHeight