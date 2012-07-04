#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui

import yatel

from yatel.gui import uis
from yatel.gui import csv_wizard
from yatel.gui import resources
from yatel.gui import explorer


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
        title = "{0} v.{1} - {2}".format(yatel.__prj__, yatel.__version__, prj)
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

                facts = self.wizard.factsFrame.dom_objects \
                    if hasattr(self.wizard, "factsFrame") \
                    else None

                haplotypes = self.wizard.haplotypesFrame.dom_objects \
                    if hasattr(self.wizard, "haplotypesFrame") \
                    else None

                edges = self.wizard.weightFrame.dom_objects \
                    if hasattr(self.wizard, "weightFrame") \
                    else None

                self.wizard.destroy()
                del self.wizard

                self.open_explorer(facts, haplotypes, edges)


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

