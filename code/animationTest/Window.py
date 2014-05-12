'''
Created on 12 maj 2014

@author: Sven
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QMainWindow
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QTransform, QPen
import rotating, rectangle, flipping

class Window(QMainWindow):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(Window, self).__init__()
        
        self.timer = QTimer()
        #self.timer.setInterval(100)
        
        # Create gameStateController (controller in MVC)
        scene = QGraphicsScene(0, 0, 800, 600)
        view = QGraphicsView(scene)
        self.setCentralWidget(view)
        view.setBackgroundBrush(Qt.darkGreen)
        view.show()
        
        
        rect = rectangle.rectangle(-50, -25, 100, 50)
        scene.addItem(rect)
        rect.setPos(400, 300)
        
        rect2 = rectangle.rectangle(-50, -25, 100, 50)
        scene.addItem(rect2)
        rect2.setPos(600, 300)

        
        self.rotation = rotating.rotating(rect, self)
        self.timer.timeout.connect(self.rotation.animate)
        
        self.flipping = flipping.flipping(rect2, self)
        self.timer.timeout.connect(self.flipping.animate)
        
        self.timer.start(10)
        print(self.timer.remainingTime())
        
        '''
        rectangleList = list()
        for x in range(0, 6):
            rectangleList.append(QGraphicsRectItem(-50, -25, 100, 50))
           
        
        i = 0
        for y in rectangleList:
            y.setBrush(Qt.white)
            y.setPos(400, 300+(50*i))
            transform = QTransform()
            #transform.translate(400, 300)
            transform.rotate(i*30, Qt.YAxis)
            #transform.scale(i*1.05, i*1.05)
            y.setTransform(transform)
            scene.addItem(y)
            i += 1
        '''
        
        