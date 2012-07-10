#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import collections

from PyQt4 import QtGui, QtCore

from yatel import constants
from yatel import topsort

from yatel.gui import uis


#===============================================================================
# 
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    
    def __init__(self, parent, haplotypes, facts, edges):
        super(ExplorerFrame, self).__init__(parent=parent)
        
        from yatel.gui import network
        
        self.is_saved = False
        self.network = network.NetworkProxy()
        self.pilasLayout.addWidget(self.network.widget)
        
        xysorted = self._add_xys(haplotypes, edges, self.network.widget)
        for hap, xy in xysorted.items():
            self.network.add_node(hap, x=xy[0], y=xy[1])
            self.hapsComboBox.addItem(unicode(hap.hap_id), QtCore.QVariant(hap))
            
        
        for edge in edges:
            self.network.add_edge(edge)
            
        for fact in facts:
            pass
        
        self.network.node_selected.conectar(self.on_node_selected)
    
    def _add_xys(self, haps, edges, widget):
            hapmapped = collections.OrderedDict()
            width = widget.size().width() / 2 #xs
            height = widget.size().height() / 2 #ys
            bounds = (
 -width + width / 4, height - height / 4,
                width, -height
            )            
            xysorted = topsort.xy(edges, "randomsort", bounds=bounds)
            for x, y, hap_id in xysorted:
                for hap in haps:
                    if hap.hap_id == hap_id:
                        hapmapped[hap] = (x, y)
                        break
            return hapmapped
    
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

