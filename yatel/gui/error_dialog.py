#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import traceback
import sys

from PyQt4 import QtGui
from PyQt4 import QtCore

from yatel.gui import uis


#===============================================================================
# CONNECTION SETUP DIALOG
#===============================================================================

class ErrorDialog(uis.UI("ErrorDialog.ui")):
    
    def __init__(self, title, msg, stack):
        super(ErrorDialog, self).__init__(parent=None)
        self.stack = stack
        self.setWindowTitle(title)
        self.messageLabel.setText(msg)
    
    @QtCore.pyqtSlot()
    def on_detailsPushButton_clicked(self):
        self.stackTextBrowser = QtGui.QTextBrowser()
        self.stackTextBrowser.setText(self.stack)
        self.verticalLayout.addWidget(self.stackTextBrowser)

    
#===============================================================================
# FUNCTIONS
#===============================================================================

def critical(title, err):
    msg = getattr(err, "msg", None) \
        or getattr(err, "message", None)\
        or str(err)
    stack = "\n".join(traceback.format_exception(*sys.exc_info()))
    return ErrorDialog(title, msg, stack).exec_()
    

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

