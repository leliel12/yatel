#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import collections

from PyQt4 import QtGui, QtCore

from yatel import topsort

from yatel.gui import uis


#===============================================================================
# 
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    
    def __init__(self, parent, yatel_connection):
        super(ExplorerFrame, self).__init__(parent=parent)
        
        from yatel.gui import network
        
        self.is_saved = False
        self.network = network.NetworkProxy()
        self.network.widget.setParent(self)
        self.pilasLayout.addWidget(self.network.widget)
        self.conn = yatel_connection
        
        haplotypes = tuple(self.conn.iter_haplotypes())
        edges = tuple(self.conn.iter_edges())
        xysorted = self._add_xys(haplotypes, edges, self.network.widget)
        for hap, xy in xysorted.items():
            self.network.add_node(hap, x=xy[0], y=xy[1])
            self.hapsComboBox.addItem(unicode(hap.hap_id), QtCore.QVariant(hap))
        
        minw, maxw = None, None
        for edge in edges:
            self.network.add_edge(edge)
            if maxw < edge.weight or minw is None:
                maxw = edge.weight
            if minw > edge.weight or maxw is None:
                minw = edge.weight
                
        minw = minw or 0
        maxw = maxw or 0
        minw = int(minw) - (1 if minw > int(minw) else 0)
        maxw = int(maxw) + (1 if maxw >  int(maxw) else 0)
            
        self.edgesLimitSlider.setMinimum(minw)
        self.edgesLimitSlider.setMaximum(maxw)
        self.edgesLimitSlider.setSliderPosition(maxw)
        
        self.network.node_clicked.conectar(self.on_node_clicked)
    
    def _add_xys(self, haps, edges, widget):
            hapmapped = collections.OrderedDict()
            width = widget.size().width() / 2 #xs
            height = widget.size().height() / 2 #ys
            bounds = (-width + width / 4,
                      height - height / 4,
                      width, -height)            
            xysorted = topsort.xy(edges, "randomsort", bounds=bounds)
            for x, y, hap_id in xysorted:
                for hap in haps:
                    if hap.hap_id == hap_id:
                        hapmapped[hap] = (x, y)
                        break
            return hapmapped
    
    #===========================================================================
    # SLOTS
    #===========================================================================
    
    def on_addEnviromentPushButton_pressed(self):
        self.envDialog = EnviromentDialog(
            self, self.conn.facts_attributes_names()
        )
        if self.envDialog.exec_():
            atts = self.envDialog.selected_attributes
            facts_and_values = {}
            for att in atts:
                facts_and_values[att] = self.conn.get_fact_attribute_values(att)
            if facts_and_values:
                row = self.enviromentsTableWidget.rowCount()
                self.enviromentsTableWidget.insertRow(row)
                envWidget = EnviromentListItem(env=facts_and_values)
                checkbox = QtGui.QCheckBox()
                checkbox.stateChanged.connect(self.on_filter_changed)
                envWidget.filterChanged.connect(self.on_filter_changed)
                envWidget.removeRequested.connect(self.on_filter_removeRequested)
                self.enviromentsTableWidget.setCellWidget(row, 0, checkbox)
                self.enviromentsTableWidget.setCellWidget(row, 1, envWidget)
                self.enviromentsTableWidget.resizeRowToContents(row)
                self.enviromentsTableWidget.resizeColumnsToContents()
        self.envDialog.setParent(None)
        self.envDialog.destroy()
        del self.envDialog
    
    def on_filter_removeRequested(self, widget):
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            if self.enviromentsTableWidget.cellWidget(ridx, 1) == widget:
                check = self.enviromentsTableWidget.cellWidget(ridx, 0)
                if check.isChecked():
                    check.setChecked(False)
                    self.on_filter_changed()
                self.enviromentsTableWidget.removeRow(ridx)
                break
    
    def on_filter_changed(self):
        haps = []
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            check = self.enviromentsTableWidget.cellWidget(ridx, 0)
            if check.isChecked():
                envwidget = self.enviromentsTableWidget.cellWidget(ridx, 1)
                for hap in self.conn.ambient(**envwidget.filters):
                    haps.append(hap)
        if haps:
            self.network.highlight_nodes(*haps)
        else:
            self.network.unhighlightall()
                
    def on_hapsComboBox_currentIndexChanged(self, idx):
        if isinstance(idx, int):
            hap = self.hapsComboBox.itemData(idx).toPyObject()
            atts = hap.items_attrs()
            
            self.network.select_node(hap)
            self.attTableWidget.clearContents()
            self.attTableWidget.setRowCount(len(atts))
            
            for idx, atts in enumerate(atts):
                nameitem = QtGui.QTableWidgetItem(atts[0])
                valueitem = QtGui.QTableWidgetItem(unicode(atts[1]))
                self.attTableWidget.setItem(idx, 0, nameitem)
                self.attTableWidget.setItem(idx, 1, valueitem)
    
    def on_node_clicked(self, evt):
        hap = evt["node"]
        for idx in range(self.hapsComboBox.count()):
            actual_hap = self.hapsComboBox.itemData(idx).toPyObject()
            if hap == actual_hap:
                self.hapsComboBox.setCurrentIndex(idx)
    
    def on_edgesLimitSlider_valueChanged(self, v):
        edges = tuple(self.conn.filter_edges(0, v))
        self.network.filter_edges(*edges)

    #===========================================================================
    # SAVE & DESTROY
    #===========================================================================
    
    def save(self):
        pass
        
    def destroy(self):
        self.network.clear()
        self.pilasLayout.removeWidget(self.network.widget)
        super(ExplorerFrame, self).destroy()


