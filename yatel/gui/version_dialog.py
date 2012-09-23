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
    
    def __init__(self, parent, dialog_type, conn):
        super(VersionDialog, self).__init__(parent=parent)
        self.conn = conn
        if dialog_type == self.SAVE:
            self.commentBrowser.setVisible(False)
            self._existing = []
        elif dialog_type == self.OPEN:
            self.newVersionWidget.setVisible(False)
        else:
            raise ValueError("Invalid dialog_type")
        self.dialog_type = dialog_type
        self.versionsTableWidget.setRowCount(len(conn.versions()))
        for idx, ver in enumerate(conn.versions()):
            id, date, tag = ver
            idItem = QtGui.QTableWidgetItem(str(id))
            dateItem = QtGui.QTableWidgetItem(date.strftime(constants.DATETIME_FORMAT))
            tagItem = QtGui.QTableWidgetItem(tag)
            self.versionsTableWidget.setItem(idx, 0, idItem)
            self.versionsTableWidget.setItem(idx, 1, tagItem)
            self.versionsTableWidget.setItem(idx, 2, dateItem)
            if dialog_type == self.SAVE:
                self._existing.append(tag)
    
    def on_versionsTableWidget_itemSelectionChanged(self):
        row = self.versionsTableWidget.currentRow()
        id = int(self.versionsTableWidget.item(row, 0).text())
        tag = self.versionsTableWidget.item(row, 1).text()
        comment = self.conn.get_version(id)["comment"]
        if self.dialog_type == self.OPEN:
            self.acceptPushButton.setEnabled(True)
            self.commentBrowser.setText(comment)
        elif self.dialog_type == self.SAVE:
            item = self.versionsList.currentItem()
            self.versionLineEdit.setText(tag)
            self.saveCommentTextEdit.setText(comment)
    
    def on_versionLineEdit_textChanged(self, text):
        if self.dialog_type == self.SAVE \
            and unicode(text) \
            and unicode(text).strip() not in self._existing:
                self.acceptPushButton.setEnabled(True)
        else:
            self.acceptPushButton.setEnabled(False)
    
    def selected_id(self):
        row = self.versionsTableWidget.currentRow()
        return int(self.versionsTableWidget.item(row, 0).text())
        
    def new_version(self):
        tag = unicode(self.versionLineEdit.text()).strip()
        comment = unicode(self.saveCommentTextEdit.toPlainText()).strip()
        return (tag, comment)


#===============================================================================
# FUNCTIONS
#===============================================================================

def save_version(conn):
    dialog = VersionDialog(None, VersionDialog.SAVE, conn)
    if dialog.exec_():
        return dialog.new_version()

        
def open_version(conn):
    dialog = VersionDialog(None, VersionDialog.OPEN, conn)
    if dialog.exec_():
        return dialog.selected_id()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

