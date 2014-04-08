'''
Created on 7 apr 2014

@author: Sven, Bjorn
Main 
'''
import sys
from PyQt5 import QtWidgets
from view import solitaireWindow
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    solWin = solitaireWindow.solitaireWindow("Hello")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()