#===============================================================================
# EVIROMENT DIALOG
#===============================================================================

class EnviromentDialog(uis.UI("EnviromentDialog.ui")):
    
    def __init__(self, parent, facts_names):
        super(EnviromentDialog, self).__init__(parent=parent)
        self.factAttributesListWidget.addItems(facts_names)
        self.factAttributesListWidget.sortItems()
    
    def on_factAttributesListWidget_currentItemChanged(self, entered, exited):
        self.addButton.setEnabled(
            bool(entered)
        )
        
    def on_selectedAttributesListWidget_currentItemChanged(self, entered, exited):
        self.removeButton.setEnabled(
            bool(entered)
        )
    
    def on_addButton_pressed(self):
        idx = self.factAttributesListWidget.currentIndex().row()
        item = self.factAttributesListWidget.takeItem(idx)
        if item:
            self.selectedAttributesListWidget.addItem(item)
            self.selectedAttributesListWidget.sortItems()
            self.factAttributesListWidget.sortItems()
        
    def on_removeButton_pressed(self):
        idx = self.selectedAttributesListWidget.currentIndex().row()
        item = self.selectedAttributesListWidget.takeItem(idx)
        if item:
            self.factAttributesListWidget.addItem(item)
            self.selectedAttributesListWidget.sortItems()
            self.factAttributesListWidget.sortItems()
        
    @property
    def selected_attributes(self):
        atts = []
        for idx in range(self.selectedAttributesListWidget.count()):
            atts.append(
                unicode(self.selectedAttributesListWidget.item(idx).text())
            )
        return tuple(atts)


#===============================================================================
# ENVIROMENT LIST ITEM
#===============================================================================

class EnviromentListItem(uis.UI("EnviromentListItem.ui")):
    
    filterChanged = QtCore.pyqtSignal()
    removeRequested = QtCore.pyqtSignal('QWidget')
    
    def __init__(self, env):
        super(EnviromentListItem, self).__init__()
        self._filters = {}
        for k, values in sorted(env.items()):
            label = QtGui.QLabel(k)
            self.envLayout.addWidget(label)
            combo = QtGui.QComboBox()
            combo.addItem("", QtCore.QVariant(None))
            for v in values:
                combo.addItem(unicode(v), QtCore.QVariant(v))
            self.envLayout.addWidget(combo)
            combo.currentIndexChanged.connect(self.on_combo_currentIndexChanged)
            self._filters[k] = combo
        self.setVisible(True)
        
    def on_combo_currentIndexChanged(self, idx):
        self.filterChanged.emit()
    
    @QtCore.pyqtSlot()
    def on_removeButton_clicked(self):
        self.removeRequested.emit(self)
    
    @property
    def filters(self):
        f = {}
        for label_text, combo in self._filters.items():
            idx = combo.currentIndex()
            value = combo.itemData(idx).toPyObject()
            if isinstance(value, QtCore.QString):
                value = unicode(value)
            f[label_text] = value
        return f


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

