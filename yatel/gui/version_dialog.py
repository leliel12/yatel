#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================


from PyQt4 import QtGui
from PyQt4 import QtCore

from yatel import constants
from yatel.gui import uis


#===============================================================================
# CONNECTION SETUP DIALOG
#===============================================================================

class VersionDialog(uis.UI("VersionDialog.ui")):
    
    def __init__(self, parent, *vers):
        super(VersionDialog, self).__init__(parent=parent)
        for id, date, name in sorted(vers, reverse=True):
            item = QtGui.QListWidgetItem(name)
            item.setToolTip(self.tr("Saved at: ") 
                            + date.strftime(constants.DATETIME_FORMAT))
            item.setData(QtGui.QListWidgetItem.UserType, QtCore.QVariant(id))
            self.versionsList.addItem(item)
    
    def on_versionsList_itemSelectionChanged(self):
        self.acceptPushButton.setEnabled(True)
    
    @property
    def selected_id(self):
        item = self.versionsList.currentItem()
        return item.data(QtGui.QListWidgetItem.UserType).toPyObject()
            
    

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

