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

if __name__ == "__main__":
    import matplotlib as mpl
    mpl.use('Agg')
    import sys, os
    sys.path.insert(1, os.path.join("..", ".."))
    import yatel.gui


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
# CLASS
#===============================================================================

class StatsFrame(uis.UI("StatsFrame.ui")):

    def __init__(self, parent=None):
        super(StatsFrame, self).__init__(parent)
        self._data = []
                # a figure instance to plot on
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.plotLayout.addWidget(self.toolbar)
        self.plotLayout.addWidget(self.canvas)
        #self.plotLayout.addWidget(self.button)

    def _reload_stats(self):
        for sname, sfunc in _STATS:
            sval = sfunc(self._data)
            item = QtGui.QTreeWidgetItem([sname, unicode(sval)])
            self.statsTreeWidget.addTopLevelItem(item)
#~
    def _reload_plot(self):
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.hold(False)
        # plot data
        ax.plot(self._data, '*-')
        # refresh canvas
        self.canvas.draw()

    def refresh(self, **env):
        self._data = arr
        self._reload_stats()
        self._reload_plot()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    app = yatel.gui.APP

    main = QtGui.QDialog()
    stats = StatsFrame(main)
    layout = QtGui.QVBoxLayout()
    layout.addWidget(stats)

    main.setLayout(layout)
    main.show()

    stats.refresh([1,2,3])
    sys.exit(app.exec_())
