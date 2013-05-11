#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module contains a gui for retrieve information for create conection
remote instance of yatel

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui
from PyQt4 import QtCore

import yatel

from yatel.gui import uis


#===============================================================================
# CONNECTION SETUP DIALOG
#===============================================================================

class RemoteSetupDialog(uis.UI("RemoteSetupDialog.ui")):
    """Dialog for setup a connection to remote yatel instances

    """

    def on_hostLineEdit_textChanged(self, txt):
        port_txt = self.portLineEdit.text()
        self.okPushButton.setEnabled(bool(txt) and bool(port_txt))

    def on_portLineEdit_textChanged(self, txt):
        host_txt = self.hostLineEdit.text()
        self.okPushButton.setEnabled(bool(txt) and bool(host_txt))

    def params(self):
        """Returns a params of the conection as dictionary.

        **returns**
            A dict instance with host and port.

        """
        return {"host": self.hostLineEdit.text(),
                 "port": int(self.portLineEdit.text())}

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

