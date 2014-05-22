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
from PyQt5.QtWidgets import (QDialog, QAction, QLabel, QFrame, QVBoxLayout, QLabel, QButtonGroup, QRadioButton)
from PyQt5.QtGui import QIcon

from view import boardView
from view import transSlider

class controlPanel(QDialog):
    '''
    Control panel dialog.
    '''
    
    winTitle = "Control panel"


    def __init__(self, boardView):
        '''
        Init function
        '''
        
        super(controlPanel,self).__init__()

        self.boardView = boardView

        self.setWindowTitle(self.winTitle)
        
        # Set up settings to store properties (width, height etc)
        self.settings = QSettings()
        
        self.frame = QFrame(self)
        self.layout = QVBoxLayout()
        
        # Create a transparency slider for the cards
        self.slide = transSlider.transSlider(self.boardView)
        self.slide.setFixedWidth(200)
        self.transparencyLabel = QLabel('Card opacity:')
        
        # Create a button group to select card look
        self.createCardButtonGroup()
        self.themeLabel = QLabel('Deck theme:')
        
        # Add widgets and buttons to the control panel
        self.layout.addWidget(self.transparencyLabel)
        self.layout.addWidget(self.slide)
        self.layout.addWidget(self.themeLabel)
        self.layout.addWidget(self.redBackButton)
        self.layout.addWidget(self.blueBackButton)

        self.frame.setLayout(self.layout)
        
        # Get position, and move window accordingly
        position = self.settings.value("ControlPanel/Position", QVariant(QPoint(0, 0)))
        self.move(position)
        
    
    def showEvent(self, event):
        '''
        Overrides showEvent to set size of window on first open.
        '''
        self.adjustSize()
        self.setFixedSize(self.size())
        
    
    def closeEvent(self, event):
        '''
        Overrides closeEvent to provide confirm dialogue and save settings
        '''
        # Save which button is checked to load theme
        self.settings.setValue("ControlPanel/Theme", self.buttonCardGroup.checkedId())
        print("CONTROLPAN: Close control panel")
        
    def createCardButtonGroup(self):
        '''
        Creates a button group to select back of card color
        '''
        
        # Create a button group to ensure buttons are exclusive
        self.buttonCardGroup = QButtonGroup()
        
        # Create buttons and add them to the group
        self.redBackButton = QRadioButton("Red", self)
        self.buttonCardGroup.addButton(self.redBackButton, 1)
        self.blueBackButton = QRadioButton("Blue", self)
        self.buttonCardGroup.addButton(self.blueBackButton, 2)

        # Connect buttonGroup buttonClicked signal to slot
        self.buttonCardGroup.buttonClicked[int].connect(self.updateTheme)
        
        # Get stored theme from settings, enable the correct theme
        # and set the correct button
        theme = self.settings.value("ControlPanel/Theme", QVariant(1))
        self.updateTheme(theme)
        if theme == 1:
            self.redBackButton.setChecked(True)
        else:
            self.blueBackButton.setChecked(True)
            
        
        
    def updateTheme(self, buttonId):
        '''
        Slot for signal when buttonId is clicked.
        Sets the corresponding theme.
        '''
        if buttonId == 1:
            self.boardView.setBackImage("backRed")
        elif buttonId == 2:
            self.boardView.setBackImage("backBlue")
        
        