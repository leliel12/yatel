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
from yatel.gui import error_dialog


#===============================================================================
# GLOBALS
#===============================================================================

#: Before anything start a QAplication is created
APP = QtGui.QApplication(sys.argv)
APP.setApplicationName(yatel.PRJ)


#===============================================================================
# FUNCTIONS
#===============================================================================

def run_gui(parser=None):
    """Launch yatel gui client

    :param cli_parser: A command line parser of yatel
    :type cli_parser: a callable.

    """
    splash = main_window.SplashScreen()
    if "--serve" not in APP.arguments():
        splash.show()
    QtCore.QThread.sleep(1)
    APP.processEvents()
    win = main_window.MainWindow()
    if parser:
        try:
            _, returns = parser(APP.arguments()[1:])
            if returns.database:
                win.open_explorer(returns.database)
        except Exception as err:
            error_dialog.critical(win.tr("Error"), err)
            win.destroy()
            win = main_window.MainWindow()
    win.show()
    splash.finish(win)
    sys.exit(APP.exec_())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
