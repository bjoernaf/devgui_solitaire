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
    
    def mouseMoveEvent(self, pos):
        super(transSlider, self).mouseMoveEvent(pos)
        self.gsc.opacity = self.sliderPosition()
        print("slider moved")
        print(self.sliderPosition())
        self.gsc.solWin.bView.scene.update()