'''
An elementary breadboard for experimenting with Qt's Drag'n'Drop classes.
'''
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
 
def xlate_actions(actions):
    msg = 'actions:'
    if actions & Qt.CopyAction : msg += ' Copy'
    if actions & Qt.MoveAction : msg += ' Move'
    if actions & Qt.LinkAction : msg += ' Link'
    return msg
 
class SorcWidj(QLabel):
    '''A simple drag-source with ability
   to recognize the start of a drag motion
   and implement the drag.'''
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        self.mouse_down = False # has a left-click happened yet?
        self.mouse_posn = QPoint() # if so, this was where...
        self.mouse_time = QTime() # ...and this was when.
 
    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton :
            self.mouse_down = True # we are left-clicked-upon
            self.mouse_posn = event.pos() # here and...
            self.mouse_time.start() # ...now
        event.ignore()
        super().mousePressEvent(event) # pass it on up
 
    #def mouseReleaseEvent(self,event):
        ## Mouse released in our rectangle, clear any drag info.
        #print('mouseup at {0} {1}'.format(event.pos().x(),event.pos().y()))
        #self.mouse_down = False
        #event.ignore()
        #super().mouseReleaseEvent(event) # pass it on up
 
    def dragTargetChange(self, qob):
        # print signal from QDrag::targetChanged
        t = type(qob)
        print('target moved to',t)
 
    def doSomeDraggin(self, actions):
        # Create the QDrag object
        dragster = QDrag(self)
        # Make a scaled pixmap of our widget to put under the cursor.
        thumb = self.grab().scaledToHeight(50)
        dragster.setPixmap(thumb)
        dragster.setHotSpot(QPoint(thumb.width()/2,thumb.height()/2))
        # Create some data to be dragged and load it in the dragster.
        md = QMimeData()
        md.setText(self.text())
        dragster.setMimeData(md)
        # Experiment: can we catch the target-change signal?
        dragster.targetChanged.connect(self.dragTargetChange)
        # Initiate the drag, which really is a form of modal dialog.
        # Result is supposed to be the action performed at the drop.
        print('starting drag with',xlate_actions(actions))
        act = dragster.exec_(actions)
        defact = dragster.defaultAction()
        # Display the results of the drag.
        targ = dragster.target() # s.b. the widget that received the drop
        src = dragster.source() # s.b. this very widget
        print('exec returns',int(act),'default',int(defact),'target',type(targ), 'source',type(src))
        return
 
    def mouseMoveEvent(self,event):
        if self.mouse_down :
            # Mouse left-clicked and is now moving. Is this the start of a
            # drag? Note time since the click and approximate distance moved
            # since the click and test against the app's standard.
            t = self.mouse_time.elapsed()
            m = (event.pos() - self.mouse_posn).manhattanLength()
            if t >= QApplication.startDragTime() \
            or m >= QApplication.startDragDistance() :
                # Yes, a proper drag is indicated. Commence dragging.
                self.doSomeDraggin(Qt.MoveAction|Qt.LinkAction|Qt.CopyAction) #Qt.MoveAction Qt.LinkAction Qt.CopyAction
                event.accept()
                return
        # Move does not (yet) constitute a drag, ignore it.
        event.ignore()
        super().mouseMoveEvent(event)
 
class TargWidj(QLabel):
    '''A simple class that can detect an incoming drag
   and accept it, but only if it's a Copy of plain text.'''
    def __init__(self,text):
        super().__init__()
        self.setAcceptDrops(True)
        self.setText(text)
        self.move_point = QPoint(-1,-1)
 
    def dragEnterEvent(self, event):
        actions = event.possibleActions()
        self.move_point = event.pos()
        msg1 = 'drag enters at {0} {1}'.format(event.pos().x(), event.pos().y())
        msg2 = 'kbd mods {0:0x} buttons {1:0x}'.format(
            int(event.keyboardModifiers()), int(event.mouseButtons()) )
        print(msg1,msg2,'offering',xlate_actions(actions))
        if actions & Qt.CopyAction :
            event.acceptProposedAction()
        else :
            print(' -- setting copy action')
            event.setDropAction(Qt.CopyAction)
            event.accept()
 
    def dragMoveEvent(self, event):
        pos = event.pos()
        if pos != self.move_point:
            print('drag moving at {0} {1}'.format(pos.x(), pos.y()))
            self.move_point = pos
        # To illustrate forbidden areas, we mark the lower right quadrant as
        # invalid. The lower right quadrant is the rect with top-left at w/2,
        # h/2 and with size w/2, h/2. It doesn't make sense to specify this
        # over and over, but there's no other way.
        half_width = self.width()/2
        half_height = self.height()/2
        forbidden_rect = QRect(half_width,half_height,half_width,half_height)
        #event.ignore(forbidden_rect)
        if forbidden_rect.contains(pos):
            event.ignore()
        else:
            event.accept()
 
    def dragLeaveEvent(self, event):
        print('drag leaving')
        event.accept()
 
    def dropEvent(self, event):
        msg = 'dropping at {0} {1}'.format(event.pos().x(), event.pos().y())
        actions = event.dropAction()
        print(msg, xlate_actions(actions))
        if actions & Qt.CopyAction :
            event.acceptProposedAction()
        else :
            print(' -- setting copy action!')
            event.setDropAction(Qt.CopyAction)
        self.setText( event.mimeData().text() )
        event.accept()
 
def main():
    import sys
    app = QApplication(sys.argv)
    main = QMainWindow()
    central = QWidget()
    hbo = QHBoxLayout()
    hbo.addWidget( SorcWidj('Source Widget') )
    hbo.addWidget( TargWidj('Target') )
    central.setLayout(hbo)
    central.setStyleSheet(
        'QLabel {border-width:4px; border-style:groove;}')
    main.setCentralWidget( central )
    main.show()
    app.exec_()
 
if __name__ == '__main__' :
    main()