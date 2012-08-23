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
        # TODO: remove this
        conn = db.YatelConnection("sqlite", "/home/juan/ejemplodb.db")
        conn.init_yatel_database()
        self.open_explorer(conn)

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
                msg = self.tr("The project has been modified.\n"
                              "Do you want to save your changes before close?")
                status = QtGui.QMessageBox.warning(self, constants.PRJ, msg,
                                                   QtGui.QMessageBox.Ok,
                                                   QtGui.QMessageBox.Cancel,
                                                   QtGui.QMessageBox.Discard)
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
                status = QtGui.QMessageBox.warning(self, constants.PRJ, msg,
                                                   QtGui.QMessageBox.Ok,
                                                   QtGui.QMessageBox.Cancel)
                if status == QtGui.QMessageBox.Ok:
                    self.centralLayout.removeWidget(self.explorerFrame)
                    self.explorerFrame.destroy()
                    self.explorerFrame = None
                    return True
                # status == QtGui.QMessageBox.Cancel:
                return False
        return True

    # SLOTS
    def on_actionOpenYatelDB_triggered(self, *chk):
        if not chk:
            return
        self.dialog = connection_setup.ConnectionSetupDialog(self, "open")
        try:
            if not self.dialog.exec_():
                return 
            conn = db.YatelConnection(**self.dialog.params)
            conn.init_yatel_database()
        except Exception as err:
            QtGui.QMessageBox.critical(self, self.tr("Error"), err.msg)
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
                code = code.replace("<", "&lt;").replace(">", "&gt;")
                lines = code.splitlines()
                return "<br/>".join(lines)
            
            title = self.tr("About %1 - %2").arg(constants.PRJ,
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

