#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import string

from PyQt4 import QtGui

import yatel

from yatel import constants

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

    def open_explorer(self, facts, haplotypes, edges):
        self.explorerFrame = explorer.ExplorerFrame(
            self.centralWidget(), haplotypes, facts, edges
        )
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
        if chk and self.close_explorer():
            
            self.wizard = csv_wizard.CSVWizard(self)

            if self.wizard.exec_():
                processing = ""
                try:
                    haplotypes = None
                    if hasattr(self.wizard, "haplotypesFrame"):
                        processing = self.wizard.haplotypesFrame.path
                        haplotypes = self.wizard.haplotypesFrame.dom_objects 
                    facts = None
                    if hasattr(self.wizard, "factsFrame"):
                        processing = self.wizard.factsFrame.path
                        facts = self.wizard.factsFrame.dom_objects
                    edges = None
                    if hasattr(self.wizard, "weightFrame"):
                        processing = self.wizard.weightFrame.path
                        edges = self.wizard.weightFrame.dom_objects
                         
                    self.wizard.destroy()
                    del self.wizard

                    processing = "render"
                    self.open_explorer(facts, haplotypes, edges)
                
                except Exception as err:
                    msg = self.tr(
                        "Error on processing '%1'\n\n%2"
                    ).arg(processing, err.message)
                    QtGui.QMessageBox.critical(
                        self, self.tr("Error on Wizard"), msg
                    )
                    
        
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
# SPLASH
#===============================================================================

class SplashScreen(QtGui.QSplashScreen):

    def __init__(self):
        pixmap = QtGui.QPixmap(resources.get("splash.png"))
        super(self.__class__, self).__init__(pixmap)


#===============================================================================
# ABOUT
#===============================================================================




#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

