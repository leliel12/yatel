#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Dialog for show all the facts of a given haplotype

"""

#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui
from PyQt4 import QtCore

from yatel.gui import uis


#===============================================================================
# WIDGET
#===============================================================================

class FactsDialog(uis.UI("FactsDialog.ui")):

    def __init__(self, parent, hap_id, attrs, facts):
        super(FactsDialog, self).__init__(parent)
        title = self.tr("Haplotype '{}' Facts").format(hap_id)
        self.setWindowTitle(title)
        self.titleLabel.setText(title)

        attrs = sorted(attrs)
        self.attrsTableWidget.setColumnCount(len(attrs))
        self.attrsTableWidget.setHorizontalHeaderLabels(attrs)
        for ridx, fact in enumerate(facts):
            self.attrsTableWidget.setRowCount(ridx + 1)
            for cidx, attr in enumerate(attrs):
                value = unicode(fact.get_attr(attr, "-"))
                newitem = QtGui.QTableWidgetItem(value)
                self.attrsTableWidget.setItem(ridx, cidx, newitem)
        self.attrsTableWidget.resizeColumnsToContents()


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    pass
