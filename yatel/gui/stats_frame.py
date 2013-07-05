#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOC
#===============================================================================

"""Wrapper for use matplotlib inside yatel

"""

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui

import numpy as np
from scipy import stats

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

import matplotlib.pyplot as plt

from yatel import stats

from yatel.gui import uis


#===============================================================================
# CONSTANS
#===============================================================================

_STATS = [
    ("Position stats", (
        ("Average weight", stats.average),
        ("Sum", stats.sum),
        ("Min weight", stats.amin),
        ("Q25", lambda arr: stats.percentile(arr, (25))),
        ("Median weight", stats.median),
        ("Q75", lambda arr: stats.percentile(arr, (75))),
        ("Max weight", stats.amax),
        ("Mode", lambda arr: ", ".join(map(unicode, stats.mode(arr))))
    )),
    ("Robust Position stats", (
        ("Quatile average", stats.Q),
        ("Trimedian", stats.TRI),
        ("Inter quartile average", stats.MID)
    )),
    ("Dispertion stats", (
        ("Variance", stats.var),
        ("Std. Deviation", stats.std),
        ("Range", stats.range),
        ("C. of variation", stats.variation),
        ("Average deviation", stats.MD),
        ("Median deviation", stats.MeD),
        ("Quartile variation", stats.varQ),
        ("Me. of abs. deviations", stats.MAD)           
    )),
    ("Simetry", (
        ("Pearson", stats.Sp_pearson),
        ("Yule", stats.H1_yule),
        ("Kelly", stats.H3_kelly),
    )),
    ("Kurtosis", (
        ("Kurtosis", stats.kurtosis),
        ("Robust Kurtosis", stats.K1_kurtosis),
    ))                    
]


#===============================================================================
# CLASS
#===============================================================================

class StatsFrame(uis.UI("StatsFrame.ui")):

    def __init__(self, conn, parent=None):
        super(StatsFrame, self).__init__(parent)
        self._data = []
        self._collapsed = set() 
        self._first_adjust = True
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.plotLayout.addWidget(self.toolbar)
        self.plotLayout.addWidget(self.canvas)
        # self.plotLayout.addWidget(self.button)

    def _reload_stats(self):
        self.statsTreeWidget.clear()
        for group, stats in _STATS:
            group = self.tr(group)
            group_item = QtGui.QTreeWidgetItem([group])
            for sname, sfunc in stats:
                sname = self.tr(sname)
                sval = unicode(sfunc(self._data))
                group_item.addChild(QtGui.QTreeWidgetItem([sname, sval]))
            self.statsTreeWidget.addTopLevelItem(group_item)
            if group not in self._collapsed:
                group_item.setExpanded(True)
            if self._first_adjust:
                self.statsTreeWidget.resizeColumnToContents(0)
                self._first_adjust = False
                
    def _reload_plot(self):
        # create an axis
        ax0 = self.figure.add_subplot(121)
        ax0.hold(False)
        ax0.hist(self._data)
        ax1 = self.figure.add_subplot(122)
        ax1.hold(False)
        ax1.boxplot(self._data)
        
        self.canvas.draw()

    def refresh(self, edges):
        self._data = stats.weights2array(edges)
        self._reload_stats()
        self._reload_plot()
        
    def on_statsTreeWidget_itemCollapsed(self, item):
        self._collapsed.add(item.text(0))
        
    def on_statsTreeWidget_itemExpanded(self, item):
        text = item.text(0)
        if text in self._collapsed:
            self._collapsed.remove(text)
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
