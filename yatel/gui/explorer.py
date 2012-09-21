#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================================================
# IMPORTS
#===============================================================================

import collections

from PyQt4 import QtGui, QtCore

from yatel import topsort

from yatel.gui import uis
from yatel.gui import double_slider
from yatel.gui import version_dialog


#===============================================================================
# 
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    saveStatusChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent, yatel_connection, saved=True):
        super(ExplorerFrame, self).__init__(parent=parent)
        
        from yatel.gui import network
        
        self._is_saved = saved
        self.network = network.NetworkProxy()
        self.network.widget.setParent(self)
        self.pilasLayout.addWidget(self.network.widget)
        self.conn = yatel_connection
        self._version = None
        
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
        maxw = int(maxw) + (1 if maxw > int(maxw) else 0)
        
        self._startw, self._endw = minw, maxw
        
        self.rs = double_slider.DoubleSlider(self, "Weights", minw, maxw)
        self.rs.endValueChanged.connect(self.on_weightEnd_changed)
        self.rs.startValueChanged.connect(self.on_weightStart_changed)
        self.sliderLayout.addWidget(self.rs)
        
        self.network.node_clicked.conectar(self.on_node_clicked)
        
        # load latest version
        self.load_match_version(None)
        if self._version["id"] == 1:
            self.save_new_version("topology_added")
            
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
    
    def _set_unsaved(self):
        self._is_saved = False
        self.saveStatusChanged.emit(self._is_saved)
        
    def _add_filter(self, checked, ambient):
        facts_and_values = {}
        for att in ambient.keys():
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
            checkbox.setChecked(checked)
            for att, value in ambient.items():
                envWidget.select_attribute_value(att, value)
    
    #===========================================================================
    # SLOTS
    #===========================================================================
    
    def on_weightStart_changed(self, start):
        if start != self._startw:
            edges = tuple(self.conn.filter_edges(start, self._endw))
            self.network.filter_edges(*edges)
            self._startw = start
            self._set_unsaved()
    
    def on_weightEnd_changed(self, end):
        if end != self._endw:
            edges = tuple(self.conn.filter_edges(self._startw, end))
            self.network.filter_edges(*edges)
            self._endw = end
            self._set_unsaved()
    
    def on_addEnviromentPushButton_pressed(self):
        self.envDialog = EnviromentDialog(self,
                                          self.conn.facts_attributes_names())
        if self.envDialog.exec_():
            atts = self.envDialog.selected_attributes
            ambient = dict((att, None) for att in atts)
            self._add_filter(False, ambient)
            self._set_unsaved()
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
                check.stateChanged.disconnect(self.on_filter_changed)
                widget.removeRequested.disconnect(self.on_filter_removeRequested)
                widget.filterChanged.disconnect(self.on_filter_changed)
                self._set_unsaved()
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
        self._set_unsaved()
    
    @QtCore.pyqtSlot(int)
    def on_hapsComboBox_currentIndexChanged(self, idx):
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
        self._set_unsaved()
        for idx in range(self.hapsComboBox.count()):
            actual_hap = self.hapsComboBox.itemData(idx).toPyObject()
            if hap == actual_hap:
                self.hapsComboBox.setCurrentIndex(idx)
    
    #===========================================================================
    # PUBLIC
    #===========================================================================
    
    def load_version(self):
        vers = self.conn.versions()
        vid = version_dialog.open_version(*vers)
        if isinstance(vid, int):
           self.load_match_version(vid) 
    
    def load_match_version(self, match):
        version = self.conn.get_version(match)
        minw, maxw = version["weight_range"]
        if minw is not None:
            self.rs.setStart(minw)
        if maxw is not None:
            self.rs.setEnd(maxw)
        for hap, xy in version["topology"].items():
            self.network.move_node(hap, xy[0], xy[1])
        for checked, ambient in version["ambients"]:
            self._add_filter(checked, ambient)
        self._version = version        
    
    def is_saved(self):
        return self._is_saved
    
    def save_version(self):
        vers = self.conn.versions()
        new_version = version_dialog.save_version(*vers)
        if new_version:
            self.save_new_version(new_version)
    
    def save_new_version(self):        
        topology = self.network.topology()
        weight_range = self._startw, self._endw
        ambients = []
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            check = self.enviromentsTableWidget.cellWidget(ridx, 0)
            envwidget = self.enviromentsTableWidget.cellWidget(ridx, 1)
            ambients.append((check.isChecked(), envwidget.filters))
        self.conn.save_version(new_version, topology,
                               weight_range, ambients)
        self._is_saved = True
        self.saveStatusChanged.emit(self._is_saved)
        
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
        self.addButton.setEnabled(bool(entered))
        
    def on_selectedAttributesListWidget_currentItemChanged(self, entered, exited):
        self.removeButton.setEnabled(bool(entered))
    
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
            text = unicode(self.selectedAttributesListWidget.item(idx).text())
            atts.append(text)
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
    
    def select_attribute_value(self, name, value):
        combo = self._filters[name]
        for idx in range(combo.count()):
            avalue = combo.itemData(idx).toPyObject()
            if value == avalue:
                combo.setCurrentIndex(idx)
                break  
            
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

