'''
Created on 12 maj 2014

@author: Sven
'''
import sys
from PyQt5.QtWidgets import QApplication
import Window
 
def main():
    '''
    Main, creates an app and a gameStateController
    '''
    
    # Create an application and set properties
    app = QApplication(sys.argv)
    
    widget = Window.Window()
    widget.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()