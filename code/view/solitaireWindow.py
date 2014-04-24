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


    def __init__(self, title):
        '''
        Init function, create a graphicsScene spawning a boardView and attach it to a graphicsView
        '''
        
        super(solitaireWindow,self).__init__()

        settings = QSettings()
        size = settings.value("MainWindow/Size", QSize(800,600))
        #, QVariant(QSize(500, 300))).toSize()
        self.resize(size)
        position = settings.value("MainWindow/Position", QVariant(QPoint(0, 0)))
        #.toPoint()
        self.move(position)
        
        #Create a boardView with self (parent) as argument, set it's position and att it to the scene
        bView = boardView.boardView(500, 300)
        #                            size.width(), size.height())
        self.setCentralWidget(bView)
        self.setWindowTitle(title)
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
    
    #def resizeEvent(self, event):
    #    self.windowWidth = event.size().width
    #    self.windowHeight = event.size().height
        
    #def getWindowWidth(self):
    #    return self.windowWidth
    
    #def getWindowHeight(self):
    #    return self.windowHeight
    
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position", QVariant(self.pos()))
        else:
            event.ignore()

    def okToContinue(self):
        reply = QMessageBox.question(self, "Exit?", "Do you want to exit Solitaire?",
                                     QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes:
            return True
        else:
            return False