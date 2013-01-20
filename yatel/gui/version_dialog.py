#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Dialog and utilities for create and load versions.

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui

import yatel
from yatel.gui import uis


#===============================================================================
# VERSION DIALOG
#===============================================================================

class VersionDialog(uis.UI("VersionDialog.ui")):
    """A dialog for create and load versions of explorations.

    """

    #: "Create a new version" mode for the dialog.
    SAVE = "save"

    #: "Load a version" mode for the dialog.
    OPEN = "open"

    def __init__(self, parent, dialog_type, conn):
        """Create a new instance of ``VersionDialog``.

        **Params**
            :parent: The parent widget.
            :dialog_type: ``VersionDialog.SAVE`` or ``VersionDialog.OPEN``.
            :conn: The ``yatel.db.YatelConnection`` instace for extract the
                   existing versions.

        """
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
        for idx, ver in enumerate(conn.versions_infos()):
            id, date, tag = ver
            self.versionsTableWidget.insertRow(idx)
            idItem = QtGui.QTableWidgetItem(str(id))
            dateItem = QtGui.QTableWidgetItem(date.strftime(yatel.DATETIME_FORMAT))
            tagItem = QtGui.QTableWidgetItem(tag)
            self.versionsTableWidget.setItem(idx, 0, idItem)
            self.versionsTableWidget.setItem(idx, 1, tagItem)
            self.versionsTableWidget.setItem(idx, 2, dateItem)
            if dialog_type == self.SAVE:
                self._existing.append(tag)

    def on_versionsTableWidget_itemSelectionChanged(self):
        """Slot executed when a version change in the list.

        This method enabled the ``acceptPushButton``and set the comment of
        the version if this dialog is ``VersionDialog.OPEN``. In
        ``VersionDialog.SAVE`` copy the old tag and comment to the entry
        widgets.


        """
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
        """Slot executed when a tag change.

        Only usefull in ``VersionDialog.SAVE`` mode. If the new tag already
        exist this method disable the ``acceptPushButton``.


        """
        if self.dialog_type == self.SAVE \
            and unicode(text) \
            and unicode(text).strip() not in self._existing:
                self.acceptPushButton.setEnabled(True)
        else:
            self.acceptPushButton.setEnabled(False)

    def selected_id(self):
        """Return the id of the selected version

        Only usefull in ``VersionDialog.OPEN``.

        """
        row = self.versionsTableWidget.currentRow()
        return int(self.versionsTableWidget.item(row, 0).text())

    def new_version(self):
        """Return the tag and comment of the new version.

        Only usefull in ``VersionDialog.SAVE``.

        """

        tag = unicode(self.versionLineEdit.text()).strip()
        comment = unicode(self.saveCommentTextEdit.toPlainText()).strip()
        return (tag, comment)


#===============================================================================
# FUNCTIONS
#===============================================================================

def save_version(conn):
    """Shortcut for show a dialog for create a new version.

    **Params**
        :conn: The ``yatel.db.YatelConnection`` instace for extract the
               existing versions.

    **Returns**
        ``(tag, comment)`` if new version is created otherwise ``None``.

    """
    dialog = VersionDialog(None, VersionDialog.SAVE, conn)
    if dialog.exec_():
        return dialog.new_version()


def open_version(conn):
    """Shortcut for show a dialog for open an existing version.

    **Params**
        :conn: The ``yatel.db.YatelConnection`` instace for extract the
               existing versions.

    **Returns**
        ``int`` if  version is need to be open otherwise ``None``.

    """
    dialog = VersionDialog(None, VersionDialog.OPEN, conn)
    if dialog.exec_():
        return dialog.selected_id()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

