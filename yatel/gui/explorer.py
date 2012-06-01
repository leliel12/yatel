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
        super(ExplorerFrame, self).__init__(parent=parent)
        
        from yatel.gui import network
        
        self.is_saved = True
        self.network = network.NetworkProxy()
        self.pilasLayout.addWidget(self.network.widget)
        
        x=-400
        y=-300
        i = 0
        for h in haplotypes:
            x = x+20 if x < 800 else -400
            y = y+20 if y<600 else -300
            if i < 50:
                i +=1
            else:
                break
            self.network.add_node(h,x,y)
            print h.hap_id
            
        
    def destroy(self):
        self.network.clear()
        super(ExplorerFrame, self).destroy()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

