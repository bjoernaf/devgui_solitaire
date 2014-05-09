'''
Created on 9 maj 2014

@author: Max, Sven
'''
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
        

class transSlider(QSlider):
    '''
    Slider to set the transparency of cards.
    TODO: Change to move cards only later?
    '''
    def __init__(self, gsc):
        '''
        Constructor, creates the slider and sets it's value to opacity stored in gsc
        '''
        super(transSlider, self).__init__(Qt.Horizontal)
        self.gsc = gsc
        self.setSliderPosition(self.gsc.opacity)
        self.setMaximumWidth(200)
        
        # Set up and send signal to update tooltip
        self.valueChanged.connect(self.updateToolTip)
        self.valueChanged.emit(self.value())
        
    def updateToolTip(self, value):
        '''
        Updates the tooltip to display the current value
        '''
        self.toolTipString = "Card Opacity: " + str(self.value())
        self.setToolTip(self.toolTipString)
    
    def mouseMoveEvent(self, event):
        '''
        Override of mouseMoveEvent to set opacity on each move
        '''
        super(transSlider, self).mouseMoveEvent(event)
        self.gsc.opacity = self.sliderPosition()
    
    def mousePressEvent(self, event):
        '''
        Override of mousePressEvent that moves the slider to the
        position pressed on the scale, and sets the opacity in
        gameStateController accordingly.
        '''
        self.gsc.solWin.bView.scene.update()
        posClicked = self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width()
        if (self.sliderPosition() != posClicked):
            self.setValue(posClicked)
            self.gsc.opacity = self.sliderPosition()
        QSlider.mousePressEvent(self, event)
        # http://stackoverflow.com/questions/11132597/qslider-mouse-direct-jump