#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import string

from PyQt4 import QtGui
from PyQt4 import QtCore

import yatel

from yatel import constants
from yatel import db

from yatel.gui import uis
from yatel.gui import csv_wizard
from yatel.gui import resources
from yatel.gui import explorer


#===============================================================================
# CONSTANTS
#===============================================================================

ABOUT_TEMPLATE = string.Template("""
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">$title</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">$doc</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Author: </span>$author</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Version: </span>$version</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Homepage: </span><a href="$url"><span style=" text-decoration: underline; color:#0000ff;">$url</span></a></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">License: </span>$license</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"></p>
""".strip())


#===============================================================================
# MAIN WINDOW
#===============================================================================

class MainWindow(uis.UI("MainWindow.ui")):
    """The main window class"""

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(resources.get("logo.svg")))
        self.explorerFrame = None

    def setWindowTitle(self, prj=""):
        title = "{0} v.{1} - {2}".format(
            constants.PRJ, constants.STR_VERSION, prj
        )
        super(self.__class__, self).setWindowTitle(title)

    def open_explorer(self, yatel_connection):
        self.explorerFrame = explorer.ExplorerFrame(
            self.centralWidget(), yatel_connection
        )
        self.setWindowTitle(yatel_connection.name)
        self.centralLayout.addWidget(self.explorerFrame)

    def close_explorer(self):
        """Return false if the project is not closed

        """
        if self.explorerFrame:
            if not self.explorerFrame.is_saved:
                msg = self.tr(
                    "The project has been modified.\n"
                    "Do you want to save your changes before close?"
                )
                status = QtGui.QMessageBox.warning(
                    self, yatel.__prj__, msg,
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Cancel,
                    QtGui.QMessageBox.Discard
                )
                if status == QtGui.QMessageBox.Ok:
                    self.explorerFrame.save()
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    return True
                elif status == QtGui.QMessageBox.Discard:
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    return True
                # status == QtGui.QMessageBox.Cancel:
                return False
            else:
                msg = self.tr("Do you want to close the actual project?")
                status = QtGui.QMessageBox.warning(
                    self, yatel.__prj__, msg,
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Cancel
                )
                if status == QtGui.QMessageBox.Ok:
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    return True
                # status == QtGui.QMessageBox.Cancel:
                return False
        return True

    # SLOTS
    def on_actionWizard_triggered(self, *chk):
        if not chk or not self.close_explorer():
            return
        self.wizard = csv_wizard.CSVWizard(self)
        self.dialog = ConnectionSetupDialog(self)
        try:
            if not self.wizard.exec_():
                return
            haplotypes = None
            facts = None
            edges = None            
            if hasattr(self.wizard, "haplotypesFrame"):
                haplotypes = self.wizard.haplotypesFrame.dom_objects 
            if hasattr(self.wizard, "factsFrame"):
                facts = self.wizard.factsFrame.dom_objects
            if hasattr(self.wizard, "weightFrame"):
                edges = self.wizard.weightFrame.dom_objects
            if not self.dialog.exec_():
                return 
            conn = db.YatelConnection(**self.dialog.params)
            conn.init_with_values(haplotypes, facts, edges)
        except Exception as err:
            QtGui.QMessageBox.critical(self, self.tr("Error"), err.msg)
        else:
            self.open_explorer(conn)
        finally:
            self.wizard.setParent(None)
            self.wizard.destroy()
            del self.wizard
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog

    def on_actionAboutQt_triggered(self, *chk):
        if chk:
            QtGui.QApplication.aboutQt()
        
    def on_actionAbout_triggered(self, *chk):
        if chk:
            
            def richtext(code):
                code = unicode(self.tr(code))
                return "<br/>".join(
                    code.replace("<", "&lt;").replace(">", "&gt;").splitlines()
                )
            
            QtGui.QMessageBox.about(
                self, self.tr("About %1 - %2").arg(
                    constants.PRJ, constants.STR_VERSION
                ), 
                ABOUT_TEMPLATE.substitute(
                    title=richtext(constants.PRJ),
                    doc=richtext(constants.DOC),
                    author=richtext(constants.AUTHOR),
                    version=richtext(constants.STR_VERSION),
                    url=richtext(constants.URL),
                    license=richtext(constants.LICENSE)
                )
            )


#===============================================================================
# CONNECTION SETUP DIALOG
#===============================================================================

class ConnectionSetupDialog(uis.UI("ConnectionSetupDialog.ui")):
    
    def __init__(self, parent=None, *args, **kwargs):
        super(ConnectionSetupDialog, self).__init__(parent, *args, **kwargs)
        self.engineComboBox.addItems(db.ENGINES)
        self._params = {}
        self.on_engineComboBox_activated(self.engineComboBox.currentText())
    
    def on_openFileButton_pressed(self):
        filename = QtGui.QFileDialog.getSaveFileName(
            self, self.tr("Database File"),
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
            self.formLayout.insertRow(idx+2, label, lineEdit)
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
# SPLASH
#===============================================================================

class SplashScreen(QtGui.QSplashScreen):

    def __init__(self):
        pixmap = QtGui.QPixmap(resources.get("splash.png"))
        super(self.__class__, self).__init__(pixmap)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

