#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# DOC
#===============================================================================

"""This packages contains all the definition, logic and resources for build
a gui of yatel

"""

#===============================================================================
# IMPORTS
#===============================================================================

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

import sys

from PyQt4 import QtCore, QtGui

from yatel.gui import main_window


#===============================================================================
# FUNCTIONS
#===============================================================================

def run_gui():
    app = QtGui.QApplication(sys.argv)
    splash = main_window.SplashScreen()
    splash.show()
    app.processEvents()
    win = main_window.MainWindow()
    win.show()
    QtCore.QThread.sleep(1)
    splash.finish(win)
    sys.exit(app.exec_())    


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
