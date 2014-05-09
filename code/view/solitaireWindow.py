'''
Created on 13 apr 2014

@author: Sven, Bjorn, Max
'''

'''
Basic imports, save to use later.
from PyQt5.QtCore import (QLineF, QMimeData, QPoint, QPointF, qrand, QRectF,
        qsrand, Qt, QTime, QTimeLine)
from PyQt5.QtGui import (QBrush, QColor, QDrag, QImage, QPainter, QPen,
        QPixmap, QTransform, QFont)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsTextItem, QGraphicsScene, QGraphicsView, QApplication)
'''

from PyQt5.QtCore import (QSettings, QSize, QVariant, QPoint, Qt)
from PyQt5.QtWidgets import (QMainWindow, QAction, QMessageBox, QToolBar)

from view import boardView
from view import transSlider

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
        
        # GameStateController needed for menu to Undo/Redo
        self.gameStateController = gameStateController

        # Set up settings to store properties (width, height etc)
        settings = QSettings()
        
        # Get size and position, resize and move accordingly
        size = settings.value("MainWindow/Size", QSize(900,600))
        position = settings.value("MainWindow/Position", QVariant(QPoint(0, 0)))
        self.resize(size)
        self.move(position)
        
        #Create a boardView and set it as central widget, create Menu
        self.bView = boardView.boardView(500, 300, gameStateController)
        self.setCentralWidget(self.bView)
        self.createUI()
        self.createMenu()
        
        self.slide = transSlider.transSlider(self.gameStateController)
        self.toolbar = QToolBar()
        self.toolbar.addWidget(self.slide)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

    
    def createUI(self):
        '''
        Creates UI... (sets window title only... unnessecary?)
        '''
        self.setWindowTitle(self.winTitle)
        
    def updateMenuUndo(self, canUndo):
        '''
        Slot called by Controller if possibility to Undo changes
        Enables undo in Menu>Edit if there are commands to undo and
        disables undo in Menu>Edit if there are no commands to undo.
        '''
        print("Can undo changed: " + str(canUndo))
        self.undoAction.setEnabled(canUndo)
        
    def updateMenuRedo(self, canRedo):
        '''
        Slot called by Controller if possibility to Redo changes
        Enables redo in Menu>Edit if there are commands to redo and
        disables redo in Menu>Edit if there are no commands to redo.
        '''
        print("Can redo changed: " + str(canRedo))
        self.redoAction.setEnabled(canRedo)
        
    def createMenu(self):
        '''
        Creates a menuBar and menus with associated actions
        '''
        
        # Create MenuBar
        self.menuBar = self.menuBar()
        
        # Create Menus
        fileMenu = self.menuBar.addMenu('&File')
        editMenu = self.menuBar.addMenu('&Edit')
        helpMenu = self.menuBar.addMenu('&Help')
        
        # Populate FileMenu
        self.exitAction = QAction('Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)
        fileMenu.addAction(self.exitAction)
        
        # Populate EditMenu with actions
        self.undoAction = QAction('Undo', self)        
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setEnabled(False)
        self.undoAction.triggered.connect(self.gameStateController.undo)
        
        self.redoAction = QAction('Redo', self)        
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.setEnabled(False)
        self.redoAction.triggered.connect(self.gameStateController.redo)
        
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
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
            
    def resizeEvent(self, event):
        '''
        Overrides resizeEvent to resize the QGraphicsScene as well
        '''
        #print("SOLWIN: resizeEvent")
        #print("SOLWIN: Size: ", event.size())
        self.bView.resizeEvent(event)
        QMainWindow.resizeEvent(self, event)

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
