#===============================================================================
# IMPORTS
#===============================================================================

import sys

from PyQt4 import QtCore, QtGui

from yatel import uis


#===============================================================================
# FUNCTION
#===============================================================================


def main():
    """Run Qt application"""
    app = QtGui.QApplication(sys.argv)
    splash = uis.SplashScreen()
    splash.show()
    app.processEvents()
    main_window = uis.MainWindow()
    main_window.show()
    QtCore.QThread.sleep(1)
    splash.finish(main_window)
    sys.exit(app.exec_())    


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    main()
