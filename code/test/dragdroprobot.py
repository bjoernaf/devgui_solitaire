#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2006-2006 Trolltech ASA. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## Licensees holding a valid Qt License Agreement may use this file in
## accordance with the rights, responsibilities and obligations
## contained therein.  Please consult your licensing agreement or
## contact sales@trolltech.com if any conditions of this licensing
## agreement are not clear to you.
##
## Further information about Qt licensing is available at:
## http://www.trolltech.com/products/qt/licensing.html or by
## contacting info@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from math import sin, cos
#rom PySide import QtCore, QtGui
from PyQt5 import QtCore

from PyQt5.QtCore import (
    Qt,
    QMimeData,
    QPoint,
    QRect,
    QTime
)
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QWidget
)

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QFont, QColor, QPen, QPixmap, QPainter, QBrush)
from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsItem)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QGraphicsTextItem, QGraphicsScene, QGraphicsView)


class ColorItem(QGraphicsItem):
    n = 0

    def __init__(self):
        QGraphicsItem.__init__(self)

        self.color = QColor(QtCore.qrand() % 256, QtCore.qrand() % 256,
                QtCore.qrand() % 256)
        self.setToolTip(
            "QColor(%d,%d,%d)\nClick and drag this color onto the robot!" %
              (self.color.red(), self.color.green(), self.color.blue())
        )
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def boundingRect(self):
        return QtCore.QRectF(-15.5, -15.5, 34, 34)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-12, -12, 30, 30)
        #painter.setPen(QtGui.QPen(Qt.black, 1))
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(-15, -15, 30, 30)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return

        drag = QDrag(event.widget())
        mime = QtCore.QMimeData()
        drag.setMimeData(mime)

        ColorItem.n += 1
        if (ColorItem.n > 2) and ((QtCore.qrand()%3) == 0):
            image = QtGui.QImage(":/images/head.png")
            mime.setImageData(image)
            drag.setPixmap(QtGui.QPixmap.fromImage(image).scaled(30,40))
            drag.setHotSpot(QtCore.QPoint(15, 30))
        else:
            c = self.color
            mime.setColorData(c)
            mime.setText("#%02x%02x%02x" % (c.red(), c.green(), c.blue()))

            pixmap = QPixmap(34, 34)
            pixmap.fill(QtCore.Qt.white)
            painter = QPainter(pixmap)
            painter.translate(15, 15)
            #painter.setRenderHint(QtGui.QPainter.Antialiasing)
            self.paint(painter, None, None)
            painter.end()
            pixmap.setMask(pixmap.createHeuristicMask())

            drag.setPixmap(pixmap)
            drag.setHotSpot(QtCore.QPoint(15, 20))

        drag.exec_()


class RobotPart(QGraphicsItem):
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)

        # NOTE: simply doing "self.color = QtCore.Qt.lightGray" doesn't work
        #   because QtCore.Qt.lightGray is a QtCore.GlobalColor object,
        #   which has no "light" method, which will be called later
        self.color = QColor(QtCore.Qt.lightGray)
        self.pixmap = None
        self.dragOver = False
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasColor() or \
          (isinstance(self, RobotHead) and event.mimeData().hasImage()):
            event.setAccepted(True)
            self.dragOver = True
            self.update()
        else:
            event.setAccepted(False)

    def dragLeaveEvent(self, event):
        self.dragOver = False
        self.update()

    def dropEvent(self, event):
        self.dragOver = False
        if event.mimeData().hasColor():
            self.color = QColor(event.mimeData().colorData())
        elif event.mimeData().hasImage():
            self.pixmap = QtGui.QPixmap(event.mimeData().imageData())

        self.update()


