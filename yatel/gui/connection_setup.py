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
to databases

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui
from PyQt4 import QtCore

import yatel
from yatel import db

from yatel.gui import uis


#===============================================================================
# CONNECTION SETUP DIALOG
#===============================================================================

class ConnectionSetupDialog(uis.UI("ConnectionSetupDialog.ui")):
    """Dialog for setup a connection to databases

    """
    #: Constant for open a dialog as open conection mode.
    OPEN = "open"

    #: Constant for open a dialog as create coneccion mode.
    CREATE = "create"

    def __init__(self, parent, action, *args, **kwargs):
        """Create a new instance of ``ConnectionSetupDialog``

        **Params**
            :parent: A gui parent of this widget.
            :action: A dialog mode
                     [ConnectionSetupDialog.OPEN|ConnectionSetupDialog.CREATE]
            :*args: Extra params for QDialog.
            :**kwags: Extra keywords arguments for QDialog.

        """
        assert action in (self.OPEN, self.CREATE)
        super(ConnectionSetupDialog, self).__init__(parent, *args, **kwargs)
        self.engineComboBox.addItems(db.ENGINES)
        self._action = action
        self._params = {}
        if action == self.OPEN:
            self.setWindowTitle(self.tr("Open Database"))
        elif action == self.CREATE:
            self.setWindowTitle(self.tr("Create Database"))
        self.on_engineComboBox_activated(self.engineComboBox.currentText())

    def on_nameLineEdit_textChanged(self, txt):
        self.okPushButton.setEnabled(bool(txt))

    def on_openFileButton_pressed(self):
        """Slot executed when a ``openFileButton`` is pressed for select an
        Sqlite file.

        If the mode is ``ConnectionSetupDialog.CREATE`` open for create a new
        file. If the mode is ``ConnectionSetupDialog.OPEN`` open for create
        read an existing file.

        """
        filename = None
        if self._action == self.CREATE:
            filename = QtGui.QFileDialog.getSaveFileName(self,
                                                         self.tr("Save Database"),
                                                         yatel.HOME_PATH,
                                                         self.tr("sqlite (*.db)"))
        elif self._action == self.OPEN:
            filename = QtGui.QFileDialog.getOpenFileName(self,
                                                         self.tr("Open Database File"),
                                                         yatel.HOME_PATH,
                                                         self.tr("sqlite (*.db)"))
        if filename:
            self.nameLineEdit.setText(filename)

    @QtCore.pyqtSlot('QString')
    def on_engineComboBox_activated(self, engine):
        """Slot executed when a ``engineComboBox`` is activated.

        This method show widgets acording to engine for configure it.

        **params**
            :engine: Engine dictionary info (see ``yatel.db``).

        """
        name_isfile = db.ENGINES_CONF[unicode(engine)]["name_isfile"]
        self.openFileButton.setVisible(name_isfile)
        self.nameLineEdit.setEnabled(not name_isfile)
        self.nameLineEdit.setText("")
        for label, lineEdit in self._params.values():
            self.formLayout.removeWidget(label)
            self.formLayout.removeWidget(lineEdit)
            label.setParent(None)
            lineEdit.setParent(None)
            label.destroy()
            lineEdit.destroy()
        self._params.clear()
        confs = sorted(db.ENGINES_CONF[unicode(engine)]["params"].items())
        for idx, conf in enumerate(confs):
            pn, pdv = conf
            label = QtGui.QLabel(pn)
            lineEdit = QtGui.QLineEdit(unicode(pdv))
            if isinstance(pdv, int):
                lineEdit.setValidator(QtGui.QIntValidator())
            self.formLayout.insertRow(idx + 2, label, lineEdit)
            self._params[pn] = (label, lineEdit)
        self.adjustSize()

    def params(self):
        """Returns a params of the conection as dictionary.

        **returns**
            A dict instance with all parameters of the engine
            (see ``yatel.db``).

        """
        data = {}
        engine = unicode(self.engineComboBox.currentText())
        data["engine"] = engine
        data["name"] = unicode(self.nameLineEdit.text())
        confs_params = db.ENGINES_CONF[engine]["params"]
        for pn, pws in self._params.items():
            lineEdit = pws[1]
            param_type = type(confs_params[pn])
            try:
                data[pn] = param_type(lineEdit.text())
            except:
                data[pn] = confs_params[pn]
        return data


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

