'''
Created on 9 maj 2014

@author: Max, Sven
'''
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class transSlider(QSlider):
    '''
    Slider to set transparency
    '''

    def __init__(self, gsc):
        super(transSlider, self).__init__(Qt.Horizontal)
        self.gsc = gsc
        self.setSliderPosition(self.gsc.opacity)
        self.setMaximumWidth(200)
        self.setToolTip("Card Opacity")
    
    def mouseMoveEvent(self, event):
        super(transSlider, self).mouseMoveEvent(event)
        self.gsc.opacity = self.sliderPosition()
    
    def mousePressEvent(self, event):
        self.gsc.solWin.bView.scene.update()
        posClicked = self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width()
        if (self.sliderPosition() != posClicked):
            self.setValue(posClicked)
            self.gsc.opacity = self.sliderPosition()
        QSlider.mousePressEvent(self, event)
        # http://stackoverflow.com/questions/11132597/qslider-mouse-direct-jump