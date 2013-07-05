#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module contains a gui of the main widget.

"""


#===============================================================================
# IMPORTS
#===============================================================================

from PyQt4 import QtGui, QtCore

from yatel.gui import uis
from yatel.gui import qrangeslider
from yatel.gui import error_dialog
from yatel.gui import sheditor
from yatel.gui import ipython
from yatel.gui import network
from yatel.gui import facts_dialog
from yatel.gui import stats_frame


#===============================================================================
# CLASS
#===============================================================================

class ExplorerFrame(uis.UI("ExplorerFrame.ui")):
    """This is the frame make all explorations

    """

    # : Signal emited when the save status of the exploration is chaged.
    saveStatusChanged = QtCore.pyqtSignal(bool)

    def __init__(self, parent, yatel_connection):
        """Create a new instance of ``ExplorerFrame``, also load the latest
         version from a database (if the latest version hasn't topology info
         create a new one with a random topology).

        **Params**
            :parent: A gui parent of this widget.
            :action: A conection to the database.
            :saved: If the status of the connection is saved.

        """
        super(ExplorerFrame, self).__init__(parent=parent)

        # internal propuses
        self._version = ()
        self._is_saved = None

        self.conn = yatel_connection

        # ipython
        self.ipythonWidget = ipython.IPythonWidget(self.tr(
            "\nUse:\n"
            "  'win' -> is the main window.\n"
            "  'win.explorer' -> the frame of the actual project.\n"
            "  'win.explorer.conn' -> context connection\n"
            "  'win.explorer.network' ->  the network graph\n"
        ))
        self.consoleLayout.addWidget(self.ipythonWidget)
        self.ipythonWidget.reset_ns(win=self.parent().parent())

        # plot
        self.stats_frame = stats_frame.StatsFrame(self)
        self.statsLayout.addWidget(self.stats_frame)

        # sigma
        self.network = network.Network(self)
        self.network.node_clicked.connect(self.on_node_clicked)
        self.networkLayout.addWidget(self.network)

        # sql
        self.hapSQLeditor = sheditor.HiglightedEditor("sql")
        self.hapSQLLayout.addWidget(self.hapSQLeditor)
        self.hapSQLeditor.textChanged.connect(self.on_hapSQLeditor_textChanged)

        # range slider
        minw, maxw = [e.weight or 0 for e in self.conn.minmax_edges()]
        minw = int(minw) - (1 if minw > int(minw) else 0)
        maxw = int(maxw) + (1 if maxw > int(maxw) else 0)

        self.rs = qrangeslider.QRangeSlider(minw, maxw, parent=self)
        self.rs.rangeChanged.connect(self.on_weightRange_changed)
        self.sliderLayout.addWidget(self.rs)


        # layout
        self.hSplitter.setSizes(
            [parent.parent().size().width() / 2] * self.hSplitter.count()
        )
        self.vSplitter.setSizes(
            [parent.parent().size().height() / 2] * self.vSplitter.count()
        )

        # load latest version
        self.filterTabWidget.setCurrentIndex(0)
        version = self.conn.get_version()  # the latest
        self.load_version(version)
        if version["id"] == 1:
            self.save_version("topology_added", "added topological info")

        self.network.center()

    def _set_save_status(self, status):
        self._is_saved = status
        self.saveStatusChanged.emit(self._is_saved)

    def _add_filter(self, checked, enviroment):
        facts_and_values = {}
        for att in enviroment.keys():
            facts_and_values[att] = self.conn.fact_attribute_values(att)
        if facts_and_values:
            row = self.enviromentsTableWidget.rowCount()
            self.enviromentsTableWidget.insertRow(row)
            envWidget = EnviromentListItem(env=facts_and_values)
            envWidget.filterChanged.connect(self.on_filter_changed)
            envWidget.removeRequested.connect(self.on_filter_removeRequested)
            self.enviromentsTableWidget.setCellWidget(row, 0, envWidget)
            envWidget.set_active(checked)
            for att, value in enviroment.items():
                envWidget.select_attribute_value(att, value)
            size = envWidget.size().height() \
                   if row == 0 else \
                   self.enviromentsTableWidget.rowHeight(0)
            self.enviromentsTableWidget.setRowHeight(row, size)

    #===========================================================================
    # SLOTS
    #===========================================================================

    @QtCore.pyqtSlot()
    def on_factsPushButton_clicked(self):
        idx = self.hapsComboBox.currentIndex()
        hap = self.conn.haplotype_by_id(self.hapsComboBox.itemData(idx))
        dialog = facts_dialog.FactsDialog(self, hap,
                                          self.conn.fact_attributes_names(),
                                          self.conn.facts_by_haplotype(hap))
        dialog.exec_()


    def on_haplotypesNamesCheckBox_stateChanged(self, state):
        """Slot executed when ``haplotypesNamesCheckBox`` state changed.

        If the ``state`` is *True* the names of the haplotypes are showed.

        **Params**
            :state: ``bool`` value if the checkbox is checked or not.

        """
        self.network.show_haps_names(bool(state))

    def on_weightsCheckBox_stateChanged(self, state):
        """Slot executed when ``weightsCheckBox`` state changed.

        If the ``state`` is *True* the weights of the edges are showed.

        **Params**
            :state: ``bool`` value if the checkbox is checked or not.

        """
        self.network.show_weights(bool(state))

    @QtCore.pyqtSlot(int)
    def on_filterTabWidget_currentChanged(self, idx):
        """Slot executed when ``filterTabWidget`` tab change.

        If the ``idx`` is *0* the execute the slot ``on_filter_changed``
        otherwise ``NetworkProxy.unhighlightall``.

        Save status is setted  to ``False``.

        **Params**
            :idx: Index of the current tab as ``int``.

        """
        if idx == 0:
            self.on_filter_changed()
        else:
            self.network.unhighlightall()

    def on_hapSQLeditor_textChanged(self):
        """Slot executed when ``hapSQLeditor`` text changed.

        If the editor is empty the ``executeHapSQL`` is disabled.

        Save status is setted  to ``False``.

        """
        text = self.hapSQLeditor.text().strip()
        self.executeHapSQLButton.setEnabled(bool(text))
        self._set_save_status(False)

    @QtCore.pyqtSlot()
    def on_executeHapSQLButton_clicked(self):
        """Slot executed when ``hapSQLButton`` is clicked.

        Executes the sql query over all haplotypes of the connection and
        highligth the result in the network.

        """
        try:
            query = self.hapSQLeditor.text().strip()
            if not query.lower().startswith("select"):
                msg = "The query must be start with the 'select' command"
                raise ValueError(msg)
            haps = self.conn.hap_sql(query)
            edges = self.conn.edges_by_haplotypes(*haps)
            self.network.highlight_nodes(haps)
            self.stats_frame.refresh(edges)
        except Exception as err:
            error_dialog.critical(self.tr("Error on Haplotype SQL"), err)

    def on_weightRange_changed(self, start, end):
        """Slot executed when the doble slider range change.

        This execute a query ober the database and filter all edges to show.

        Save status is setted  to ``False``.

        """
        edges = tuple(self.conn.filter_edges(start, end))
        self.network.filter_edges(*edges)
        self._set_save_status(False)

    @QtCore.pyqtSlot()
    def on_addEnviromentPushButton_clicked(self):
        """Slot executed when ``addEnviromentPushButton`` is clicked.

        This method open a ``EnviromentDialog`` instance for configure the
        new filter and if its accepted add a new filter to the ambien table.

        Save status is setted  to ``False``.

        """
        self.envDialog = EnviromentDialog(self,
                                          self.conn.fact_attributes_names())
        if self.envDialog.exec_():
            atts = self.envDialog.selected_attributes()
            enviroment = dict((att, None) for att in atts)
            self._add_filter(False, enviroment)
            self._set_save_status(False)
        self.envDialog.setParent(None)
        self.envDialog.destroy()
        del self.envDialog

    def on_filter_removeRequested(self, widget):
        """Slot executed when *remove* button of a filter is clicked.

        This method remove a parent row of the widget.

        Save status is setted  to ``False``.

        **Params**
            :widget: The widget to be removed from the enviroment table.

        """
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            if self.enviromentsTableWidget.cellWidget(ridx, 0) == widget:
                if widget.is_active():
                    widget.set_active(False)
                    self.on_filter_changed()
                self.enviromentsTableWidget.removeRow(ridx)
                widget.removeRequested.disconnect(self.on_filter_removeRequested)
                widget.filterChanged.disconnect(self.on_filter_changed)
                self._set_save_status(False)
                break

    def on_filter_changed(self):
        """Slot executed when a combo box of a filter or a checkbox status
        change.

        This method iterates over all enviroments and highlight all match nodes.

        Save status is setted  to ``False``.

        """
        haps = ()
        for ridx in range(self.enviromentsTableWidget.rowCount()):
            envwidget = self.enviromentsTableWidget.cellWidget(ridx, 0)
            if envwidget.is_active():
                haps = self.conn.enviroment(**envwidget.filters())
                break
        edges = self.conn.edges_by_haplotypes(*haps)
        self.network.highlight_nodes(haps)
        self._set_save_status(False)

    @QtCore.pyqtSlot(int)
    def on_hapsComboBox_currentIndexChanged(self, idx):
        """Slot executed when a ``hapsComboBox`` index change.

        The method charge ``attTableWidget`` with the selected haplotype.

        **Params**
            :idx: The new index of the ``hapsComboBox``.

        """
        hap_id = self.hapsComboBox.itemData(idx)
        hap = self.conn.haplotype_by_id(hap_id)
        atts = hap.items_attrs()
        atts.sort()
        self.network.select_node(hap)
        self.attTableWidget.clearContents()
        self.attTableWidget.setRowCount(len(atts))
        for idx, atts in enumerate(atts):
            nameitem = QtGui.QTableWidgetItem(atts[0])
            valueitem = QtGui.QTableWidgetItem(unicode(atts[1]))
            self.attTableWidget.setItem(idx, 0, nameitem)
            self.attTableWidget.setItem(idx, 1, valueitem)

    def on_node_clicked(self, hap_id):
        """Slot executed when a *node* is clicked in the network.

        This method select the index of the haplotype in ``hapsComboBox`` and
        execute the ``on_hapsComboBox_currentIndexChanged`` slot.

        **Params**
            :hap_id: an haplotype id

        """
        self._set_save_status(False)
        for idx in range(self.hapsComboBox.count()):
            idx_hap_id = self.hapsComboBox.itemData(idx)
            if hap_id == idx_hap_id:
                self.hapsComboBox.setCurrentIndex(idx)

    #===========================================================================
    # PUBLIC
    #===========================================================================

    def remove_all_filters(self):
        """Removes all filters from enviroment table.

        """
        while self.enviromentsTableWidget.rowCount():
            widget = self.enviromentsTableWidget.cellWidget(0, 0)
            if widget.is_active():
                widget.set_active(False)
            widget.removeRequested.disconnect(self.on_filter_removeRequested)
            widget.filterChanged.disconnect(self.on_filter_changed)
            self.enviromentsTableWidget.removeRow(0)
        self._set_save_status(False)

    def load_version(self, version):
        """Load a version ``dict``.

        **Params**
            :version: A ``dict`` to setup all the gui of the explorer.

        """
        try:
            self.network.clear()
            vdata = version["data"]
            if not vdata["hap_sql"]:
                vdata["hap_sql"] = "SELECT * FROM `haplotypes`"
            if not vdata["topology"]:
                for hap in self.conn.iter_haplotypes():
                    vdata["topology"][hap.hap_id] = self.network.get_unused_coord()
            for hap_id, xy in sorted(vdata["topology"].items()):
                hap = self.conn.haplotype_by_id(hap_id)
                self.network.add_node(hap, x=xy[0], y=xy[1])
                self.hapsComboBox.addItem(unicode(hap.hap_id), hap_id)

            self.remove_all_filters()
            for checked, enviroment in vdata["enviroments"]:
                self._add_filter(checked, enviroment)

            for edge in self.conn.iter_edges():
                self.network.add_edge(edge)

            if None in vdata["weight_range"]:
                vdata["weight_range"] = self.rs.tops()
            self.rs.setStart(vdata["weight_range"][0])
            self.rs.setEnd(vdata["weight_range"][1])

            self.hapSQLeditor.setText(vdata["hap_sql"])

            self.on_filterTabWidget_currentChanged(self.filterTabWidget.currentIndex())
            self.on_weightsCheckBox_stateChanged(
                self.weightsCheckBox.isChecked())
            self.on_haplotypesNamesCheckBox_stateChanged(
                self.haplotypesNamesCheckBox.isChecked()
            )
            self.on_hapsComboBox_currentIndexChanged(
                self.hapsComboBox.currentIndex()
            )
            self._version = (version["id"],
                             version["datetime"], version["tag"])
        except Exception as err:
            error_dialog.critical(self.tr("Load Error"), err)
        else:
            self._set_save_status(True)

    def is_saved(self):
        """Return a ``bool`` representing if the exploraton status of the
        explorer change from the last save.

        """
        return self._is_saved

    def save_version(self, new_version, comment):
        """Save the current status of the exploration to the database.

        Save status is setted  to ``True``.

        **Params**
            :new_version: The new name of the version (like *0.1* or *1.5.2b*).
            :comment: A coment about the new version.

        """
        try:
            topology = self.network.topology()
            weight_range = self.rs.getRange()
            sql = self.hapSQLeditor.text().strip()
            enviroments = []
            for ridx in range(self.enviromentsTableWidget.rowCount()):
                envwidget = self.enviromentsTableWidget.cellWidget(ridx, 0)
                enviroments.append((envwidget.is_active(), envwidget.filters()))
            self.conn.save_version(new_version, comment, sql, topology,
                                   weight_range, enviroments)
        except Exception as err:
            error_dialog.critical(self.tr("Save Error"), err)
        else:
            self._set_save_status(True)

    def destroy(self):
        """Destroy the explorer widget"""
        self.network.clear()
        self.network.setParent(None)
        self.networkLayout.removeWidget(self.network)
        self.ipythonWidget.clear()
        self.ipythonWidget.setParent(None)
        self.consoleLayout.removeWidget(self.ipythonWidget)
        super(ExplorerFrame, self).destroy()

    def version(self):
        """Return the actual version of the exploration

        **Return**
            A ``dict`` with info about the version.

        """
        return self._version


#===============================================================================
# EVIROMENT DIALOG
#===============================================================================

class EnviromentDialog(uis.UI("EnviromentDialog.ui")):
    """This dialog is used for select ``yatel.dom.Fact`` atributes for creante
    new enviroments"""

    def __init__(self, parent, facts_names):
        """Creates a new instance of the ``EnviromentDialog``

        **Params**
            :parent: The parent widget.
            :facts_names: A list of all posible facts values.

        """
        super(EnviromentDialog, self).__init__(parent=parent)
        self.factAttributesListWidget.addItems(list(facts_names))
        self.factAttributesListWidget.sortItems()

    def on_factAttributesListWidget_currentItemChanged(self, entered, exited):
        """Slot executed when ``factAttributesListWidget`` item change.

        This method validates if a new item is selected the ``addButton`` is
        activated otherwise is deactivated.

        **Param**
            :entered: The new curren item (can be ``None``).
            :exited: The previous selected item (not used).

        """
        self.addButton.setEnabled(bool(entered))

    def on_selectedAttributesListWidget_currentItemChanged(self,
                                                           entered, exited):
        """Slot executed when ``selectedAttributesListWidget`` item change.

        This method validates if a new item is selected the ``removeButton`` is
        activated otherwise is deactivated.

        **Param**
            :entered: The new curren item (can be ``None``).
            :exited: The previous selected item (not used).

        """
        self.removeButton.setEnabled(bool(entered))

    @QtCore.pyqtSlot()
    def on_addButton_clicked(self):
        """Slot executed when ``addButton`` is clicked.

        This method peek the selected attribut to the
        ``factAttributesListWidget`` and put it on
        ``selectedAttributesListWidget``.

        """
        idx = self.factAttributesListWidget.currentIndex().row()
        item = self.factAttributesListWidget.takeItem(idx)
        if item:
            self.selectedAttributesListWidget.addItem(item)
            self.selectedAttributesListWidget.sortItems()
            self.factAttributesListWidget.sortItems()

    @QtCore.pyqtSlot()
    def on_removeButton_clicked(self):
        """Slot executed when ``removeButton`` is clicked.

        This method peek the selected attribut to the
        ``selectedAttributesListWidget`` and put it on
        ``factAttributesListWidget``.

        """
        idx = self.selectedAttributesListWidget.currentIndex().row()
        item = self.selectedAttributesListWidget.takeItem(idx)
        if item:
            self.factAttributesListWidget.addItem(item)
            self.selectedAttributesListWidget.sortItems()
            self.factAttributesListWidget.sortItems()

    def selected_attributes(self):
        """Return a ``tuple`` with a list of all selected attributes.

        """
        atts = []
        for idx in range(self.selectedAttributesListWidget.count()):
            text = self.selectedAttributesListWidget.item(idx).text()
            atts.append(text)
        return tuple(atts)


#===============================================================================
# ENVIROMENT LIST ITEM
#===============================================================================

class EnviromentListItem(uis.UI("EnviromentListItem.ui")):

    # : Signal emited when the filter change his status
    filterChanged = QtCore.pyqtSignal()

    # : Signal emited when the filter request his removal
    removeRequested = QtCore.pyqtSignal('QWidget')

    def __init__(self, env):
        """Creates a new instance of the ``EnviromentListItem``

        **Params**
            :env: a dictionary with keys as combo names and value is a list with
                  all posible values

        """
        super(EnviromentListItem, self).__init__()
        self._filters = {}
        for k, values in sorted(env.items()):
            label = QtGui.QLabel(k)
            self.envLayout.addWidget(label)
            combo = QtGui.QComboBox()
            combo.addItem("", None)
            for v in values:
                combo.addItem(unicode(v), v)
            self.envLayout.addWidget(combo)
            combo.currentIndexChanged.connect(self.on_combo_currentIndexChanged)
            self._filters[k] = combo
        self.setVisible(True)

    def on_checkBox_clicked(self):
        """Slot executed when ``checkBox`` status change.

        This method emit the signal ``filterChanged``.

        """
        self.filterChanged.emit()

    def on_combo_currentIndexChanged(self, idx):
        """Slot executed when ``combo`` index change.

        This method emit the signal ``filterChanged`` only if the filter is
        active.

        **Param**
            :idx: The new index of the combo.

        """
        if self.checkBox.isChecked():
            self.filterChanged.emit()

    @QtCore.pyqtSlot()
    def on_removeButton_clicked(self):
        """Slot executed when ``removeButton`` is clicked.

        This method emit the signal ``removeRequested`` sending the instance as
        param.

        """
        self.removeRequested.emit(self)

    def is_active(self):
        """Returns if the filter is active or not"""
        return self.checkBox.isChecked()

    def set_active(self, status):
        """Activates or deactivate this filter

        **Params**
            :status: ``bolean``
        """
        if self.checkBox.isChecked() != status:
            self.filterChanged.emit()
        self.checkBox.setChecked(status)

    def select_attribute_value(self, name, value):
        """Change the value of a given combo by name (if the value not exists
        nothing happend).

        """
        combo = self._filters[name]
        for idx in range(combo.count()):
            avalue = combo.itemData(idx)
            if value == avalue:
                combo.setCurrentIndex(idx)
                break

    def filters(self):
        """Returns all the data of the wisget as a ``dict`` where the key
        is the fat attribute name and the value is the selected value of the
        combo.

        """
        f = {}
        for label_text, combo in self._filters.items():
            idx = combo.currentIndex()
            value = combo.itemData(idx)
            f[label_text] = value
        return f


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

