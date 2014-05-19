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
from PyQt5.QtGui import QIcon

from view import boardView, transSlider, controlPanel, communicator

class solitaireWindow(QMainWindow):
    '''
    solitaireWindow is a QMainWindow. It has a menu
    '''
    
    winTitle = "Group 13 Solitaire"


    def __init__(self, title, gameStateController):
        '''
        Init function, create a graphicsScene spawning a boardView and attach it to a graphicsView
        '''
        
        super(solitaireWindow,self).__init__()
        
        # GameStateController needed for menu to Undo/Redo
        self.gameStateController = gameStateController
        
        # Create communicator and connect signals
        self.com = communicator.communicator()
        self.com.newGameSignal.connect(self.gameStateController.startNewGame)

        # Set up settings to store properties (width, height etc)
        settings = QSettings()
        
        # Get size and position, resize and move accordingly
        size = settings.value("MainWindow/Size", QSize(900,600))
        position = settings.value("MainWindow/Position", QVariant(QPoint(0, 0)))
        self.resize(size)
        self.move(position)
        
        # Create a boardView and set it as central widget, create Menu
        self.bView = boardView.boardView(500, 300, gameStateController)
        self.setCentralWidget(self.bView)
        self.createUI()
        self.createMenu()
        
        # Create control panel
        self.controlPanel = controlPanel.controlPanel(self.bView)
        
        # Create a transparency slider for the cards
        self.slide = transSlider.transSlider(self.bView)
        # Create a toolbar and add appropriate actions and widgets to it
        self.toolbar = QToolBar()
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.slide)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)


    def openControlPanel(self):
        '''
        Opens the control panel dialog.
        '''
        self.controlPanel.show()
        self.controlPanel.raise_()
        self.controlPanel.activateWindow()
        
    
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
        print("SOLITAIREW: UpdateMenuUndo: Can undo changed: " + str(canUndo))
        self.undoAction.setEnabled(canUndo)
        
        
    def updateMenuRedo(self, canRedo):
        '''
        Slot called by Controller if possibility to Redo changes
        Enables redo in Menu>Edit if there are commands to redo and
        disables redo in Menu>Edit if there are no commands to redo.
        '''
        print("SOLITAIREW: updateMenuRedo: Can redo changed: " + str(canRedo))
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
        self.newGameAction = QAction('New Game', self)
        self.newGameAction.setShortcut('Ctrl+N')
        self.newGameAction.triggered.connect(self.newGame)
        fileMenu.addAction(self.newGameAction)
        
        self.exitAction = QAction('Exit', self)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)
        fileMenu.addAction(self.exitAction)
        
        # Populate EditMenu with actions
        self.undoAction = QAction(QIcon('images/undo.png'), 'Undo', self)        
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.setEnabled(False)
        self.undoAction.triggered.connect(self.gameStateController.undo)
        
        self.redoAction = QAction(QIcon('images/redo.png'), 'Redo', self)        
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.setEnabled(False)
        self.redoAction.triggered.connect(self.gameStateController.redo)
        
        self.controlPanelAction = QAction('Preferences', self)
        self.controlPanelAction.setEnabled(True)
        self.controlPanelAction.triggered.connect(self.openControlPanel)
        
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction(self.controlPanelAction)
        
        # Populate HelpMenu
        helpMenu.addAction('About')
    
    
    def closeEvent(self, event):
        '''
        Overrides closeEvent to provide confirm dialogue and save settings
        '''
        if self.okToContinue():

			# Close the control panel
            self.controlPanel.close()
            
            # Store settings
            settings = QSettings()
            settings.setValue("MainWindow/Size", QVariant(self.size()))
            settings.setValue("MainWindow/Position", QVariant(self.pos()))
            settings.setValue("ControlPanel/Position", QVariant(self.controlPanel.pos()))
            settings.setValue("TransparencySlider/Position", QVariant(self.bView.getOpacity()))
        else:
            event.ignore()
         
            
    def resizeEvent(self, event):
        '''
        Overrides resizeEvent to resize the QGraphicsScene as well
        '''
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
        
    def newGame(self):
        '''
        Creates a QMessageBox that prompts user if they wish to start a
        new game and abandon their current session. If reply is yes,
        current game is destroyed and a new game is set up.
        '''
        reply = QMessageBox.question(self, "Start new game?",
                                     "Do you want to abandon your current session and start a new game?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.com.newGameSignal.emit()
