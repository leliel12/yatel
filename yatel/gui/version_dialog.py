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
# VERSION DIALOG
#===============================================================================

class VersionDialog(uis.UI("VersionDialog.ui")):
    
    SAVE = 0
    OPEN = 10
    
    def __init__(self, parent, dialog_type, *vers):
        super(VersionDialog, self).__init__(parent=parent)
        if dialog_type == self.SAVE:
            self.newVersionWidget.setVisible(True)
            self._existing = []
        elif dialog_type == self.OPEN:
            self.newVersionWidget.setVisible(False)
        else:
            raise ValueError("Invalid dialog_type")
        self.dialog_type = dialog_type
        for id, date, name in sorted(vers, reverse=True):
            item = QtGui.QListWidgetItem(name)
            item.setToolTip(self.tr("Saved at: ") 
                            + date.strftime(constants.DATETIME_FORMAT))
            item.setData(QtGui.QListWidgetItem.UserType, QtCore.QVariant(id))
            self.versionsList.addItem(item)
            if dialog_type == self.SAVE:
                self._existing.append(name)
    
    def on_versionsList_itemSelectionChanged(self):
        if self.dialog_type == self.OPEN:
            self.acceptPushButton.setEnabled(True)
        elif self.dialog_type == self.SAVE:
            item = self.versionsList.currentItem()
            self.versionLineEdit.setText(item.text())
    
    def on_versionLineEdit_textChanged(self, text):
        if self.dialog_type == self.SAVE \
            and unicode(text) \
            and unicode(text).strip() not in self._existing:
                self.acceptPushButton.setEnabled(True)
        else:
            self.acceptPushButton.setEnabled(False)
    
    @property
    def selected_id(self):
        item = self.versionsList.currentItem()
        return item.data(QtGui.QListWidgetItem.UserType).toPyObject()
        
    @property
    def new_version(self):
        return unicode(self.versionLineEdit.text()).strip()


#===============================================================================
# FUNCTIONS
#===============================================================================

def save_version(*vers):
    dialog = VersionDialog(None, VersionDialog.SAVE, *vers)
    if dialog.exec_():
        return dialog.new_version

        
def open_version(*vers):
    dialog = VersionDialog(None, VersionDialog.OPEN, *vers)
    if dialog.exec_():
        return dialog.selected_id


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

