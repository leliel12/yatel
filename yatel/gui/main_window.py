#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui

import yatel
from yatel import csv2dom

from yatel.gui import uis
from yatel.gui import csv_wizard
from yatel.gui import resources


#===============================================================================
# MAIN WINDOW
#===============================================================================

class MainWindow(uis.UI("MainWindow.ui")):
    """The main window class"""
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(resources.get("logo.svg")))
    
    def setWindowTitle(self, prj=""):
        title = "{0} v.{1} - {2}".format(yatel.__prj__, yatel.__version__, prj)
        super(self.__class__, self).setWindowTitle(title)
    
    # SLOTS
    def on_actionWizard_triggered(self, *chk):
        if chk:
            self.wizard = csv_wizard.CSVWizard(self)
            self.wizard.exec_()
            
            facts = None
            if hasattr(self.wizard, "factsFrame"):
                factsFrame = self.wizard.factsFrame
                cool = factsFrame.cool.type_corrector(factsFrame.types)
                facts = csv2dom.construct_facts(cool, factsFrame.id_column)
            
            haplotypes = None
            if hasattr(self.wizard, "haplotypesFrame"):
                haplotypesFrame = self.wizard.haplotypesFrame
                cool = haplotypesFrame.cool.type_corrector(
                    haplotypesFrame.types
                )
                haplotypes = csv2dom.construct_haplotypes(
                    cool, haplotypesFrame.id_column
                )
            
            edges = None
            if hasattr(self.wizard, "weightsFrame"):
                weightsFrame = self.wizard.weightsFrame
                cool = weightsFrame.cool.type_corrector(weightsFrame.types)
                edges = csv2dom.construct_edges(cool, weightsFrame.id_column)



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

