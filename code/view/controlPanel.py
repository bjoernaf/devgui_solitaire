'''
Created on 13 apr 2014

@author: Sven, Bjorn, Max
'''

from PyQt5.QtCore import (QSettings, QPoint)
from PyQt5.QtWidgets import (QDialog, QFrame, QVBoxLayout, QLabel, QButtonGroup, QRadioButton)

from view import transSlider

class controlPanel(QDialog):
    '''
    Control panel dialog.
    Contains card opacity slider and theme selection.
    '''
    
    winTitle = "Control panel"


    def __init__(self, boardView):
        '''
        Constructor:
        Creates the control panel and adds content.
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
        
        # Create a button group to select card back look
        self.createThemeButtonGroup()
        self.themeLabel = QLabel('Deck theme:')
        
        # Create a button group to select card front look
        self.createCardButtonGroup()
        self.cardLabel = QLabel('Card style:')
        
        # Add widgets and buttons to the control panel
        self.layout.addWidget(self.transparencyLabel)
        self.layout.addWidget(self.slide)
        self.layout.addWidget(self.themeLabel)
        self.layout.addWidget(self.redBackButton)
        self.layout.addWidget(self.blueBackButton)
        self.layout.addWidget(self.cardLabel)
        self.layout.addWidget(self.detailedCardButton)
        self.layout.addWidget(self.simpleCardButton)

        # Set frame layout
        self.frame.setLayout(self.layout)
        
        # Get position from settings, and move window accordingly
        position = self.settings.value("ControlPanel/Position", QPoint(0, 0))
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
        self.settings.setValue("ControlPanel/Theme", self.buttonThemeGroup.checkedId())
        self.settings.setValue("ControlPanel/CardStyle", self.buttonCardGroup.checkedId())
        print("CONTROLPAN: Close control panel")
        
    def createThemeButtonGroup(self):
        '''
        Creates a button group to select back of card color
        '''
        
        # Create a button group to ensure buttons are exclusive
        self.buttonThemeGroup = QButtonGroup()
        
        # Create buttons and add them to the group
        self.redBackButton = QRadioButton("Red", self)
        self.buttonThemeGroup.addButton(self.redBackButton, 1)
        self.blueBackButton = QRadioButton("Blue", self)
        self.buttonThemeGroup.addButton(self.blueBackButton, 2)

        # Connect buttonGroup buttonClicked signal to slot
        self.buttonThemeGroup.buttonClicked[int].connect(self.updateTheme)
        
        # Get stored theme from settings, enable the correct theme
        # and set the correct button
        theme = int(self.settings.value("ControlPanel/Theme", 1))
        self.updateTheme(theme)
        if theme == 1:
            self.redBackButton.setChecked(True)
        else:
            self.blueBackButton.setChecked(True)
            
    
    def createCardButtonGroup(self):
        '''
        Creates a button group to select the look of a card.
        Detailed displays a full card image, simple draws a
        simple card using text and a color image.
        '''
        
        # Create a button group to ensure buttons are exclusive
        self.buttonCardGroup = QButtonGroup()
        
        # Create buttons and add them to the group
        self.detailedCardButton = QRadioButton("Detailed", self)
        self.detailedCardButton.setToolTip("Paint card image")
        self.buttonCardGroup.addButton(self.detailedCardButton, 1)
        self.simpleCardButton = QRadioButton("Simple", self)
        self.simpleCardButton.setToolTip("Paint card number and color")
        self.buttonCardGroup.addButton(self.simpleCardButton, 2)

        # Connect buttonGroup buttonClicked signal to slot
        self.buttonCardGroup.buttonClicked[int].connect(self.updateCard)
        
        # Get stored theme from settings, enable the correct theme
        # and set the correct button
        cardStyle = int(self.settings.value("ControlPanel/CardStyle", 1))
        self.updateCard(cardStyle)
        if cardStyle == 1:
            self.detailedCardButton.setChecked(True)
        else:
            self.simpleCardButton.setChecked(True)
            
        
    def updateCard(self, buttonId):
        '''
        Slot for signal when buttonId is clicked.
        Calls boardView to set the selected image as front image.
        '''
        if buttonId == 1:
            self.boardView.setFrontImage("detailed")
        elif buttonId == 2:
            self.boardView.setFrontImage("simple")
        
    def updateTheme(self, buttonId):
        '''
        Slot for signal when buttonId is clicked.
        Calls boardView to set the selected theme as back image.
        '''
        if buttonId == 1:
            self.boardView.setBackImage("backRed")
        elif buttonId == 2:
            self.boardView.setBackImage("backBlue")
