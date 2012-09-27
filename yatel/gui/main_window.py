#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import string

from PyQt4 import QtGui

from yatel import constants
from yatel import db

from yatel.gui import uis
from yatel.gui import csv_wizard
from yatel.gui import resources
from yatel.gui import explorer
from yatel.gui import connection_setup
from yatel.gui import error_dialog
from yatel.gui import version_dialog


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
        
        example_db = "/home/juan/proyectos/yatel_hg/data/example.db"
        conn = db.YatelConnection("sqlite", example_db)
        conn.init_yatel_database()
        self.open_explorer(conn)

    def reloadTitle(self):
        prj, saved = "", ""
        if self.explorerFrame:
            prj = self.explorerFrame.conn.name
            saved = "" if self.explorerFrame.is_saved() else "*"
        title = "{} v.{} - {} {}".format(constants.PRJ,
                                         constants.STR_VERSION,
                                         prj, saved)
        super(self.__class__, self).setWindowTitle(title)

    def open_explorer(self, yatel_connection, saved=True):
        self.explorerFrame = explorer.ExplorerFrame(self.centralWidget(),
                                                    yatel_connection, saved)
        self.explorerFrame.saveStatusChanged.connect(
            self.on_explorerFrame_saveStatusChanged
        )
        self.centralLayout.addWidget(self.explorerFrame)
        self.actionSave.setEnabled(not self.explorerFrame.is_saved())
        self.actionClose.setEnabled(True)
        self.actionLoad.setEnabled(True)
        self.reloadTitle()

    def close_explorer(self):
        """Return false if the project is not closed

        """
        if self.explorerFrame:
            closed = False
            if not self.explorerFrame.is_saved():
                msg = self.tr("The project has been modified.\n"
                              "Do you want to save your changes before close?")
                status = QtGui.QMessageBox.warning(self, constants.PRJ, msg,
                                                   QtGui.QMessageBox.Ok,
                                                   QtGui.QMessageBox.Cancel,
                                                   QtGui.QMessageBox.Discard)
                if status == QtGui.QMessageBox.Ok:
                    self.on_actionSave_triggered(True)
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
                status = QtGui.QMessageBox.warning(self, constants.PRJ, msg,
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
            self.reloadTitle()
            return closed
        return True

    #===========================================================================
    # SLOTS
    #===========================================================================
    
    def on_actionLoad_triggered(self, *chk):
        if chk:
            conn = self.explorerFrame.conn
            vid = version_dialog.open_version(conn)
            if isinstance(vid, int):
                version = conn.get_version(vid)
                self.explorerFrame.load_version(version)
                self.reloadTitle()
    
    def on_explorerFrame_saveStatusChanged(self, is_saved):
        self.reloadTitle()
        self.actionSave.setEnabled(not is_saved)
    
    def on_actionExit_triggered(self, *chk):
        if chk and self.close_explorer():
            self.close()
    
    def on_actionClose_triggered(self, *chk):
        if chk:
            self.close_explorer()
    
    def on_actionSave_triggered(self, *chk):
        if chk and not self.explorerFrame.is_saved():
            conn = self.explorerFrame.conn
            tag_comment = version_dialog.save_version(conn)
            if tag_comment :
                self.explorerFrame.save_version(*tag_comment)
    
    def on_actionOpenYatelDB_triggered(self, *chk):
        if not chk or not self.close_explorer():
            return
        self.dialog = connection_setup.ConnectionSetupDialog(self, "open")
        try:
            if not self.dialog.exec_():
                return 
            conn = db.YatelConnection(**self.dialog.params)
            conn.init_yatel_database()
        except Exception as err:
            error_dialog.critical(self.tr("Error"), err)
        else:
            self.open_explorer(conn)
        finally:
            self.dialog.setParent(None)
            self.dialog.destroy()
            del self.dialog
            
    def on_actionWizard_triggered(self, *chk):
        if not chk or not self.close_explorer():
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
            conn = db.YatelConnection(**self.dialog.params)
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

    def on_actionAboutQt_triggered(self, *chk):
        if chk:
            QtGui.QApplication.aboutQt()
        
    def on_actionAbout_triggered(self, *chk):
        if chk:
            
            def richtext(code):
                code = self.tr(code)
                code = code.replace("<", "&lt;").replace(">", "&gt;")
                lines = code.splitlines()
                return "<br/>".join(lines)
            
            title = self.tr("About {} - {}").format(constants.PRJ,
                                                 constants.STR_VERSION)
            about = ABOUT_TEMPLATE.substitute(title=richtext(constants.PRJ),
                                              doc=richtext(constants.DOC),
                                              author=richtext(constants.AUTHOR),
                                              version=richtext(constants.STR_VERSION),
                                              url=richtext(constants.URL),
                                              license=richtext(constants.LICENSE))
            QtGui.QMessageBox.about(self, title, about)


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

