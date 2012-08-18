#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================


from PyQt4 import QtGui
from PyQt4 import QtCore

from yatel import constants
from yatel import db

from yatel.gui import uis



#===============================================================================
# CONNECTION SETUP DIALOG
#===============================================================================

class ConnectionSetupDialog(uis.UI("ConnectionSetupDialog.ui")):
    
    OPEN = "open"
    CREATE = "create"
    
    def __init__(self, parent, action, *args, **kwargs):
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
    
    def on_openFileButton_pressed(self):
        filename = None
        if self._action == self.CREATE:
            filename = QtGui.QFileDialog.getSaveFileName(
                self, self.tr("Save Database"),
                constants.HOME_PATH,
                self.tr("sqlite (*.db)")
            )
        elif self._action == self.OPEN:
            filename = QtGui.QFileDialog.getOpenFileName(
                self, self.tr("Open Database File"),
                constants.HOME_PATH,
                self.tr("sqlite (*.db)")
            )
        if filename:
            self.nameLineEdit.setText(filename)
    
    @QtCore.pyqtSlot('QString')
    def on_engineComboBox_activated(self, engine):
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
            
    @property
    def params(self):
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

