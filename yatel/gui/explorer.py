#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui, QtCore

from yatel import constants

from yatel.gui import uis
from yatel.gui.utils import topsort
from yatel.gui.utils import randomsort


#===============================================================================
# 
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    
    def __init__(self, parent, haplotypes, facts, edges):
        super(ExplorerFrame, self).__init__(parent=parent)
        
        from yatel.gui import network
        
        def add_xys(haps, edges, widget):
            hapmapped = {}
            width = widget.size().width() / 2 #xs
            height = widget.size().height() / 2 #ys
            bounds = (
                -width + width/4, height - height/4,
                width, -height
            )            
            xysorted = randomsort.xysort(edges, bounds=bounds)
            for hap_id, xy in xysorted.items():
                for hap in haps:
                    if hap.hap_id == hap_id:
                        hapmapped[hap] = xy
                        break
            return hapmapped
        
        self.is_saved = False
        self.network = network.NetworkProxy()
        self.pilasLayout.addWidget(self.network.widget)
        
        xysorted = add_xys(haplotypes, edges, self.network.widget)
        for hap, xy in xysorted.items():
            self.network.add_node(hap, x=xy[0], y=xy[1])
        
        for edge in edges:
            self.network.add_edge(edge)
            
        for fact in facts:
            pass
        
        self.network.node_selected.conectar(self.on_node_selected)
            
            
    def on_node_selected(self, evt):
        print id(self), evt
        
    def save(self):
        pass
        
    def destroy(self):
        self.network.clear()
        self.pilasLayout.removeWidget(self.network.widget)
        self.setParent(None)
        super(ExplorerFrame, self).destroy()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

