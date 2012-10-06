#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


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

from yatel import constants
from yatel.gui import main_window


#===============================================================================
# GLOBALS
#===============================================================================

#: Before anything start a QAplication is created
APP = QtGui.QApplication(sys.argv)
APP.setApplicationName(constants.PRJ);


#===============================================================================
# FUNCTIONS
#===============================================================================

def run_gui():
    """Launch yatel gui client

    """
    splash = main_window.SplashScreen()
    splash.show()
    APP.processEvents()
    win = main_window.MainWindow()
    win.show()
    QtCore.QThread.sleep(1)
    splash.finish(win)
    sys.exit(APP.exec_())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
