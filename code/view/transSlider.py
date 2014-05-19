'''
Created on 9 maj 2014

@author: Max, Sven, Bjorn
'''
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
from view import communicator
        

class transSlider(QSlider):
    '''
    Slider to set the transparency of cards.
    TODO: Change to move cards only later?
    '''
    
    classCom = communicator.communicator()
    
    def __init__(self, boardView):
        '''
        Constructor, creates the slider and sets it's value to opacity stored in gsc
        '''
        super(transSlider, self).__init__(Qt.Horizontal)
        self.boardView = boardView
        self.setMaximumWidth(200)
        
        # Set minimum and maximum value of the slider, then get value from gsc
        self.setMinimum(0)
        self.setMaximum(100)
        self.setSliderPosition(self.boardView.getOpacity())
        
        # Set up and send valueChanged signal to synchronize all instances.
        self.valueChanged.connect(transSlider.spreadValue)
        self.valueChanged.emit(self.value())
        
        # Set up this instance to listen to synch signal.
        transSlider.classCom.opacitySignal.connect(self.updateSliderView)
        
        
    def updateSliderView(self, value):
        '''
        Updates the tooltip and position to display the current value in this instance.
        '''
        
        # Set tooltip
        self.toolTipString = "Card Opacity: " + str(value) + "%"
        self.setToolTip(self.toolTipString)
        
        # Set the opacity of cards
        # TODO: Make boardView static and set it once in spreadValue instead?
        self.boardView.setOpacity(value)
        
        # Set slider position (since the value might have moved in other instance)
        self.setSliderPosition(value)
        
        
    @classmethod
    def spreadValue(cls, value):
        '''
    	Emits the local value changed signal in every instance of transSlider
        '''
        
        # Update the view of all instances of transSlider to display same value.
        cls.classCom.opacitySignal.emit(value)