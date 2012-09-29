#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Implementation of a error dialog

"""

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
    """A simple implementation for create dialog using an exception
    
    """
    
    def __init__(self, title, msg, stack, parent=None):
        """Create a new instance of ErrorDialog
        
        **Params**
            :title: A text for use as title of the dialog.
            :msg: A description of the error.
            :stack: Stack trace of the error as string.
            :parent: A gui parent of this widget.
        
        """
        super(ErrorDialog, self).__init__(parent=parent)
        self.stack = stack
        self.setWindowTitle(title)
        self.messageLabel.setText(msg)
    
    @QtCore.pyqtSlot()
    def on_detailsPushButton_clicked(self):
        """Slot executed when detailsPushButton is clicked

        """
        self.stackTextBrowser = QtGui.QTextBrowser()
        self.stackTextBrowser.setText(self.stack)
        self.verticalLayout.addWidget(self.stackTextBrowser)

    
#===============================================================================
# FUNCTIONS
#===============================================================================

def critical(title, err):
    """Shorcut for show a modal dialog of a critical error
    
    **Params**
        :title: A title of the dialog.
        :err: An exception istance for extract message and stack texts
        
    """
    msg = getattr(err, "msg", None) \
        or getattr(err, "message", None)\
        or str(err)
    stack = "\n".join(traceback.format_exception(*sys.exc_info()))
    ErrorDialog(title, msg, stack).exec_()
    

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

