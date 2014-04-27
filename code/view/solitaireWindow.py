'''
Created on 13 apr 2014

@author: Sven, Bjorn
'''

'''
Basic imports, save to use later.
from PyQt5.QtCore import (QLineF, QMimeData, QPoint, QPointF, qrand, QRectF,
        qsrand, Qt, QTime, QTimeLine)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QTransform, QFont)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView, QApplication)
'''

from PyQt5.QtCore import (QSettings, QSize, QVariant, QPoint)
from PyQt5.QtWidgets import (QMainWindow, QAction, QMessageBox)

from view import boardView

class solitaireWindow(QMainWindow):
    '''
    solitaireWindow is a QMainWindow. It has a menu
    '''
    
    winTitle = ""
    
#    ' Move to config file in a later step '
#    windowWidth = 500
#    windowHeight = 300


    def __init__(self, title, gameStateController):
        '''
        Init function, create a graphicsScene spawning a boardView and attach it to a graphicsView
        '''
        
        super(solitaireWindow,self).__init__()

        settings = QSettings()
        size = settings.value("MainWindow/Size", QSize(800,600))
        position = settings.value("MainWindow/Position", QVariant(QPoint(0, 0)))
    
        self.resize(size)
        self.move(position)
        
        #Create a boardView with self (parent) as argument, set it's position and att it to the scene
        bView = boardView.boardView(500, 300, gameStateController)
        #                            size.width(), size.height())
        self.setCentralWidget(bView)
        self.setWindowTitle(title)
        self.createUI()
        self.createMenu()
        self.show()

    
    def createUI(self):
        '''
        Creates UI... (sets window title only... unnessecary?)
        '''
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
        exitAction.triggered.connect(self.close)
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
    
    def closeEvent(self, event):
        '''
        Overrides closeEvent to provide confirm dialogue and save settings
        '''
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position", QVariant(self.pos()))
        else:
            event.ignore()

    def okToContinue(self):
        '''
        Creates a QMessageBox that prompts users if they wish to exit or not
        Returns True if yes, else False.
        '''
        reply = QMessageBox.question(self, "Exit?", "Do you want to exit Solitaire?",
                                     QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False
        
    #def resizeEvent(self, event):
    #    self.windowWidth = event.size().width
    #    self.windowHeight = event.size().height
        
    #def getWindowWidth(self):
    #    return self.windowWidth
    
    #def getWindowHeight(self):
    #    return self.windowHeight
    