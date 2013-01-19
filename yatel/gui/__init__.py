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

import yatel
from yatel.gui import main_window


#===============================================================================
# GLOBALS
#===============================================================================

#: Before anything start a QAplication is created
APP = QtGui.QApplication(sys.argv)
APP.setApplicationName(yatel.PRJ)


#===============================================================================
# FUNCTIONS
#===============================================================================

def run_gui(cli_parser=None):
    """Launch yatel gui client

    :param cli_parser: A command line parser of yatel
    :type cli_parser: a callable.

    """
    splash = main_window.SplashScreen()
    splash.show()
    QtCore.QThread.sleep(1)
    APP.processEvents()
    win = main_window.MainWindow()
    conn = cli_parser(APP.arguments())
    if conn:
        win.open_explorer(conn)
    win.show()
    splash.finish(win)
    sys.exit(APP.exec_())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
