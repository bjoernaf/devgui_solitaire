'''
Created on 7 apr 2014

@author: Sven, Bjorn
'''

import sys
from view import solitaireWindow
from PyQt5.QtWidgets import QApplication
 
def main():
    '''
    Main, creates an app and a MainWindow with title as parameter.
    '''
    
    # Create an application
    app = QApplication(sys.argv)
    
    # Create and show the main window,
    solWin = solitaireWindow.solitaireWindow("Solitaire")
    solWin.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()