'''
Created on 13 apr 2014

@author: Sven, Bjorn
'''

from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QTransform, QIcon)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView, QMainWindow, QToolBar, QAction)

from view import boardView

class solitaireWindow(QMainWindow):
    '''
    solitaireWindow is a QMainWindow. It has a menu
    '''
    
    winTitle = ""
    
    ' Move to config file in a later step '
    windowWidth = 500
    windowHeight = 300


    def __init__(self, title):
        '''
        Init function, create a graphicsScene spawning a boardView and attach it to a graphicsView
        '''
        
        super(solitaireWindow,self).__init__()
        
        #Create a boardView with self (parent) as argument, set it's position and att it to the scene
        bView = boardView.boardView(self.windowWidth, self.windowHeight)
        #boardView.setTransform(QTransform.fromScale(1.2, 1.2), True)
        self.setCentralWidget(bView)
        self.winTitle = title
        self.createUI()
        self.createMenu()

    
    def createUI(self):
        self.setWindowTitle(self.winTitle)
        
    def createMenu(self):
        '''
        Creates a menuBar and menus with associated actions
        '''
        
        # Create MenuBar
        menuBar = self.menuBar()
        
        # Create Menus
        fileMenu = menuBar.addMenu('&File')
        editMenu = menuBar.addMenu('&Edit')
        helpMenu = menuBar.addMenu('&Help')
        
        # Populate FileMenu
        exitAction = QAction('Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QApplication.quit)
        fileMenu.addAction(exitAction)
        
        # Populate EditMenu with actions
        undoAction = QAction('Undo', self)        
        undoAction.setShortcut('Ctrl+Z')
        
        redoAction = QAction('Redo', self)        
        redoAction.setShortcut('Ctrl+Y')
        
        editMenu.addAction(undoAction)
        editMenu.addAction(redoAction)
        editMenu.addAction('Preferences')
        
        # Populate HelpMenu
        helpMenu.addAction('About')
    
    #def resizeEvent(self, event):
    #    self.windowWidth = event.size().width
    #    self.windowHeight = event.size().height
        
    #def getWindowWidth(self):
    #    return self.windowWidth
    
    #def getWindowHeight(self):
    #    return self.windowHeight
        