class RobotHead(RobotPart):
    def boundingRect(self):
        return QtCore.QRectF(-15, -50, 30, 50)

    def paint(self, painter, option, widget=None):
        if not self.pixmap:
            painter.setBrush(self.dragOver and self.color.lighter(130)
                                            or self.color)
            painter.drawRoundedRect(-10, -30, 20, 30, 25, 25,
                    QtCore.Qt.RelativeSize)
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(-7, -3 - 20, 7, 7)
            painter.drawEllipse(0, -3 - 20, 7, 7)
            painter.setBrush(QtCore.Qt.black)
            painter.drawEllipse(-5, -1 - 20, 2, 2)
            painter.drawEllipse(2, -1 - 20, 2, 2)
            painter.setPen(QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawArc(-6, -2 - 20, 12, 15, 190 * 16, 160 * 16)
        else:
            #painter.scale(.2272, .2824)
            painter.drawPixmap(QtCore.QPointF(-15*4.4, -50*3.54), self.pixmap)


class RobotTorso(RobotPart):
    def boundingRect(self):
        return QtCore.QRectF(-30, -20, 60, 60)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.dragOver and self.color.lighter(130)
                                        or self.color)
        painter.drawRoundedRect(-20, -20, 40, 60, 25, 25,
                QtCore.Qt.RelativeSize)
        painter.drawEllipse(-25, -20, 20, 20)
        painter.drawEllipse(5, -20, 20, 20)
        painter.drawEllipse(-20, 22, 20, 20)
        painter.drawEllipse(0, 22, 20, 20)


class RobotLimb(RobotPart):
    def boundingRect(self):
        return QtCore.QRectF(-5, -5, 40, 10)

    def paint(self, painter, option, widget=None):
        painter.setBrush(self.dragOver and self.color.lighter(130) or self.color)
        painter.drawRoundedRect(self.boundingRect(), 50, 50,
                QtCore.Qt.RelativeSize)
        painter.drawEllipse(-5, -5, 10, 10)


class Robot(RobotPart):
    def __init__(self):
        RobotPart.__init__(self)

        self.torsoItem         = RobotTorso(self)
        self.headItem          = RobotHead(self.torsoItem)
        self.upperLeftArmItem  = RobotLimb(self.torsoItem)
        self.lowerLeftArmItem  = RobotLimb(self.upperLeftArmItem)
        self.upperRightArmItem = RobotLimb(self.torsoItem)
        self.lowerRightArmItem = RobotLimb(self.upperRightArmItem)
        self.upperRightLegItem = RobotLimb(self.torsoItem)
        self.lowerRightLegItem = RobotLimb(self.upperRightLegItem)
        self.upperLeftLegItem  = RobotLimb(self.torsoItem)
        self.lowerLeftLegItem  = RobotLimb(self.upperLeftLegItem)

        self.timeline = QtCore.QTimeLine()
        self.timeline.setUpdateInterval(1000/25)
        self.timeline.setCurveShape(QtCore.QTimeLine.SineCurve)
        self.timeline.setLoopCount(0)
        self.timeline.setDuration(2000)

        settings = [
        #             item               position    rotation at
        #                                 x    y    time 0  /  1
            ( self.headItem,              0,  -18,      20,   -20 ),
            ( self.upperLeftArmItem,    -15,  -10,     190,   180 ),
            ( self.lowerLeftArmItem,     30,    0,      50,    10 ),
            ( self.upperRightArmItem,    15,  -10,     300,   310 ),
            ( self.lowerRightArmItem,    30,    0,       0,   -70 ),
            ( self.upperRightLegItem,    10,   32,      40,   120 ),
            ( self.lowerRightLegItem,    30,    0,      10,    50 ),
            ( self.upperLeftLegItem,    -10,   32,     150,    80 ),
            ( self.lowerLeftLegItem,     30,    0,      70,    10 ),
            ( self.torsoItem,             0,    0,       5,   -20 )
        ]

        self.timeline.start()

    def boundingRect(self):
        return QtCore.QRectF()

    def paint(self, painter, option, widget=None):
        pass


if __name__=="__main__":
    import sys

    app = QApplication(sys.argv)

    QtCore.qsrand(QtCore.QTime(0, 0, 0).secsTo(QtCore.QTime.currentTime()))

    scene = QGraphicsScene(-200, -200, 400, 400)
    for i in range(10):
        item = ColorItem()
        angle = i*6.28 / 10.0
        item.setPos(sin(angle)*150, cos(angle)*150)
        scene.addItem(item)

    robot = Robot()
    #robot.scale(1.2)
    robot.setPos(0, -20)
    scene.addItem(robot)

    view = QGraphicsView(scene)
    #view.setRenderHint(QPainter.Antialiasing)
    view.setBackgroundBrush(QColor(230, 200, 167))
    view.setWindowTitle(view.tr("Drag and Drop Robot"))
    view.show()

    sys.exit(app.exec_())
