#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""The main container of yatel gui client

"""


#===============================================================================
# IMPORTS
#===============================================================================

import string
import webbrowser

from PyQt4 import QtGui
from PyQt4 import QtCore

import yatel
from yatel import db
from yatel import remote
from yatel.conversors import yyf2yatel
from yatel.conversors import yjf2yatel

from yatel.gui import uis
from yatel.gui import csv_wizard
from yatel.gui import resources
from yatel.gui import explorer
from yatel.gui import connection_setup
from yatel.gui import remote_setup
from yatel.gui import error_dialog
from yatel.gui import version_dialog


#===============================================================================
# CONSTANTS
#===============================================================================

#: Template for create the *About Yatel..* pop-up
ABOUT_TEMPLATE = string.Template("""
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">$title</span></p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">$doc</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;"></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">Author: </span>$author <a href="mailto:$email"><span style=" text-decoration: underline; color:#0000ff;">&lt;$email&gt;</span></a></p>
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
        """Creates a new instance of ``MainWindow``

        All params are pased to superclass

        """
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(resources.get("logo.svg")))
        self.explorerFrame = None
        self.reloadTitle()

    def reloadTitle(self):
        """Reload the window title based on status of the actual project."""
        prj, saved = "", ""
        if self.explorerFrame:
            prj = self.explorerFrame.conn.name
            saved = "" if self.explorerFrame.is_saved() else "*"
        title = "{} v.{} - {} {}".format(yatel.PRJ,
                                          yatel.STR_VERSION,
                                          prj, saved)
        super(self.__class__, self).setWindowTitle(title)

    def open_explorer(self, yatel_connection):
        """Creates a new explorer frame with a given ``yatel_connection``.

        **Params**
            :yatel_connection: A ``yatel.db.YatelConnection`` instance.

        """
        self.explorerFrame = explorer.ExplorerFrame(self.centralWidget(),
                                                    yatel_connection)
        self.explorerFrame.saveStatusChanged.connect(
            self.on_explorerFrame_saveStatusChanged
        )
        self.centralLayout.addWidget(self.explorerFrame)
        self.actionSave.setEnabled(not self.explorerFrame.is_saved())
        self.actionClose.setEnabled(True)
        self.actionLoad.setEnabled(True)
        self.menuExport.setEnabled(True)
        self.reloadTitle()

    def close_explorer(self, force=False):
        """If a project are open; ask to the user for close it.

        **Return**
            Return ``False`` if the project is not closed otherwise ``True``.

        """
        if self.explorerFrame:
            closed = False
            if force:
                self.centralLayout.removeWidget(self.explorerFrame)
                self.explorerFrame.saveStatusChanged.disconnect(
                    self.on_explorerFrame_saveStatusChanged
                )
                self.explorerFrame.setParent(None)
                self.explorerFrame.destroy()
                self.explorerFrame = None
                self.actionSave.setEnabled(False)
                closed = True
            elif not self.explorerFrame.is_saved():
                msg = self.tr("The project has been modified.\n"
                              "Do you want to save your changes before close?")
                status = QtGui.QMessageBox.warning(self, yatel.PRJ, msg,
                                                   QtGui.QMessageBox.Ok,
                                                   QtGui.QMessageBox.Cancel,
                                                   QtGui.QMessageBox.Discard)
                if status == QtGui.QMessageBox.Ok:
                    self.on_actionSave_triggered()
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.saveStatusChanged.disconnect(
                        self.on_explorerFrame_saveStatusChanged
                    )
                    self.explorerFrame.setParent(None)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    closed = True
                elif status == QtGui.QMessageBox.Discard:
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.saveStatusChanged.disconnect(
                        self.on_explorerFrame_saveStatusChanged
                    )
                    self.explorerFrame.setParent(None)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    self.actionSave.setEnabled(False)
                    closed = True
                else: # status == QtGui.QMessageBox.Cancel:
                    closed = False
            else:
                msg = self.tr("Do you want to close the actual project?")
                status = QtGui.QMessageBox.warning(self, yatel.PRJ, msg,
                                                   QtGui.QMessageBox.Ok,
                                                   QtGui.QMessageBox.Cancel)
                if status == QtGui.QMessageBox.Ok:
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.saveStatusChanged.disconnect(
                        self.on_explorerFrame_saveStatusChanged
                    )
                    self.explorerFrame.setParent(None)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    self.actionSave.setEnabled(False)
                    closed = True
                else: # status == QtGui.QMessageBox.Cancel:
                    closed = False
            if closed:
                self.actionSave.setEnabled(False)
                self.actionClose.setEnabled(False)
                self.actionLoad.setEnabled(False)
                self.menuExport.setEnabled(False)
            self.reloadTitle()
            return closed
        return True

    #===========================================================================
    # SLOTS
    #===========================================================================

    @QtCore.pyqtSlot()
    def on_actionLoad_triggered(self):
        """Slot executed when ``actionLoad`` is triggered.

        Open a popup for select other version of the actual exploration and send
        to the explorer information to recondigure the gui.

        """
        conn = self.explorerFrame.conn
        vid = version_dialog.open_version(conn)
        if isinstance(vid, int):
            version = conn.get_version(vid)
            self.explorerFrame.load_version(version)
            self.reloadTitle()

    def on_explorerFrame_saveStatusChanged(self, is_saved):
        """Slot executed when ``explorerFrame`` change the save status.

        Reload a title (acording to the new status) ad if the status is save,
        disabled the action ``actionSave``

        **Params**
            :is_saved: ``bool`` if the explorer is saved or not.

        """
        self.reloadTitle()
        self.actionSave.setEnabled(not is_saved)

    @QtCore.pyqtSlot()
    def on_actionExit_triggered(self):
        """Slot executed when ``actionExit`` is triggered.

        Close the explorer (asking for save  depending on *save-state*) and
        close the app.

        """
        if self.close_explorer():
            self.close()

    @QtCore.pyqtSlot()
    def on_actionClose_triggered(self):
        """Slot executed when ``actionClose`` is triggered.

        Close the explorer (asking for save  depending on *save-state*).

        """
        self.close_explorer()

    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        """Slot executed when ``actionSave`` is triggered.

        Show a popup for create a new version and create it.

        """
        if not self.explorerFrame.is_saved():
            conn = self.explorerFrame.conn
            tag_comment = version_dialog.save_version(conn)
            if tag_comment :
                self.explorerFrame.save_version(*tag_comment)

    @QtCore.pyqtSlot()
    def on_actionConnectToRemoteYatel_triggered(self):
        if not self.close_explorer():
            return
        self.dialog = remote_setup.RemoteSetupDialog(self)
        try:
            if not self.dialog.exec_():
                return
            conn = remote.YatelRemoteClient(**self.dialog.params())
            conn.ping()
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        else:
            self.open_explorer(conn)
        finally:
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog

    @QtCore.pyqtSlot()
    def on_actionOpenYatelDB_triggered(self):
        """Slot executed when ``actionOpenYatelDB`` is triggered.

        Show a popup to select a database that contains all the metadata
        needed to build an exploration.

        """
        if not self.close_explorer():
            return
        self.dialog = connection_setup.ConnectionSetupDialog(self, "open")
        try:
            if not self.dialog.exec_():
                return
            conn = db.YatelConnection(**self.dialog.params())
            conn.init_yatel_database()
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        else:
            self.open_explorer(conn)
        finally:
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog

    @QtCore.pyqtSlot()
    def on_actionExportYYF_triggered(self):
        """Slot executed when ``actionExportYYF`` is triggered.

        Show a file dialog for select a new name "Yatel Yaml Format" and dump
        the actual network there.

        """
        try:
            self.explorerFrame.setVisible(False)
            title = self.tr("Export Yatel Yaml Format")
            filetypes = self.tr("Yatel Yaml Format (*.yyf *.yaml *.yml)")
            filename = QtGui.QFileDialog.getSaveFileName(self, title,
                                                         yatel.HOME_PATH,
                                                         filetypes)
            if filename:
                conn = self.explorerFrame.conn
                haps = conn.iter_haplotypes()
                facts = conn.iter_facts()
                edges = conn.iter_edges()
                with open(filename, "w") as fp:
                    yyf2yatel.dump(haps, facts, edges, fp)
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        finally:
            self.explorerFrame.setVisible(True)

    @QtCore.pyqtSlot()
    def on_actionImportYYF_triggered(self):
        """Slot executed when ``actionImportYYF`` is triggered.

        Show a file dialog for select a "Yatel Yaml Format" to be imported

        """
        if not self.close_explorer():
            return
        self.dialog = connection_setup.ConnectionSetupDialog(self, "create")
        try:
            title = self.tr("Import Yatel Yaml Format")
            filetypes = self.tr("Yatel Yaml Format (*.yyf *.yaml *.yml)")
            filename = QtGui.QFileDialog.getOpenFileName(self, title,
                                                         yatel.HOME_PATH,
                                                         filetypes)
            if filename:
                with open(filename) as fp:
                    haps, facts, edges = yyf2yatel.load(fp)
            if not self.dialog.exec_():
                return
            conn = db.YatelConnection(**self.dialog.params())
            conn.init_with_values(haps, facts, edges)
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        else:
            self.open_explorer(conn, saved=False)
        finally:
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog

    @QtCore.pyqtSlot()
    def on_actionExportYJF_triggered(self):
        """Slot executed when ``actionExportYJF`` is triggered.

        Show a file dialog for select a new name "Yatel JSON Format" and dump
        the actual network there.

        """
        try:
            self.explorerFrame.setVisible(False)
            title = self.tr("Export Yatel Json Format")
            filetypes = self.tr("Yatel Json Format (*.yjf *.json)")
            filename = QtGui.QFileDialog.getSaveFileName(self, title,
                                                         yatel.HOME_PATH,
                                                         filetypes)
            if filename:
                conn = self.explorerFrame.conn
                haps = conn.iter_haplotypes()
                facts = conn.iter_facts()
                edges = conn.iter_edges()
                with open(filename, "w") as fp:
                    yjf2yatel.dump(haps, facts, edges, fp)
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        finally:
            self.explorerFrame.setVisible(True)

    @QtCore.pyqtSlot()
    def on_actionImportYJF_triggered(self):
        """Slot executed when ``actionImportYJF`` is triggered.

        Show a file dialog for select a "Yatel Json Format" to be imported

        """
        if not self.close_explorer():
            return
        self.dialog = connection_setup.ConnectionSetupDialog(self, "create")
        try:
            title = self.tr("Import Yatel Json Format")
            filetypes = self.tr("Yatel Json Format (*.yjf *.json)")
            filename = QtGui.QFileDialog.getOpenFileName(self, title,
                                                         yatel.HOME_PATH,
                                                         filetypes)
            if filename:
                with open(filename) as fp:
                    haps, facts, edges = yjf2yatel.load(fp)
            if not self.dialog.exec_():
                return
            conn = db.YatelConnection(**self.dialog.params())
            conn.init_with_values(haps, facts, edges)
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        else:
            self.open_explorer(conn, saved=False)
        finally:
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog

    @QtCore.pyqtSlot()
    def on_actionImportCSV_triggered(self):
        """Slot executed when ``actionImportCSV`` is triggered.

        Show a wizard for create a database importing ``csv`` files.

        """
        if not self.close_explorer():
            return
        self.wizard = csv_wizard.CSVWizard(self)
        self.dialog = connection_setup.ConnectionSetupDialog(self, "create")
        try:
            if not self.wizard.exec_():
                return
            haplotypes = None
            facts = None
            edges = None
            if hasattr(self.wizard, "haplotypesFrame"):
                haplotypes = self.wizard.haplotypesFrame.dom_objects ()
            if hasattr(self.wizard, "factsFrame"):
                facts = self.wizard.factsFrame.dom_objects()
            if hasattr(self.wizard, "weightFrame"):
                edges = self.wizard.weightFrame.dom_objects()
            if not self.dialog.exec_():
                return
            conn = db.YatelConnection(**self.dialog.params())
            conn.init_with_values(haplotypes, facts, edges)
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        else:
            self.open_explorer(conn, saved=False)
        finally:
            self.wizard.setParent(None)
            self.wizard.destroy()
            del self.wizard
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog

    @QtCore.pyqtSlot()
    def on_actionYatelHelp_triggered(self):
        """Slot executed when ``actionYatelHel`` is triggered.

        Open a default web browser with the latest yatel doc

        """
        webbrowser.open(yatel.DOC_URL)

    @QtCore.pyqtSlot()
    def on_actionAboutQt_triggered(self):
        """Slot executed when ``actionAboutQt`` is triggered.

        Show a default popup of ``about Qt...`` message.

        """
        QtGui.QApplication.aboutQt()

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        """Slot executed when ``actionAbout`` is triggered.

        Show a popup of ``about Yatel...`` message.

        """
        def richtext(code):
            code = self.tr(code)
            code = code.replace("<", "&lt;").replace(">", "&gt;")
            lines = code.splitlines()
            return "<br/>".join(lines)

        title = self.tr("About {} - {}").format(yatel.PRJ,
                                             yatel.STR_VERSION)
        abt = ABOUT_TEMPLATE.substitute(title=richtext(yatel.PRJ),
                                        doc=richtext(yatel.DOC),
                                        author=richtext(yatel.AUTHOR),
                                        email=richtext(yatel.EMAIL),
                                        version=richtext(yatel.STR_VERSION),
                                        url=richtext(yatel.URL),
                                        license=richtext(yatel.LICENSE))
        QtGui.QMessageBox.about(self, title, abt)

    @property
    def explorer(self):
        return self.explorerFrame


#===============================================================================
# SPLASH
#===============================================================================

class SplashScreen(QtGui.QSplashScreen):
    """Splash screen of yatel"""

    def __init__(self):
        """Creates a new instance of ``SplashScreen``."""
        pixmap = QtGui.QPixmap(resources.get("splash.png"))
        super(self.__class__, self).__init__(pixmap)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

