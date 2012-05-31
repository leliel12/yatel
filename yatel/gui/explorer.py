#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui, QtCore

from yatel import constants

from yatel.gui import uis


#===============================================================================
# 
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    
    def __init__(self, parent, facts, haplotypes, edges):
       pass


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

