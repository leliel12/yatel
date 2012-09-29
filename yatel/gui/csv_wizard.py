#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice 
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""This module contains a gui of a wizard for create a new database from
diferents csv files.

"""


#===============================================================================
# IMPORTS
#===============================================================================

import cStringIO

from PyQt4 import QtGui, QtCore

import csvcool

from yatel import constants
from yatel.conversors import csvcool2yatel

from yatel.gui import uis


#===============================================================================
# 
#===============================================================================

class CSVChargeFrame(uis.UI("CSVChargeFrame.ui")):
    """This is the frame to show for select types of given csv file.
    
    """
    
    #: Constant for open create a wizard page for creation of haplotypes.
    CONTENT_HAPLOTYPES = "haplotypes"
    
    #: Constant for open create a wizard page for creation of facts.
    CONTENT_FACTS = "facts"
    
    #: Constant for open create a wizard page for creation of edges.
    CONTENT_EDGES = "edges"
    
    #: Constant for identify a id of diferete a diferent types of objects.
    CONTENT_IDS = {
        CONTENT_HAPLOTYPES: "ID",
        CONTENT_FACTS: "Hap ID",
        CONTENT_EDGES: "Weight",
    }
    
    def __init__(self, parent, file_content, csv_path):
        """Create a new instance of CSVChargeFrame
        
        **Params**
            :parent: A gui parent of this widget.
            :action: A frame mode. 
                     [CSVChargeFrame.CONTENT_FACTS|
                      CSVChargeFrame.CONTENT_FACTS
                      CSVChargeFrame.CONTENT_EDGES]
            :csv_path: The path of the csv file to be open.
            
        
        """
        assert file_content in CSVChargeFrame.CONTENT_IDS
        
        super(CSVChargeFrame, self).__init__(parent)
        self.file_content = file_content
        self.path = csv_path
        with open(csv_path) as f: 
            self.cool_code = cStringIO.StringIO(f.read())
            
        # setup the conf widgets
        self.encodingComboBox.addItems(constants.ENCODINGS)
        try: 
            idx = constants.ENCODINGS.index(constants.DEFAULT_FILE_ENCODING)
            self.encodingComboBox.setCurrentIndex(idx)
        except ValueError:
            pass
        self.delimiterLineEdit.setText(
            csvcool2yatel.EXCEL_DIALECT.delimiter or ","
        )
        self.escapeCharLineEdit.setText(
            csvcool2yatel.EXCEL_DIALECT.escapechar or ""
        )
        self.doubleQuoteCheckBox.setChecked(
            csvcool2yatel.EXCEL_DIALECT.doublequote
        )
        self.skipInitialSpaceCheckBox.setChecked(
            csvcool2yatel.EXCEL_DIALECT.skipinitialspace
        )
        
        self.encodingComboBox.activated.connect(self.on_csvconf_changed)
        self.delimiterLineEdit.textEdited.connect(self.on_csvconf_changed)
        self.escapeCharLineEdit.textEdited.connect(self.on_csvconf_changed)
        self.doubleQuoteCheckBox.stateChanged.connect(self.on_csvconf_changed)
        self.skipInitialSpaceCheckBox.stateChanged.connect(
            self.on_csvconf_changed
        )
        
        # Set the name of the id's of the csv
        iow = CSVChargeFrame.CONTENT_IDS[self.file_content]
        self.tableTypes.horizontalHeaderItem(1).setText(self.tr(iow))
        
        # refresh all content
        self.on_csvconf_changed()
    
    # SLOTS
    def on_csvconf_changed(self):
        """Slot executed when a any configuration is changed on anythis frame.
        
        """
        # reload csv conf
        encoding = self.encodingComboBox.currentText()
        delimiter = str(self.delimiterLineEdit.text()).strip()
        escapechar = str(self.escapeCharLineEdit.text()) or None
        doublequote = bool(self.doubleQuoteCheckBox.checkState())
        skipinitialspace = bool(self.skipInitialSpaceCheckBox.checkState())
        
        # recharge cool instance
        try:
            self.cool_code.seek(0)
            self.cool = csvcool.read(
                self.cool_code, encoding=encoding, delimiter=delimiter,
                escapechar=escapechar, doublequote=doublequote,
                skipinitialspace=skipinitialspace
            )
        except Exception as ex:
            print str(ex)
            self.cool = csvcool.CSVCool(keys=[], rows=[])
        
        # setup table of csv
        self.tableCool.setColumnCount(len(self.cool.columnnames))
        self.tableCool.setRowCount(len(self.cool))
        self.tableCool.setHorizontalHeaderLabels(self.cool.columnnames)
        for cidx, cname in enumerate(self.cool.columnnames):
            for ridx, row in enumerate(self.cool):
                value = row[cname]
                newitem = QtGui.QTableWidgetItem(value)
                self.tableCool.setItem(ridx, cidx, newitem)
        self.tableCool.resizeColumnsToContents()
        
        # setup the table of types
        id_candidates = [
            cname for cname in self.cool.columnnames 
            if len(self.cool.column(cname)) == len(set(self.cool.column(cname)))
                or self.file_content != CSVChargeFrame.CONTENT_HAPLOTYPES
        ]
        selected_id = self.id_column()
        if selected_id == None and len(id_candidates):
            selected_id = id_candidates[0]
        all_types = self.cool.discover_types()
        self.tableTypes.setRowCount(len(all_types))
        self.tableTypes.setVerticalHeaderLabels(self.cool.columnnames)
        types = [(t.__name__, t) for t in csvcool.types()]
        for cidx, cname in enumerate(self.cool.columnnames):
            column_type = all_types[cname]
            type_idx = csvcool.types().index(column_type)
            
            radiobutton = QtGui.QRadioButton(self)            
            combo = QtGui.QComboBox(self)
            for idx, t in enumerate(types):
                combo.addItem(*t)
                if idx == type_idx:
                    break
                    
            combo.setCurrentIndex(type_idx)
            
            self.tableTypes.setCellWidget(cidx, 0, combo)
            self.tableTypes.setCellWidget(cidx, 1, radiobutton)
            
            if cname not in id_candidates:
                radiobutton.setEnabled(False)
            elif cname == selected_id:
                radiobutton.setChecked(True)
            
        self.tableTypes.resizeColumnsToContents()
    
    def types(self):
        """Return all types in selected for all columns as a dict.
        
        **Returns**
            A dict with column names as *keys*, and selected types as *values*.
            
        """
        tps = {}
        for ridx in range(self.tableTypes.rowCount()):
            header = self.tableTypes.verticalHeaderItem(ridx).text()
            combo = self.tableTypes.cellWidget(ridx, 0)
            tps[header] = combo.itemData(combo.currentIndex())
        return tps
    
    def id_column(self):
        """Return a str with the name of the column selected as unique id of
        all registers.
        
        """
        for ridx in range(self.tableTypes.rowCount()):
            radiobutton = self.tableTypes.cellWidget(ridx, 1)
            if radiobutton.isChecked():
                return self.tableTypes.verticalHeaderItem(ridx).text()
                
    def dom_objects(self):
        """Returns a ``yatel.dom`` objects acording of frame content type.
        
        """
        cool = self.cool.type_corrector(self.types())
        if self.file_content == self.CONTENT_HAPLOTYPES:
            return csvcool2yatel.construct_haplotypes(cool, self.id_column())
        elif self.file_content == self.CONTENT_FACTS:
            return csvcool2yatel.construct_facts(cool, self.id_column())
        elif self.file_content == self.CONTENT_EDGES:
            return csvcool2yatel.construct_edges(cool, self.id_column())
            

#===============================================================================
# 
#===============================================================================

class CSVWizard(uis.UI("CSVWizard.ui")):
    """Wizard for charge csv file as ``yatel.dom`` objects.
    
    """
    
    @QtCore.pyqtSlot()
    def on_openFileButtonWeights_clicked(self):
        """Slot executed when openFileButtonWeights is clicked.
        
        """
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.tr("Open Edges File"),
            constants.HOME_PATH,
            self.tr("CSV (*.csv)")
        )
        if filename:
            self.on_closeFileButtonWeights_clicked()
            self.fileLabelWeights.setText(filename)
            self.weightFrame = CSVChargeFrame(
                self.weightsPage, CSVChargeFrame.CONTENT_EDGES, filename
            )
            self.weightsLayout.addWidget(self.weightFrame)
            self.closeFileButtonWeights.setEnabled(True)
    
    @QtCore.pyqtSlot()
    def on_closeFileButtonWeights_clicked(self):
        """Slot executed when closeFileButtonWeights is clicked.
        
        """
        if hasattr(self, "weightFrame"):
            self.weightsLayout.removeWidget(self.weightFrame)
            self.weightFrame.setParent(None)
            self.weightFrame.destroy()
            self.updateGeometry()
        self.fileLabelWeights.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonWeights.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def on_openFileButtonFacts_clicked(self):
        """Slot executed when openFileButtonFacts is clicked.
        
        """
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.tr("Open Facts File"),
            constants.HOME_PATH,
            self.tr("CSV (*.csv)")
        )
        if filename:
            self.on_closeFileButtonFacts_clicked()
            self.fileLabelFacts.setText(filename)
            self.factsFrame = CSVChargeFrame(
                self.factsPage, CSVChargeFrame.CONTENT_FACTS, filename
            )
            self.factsLayout.addWidget(self.factsFrame)
            self.closeFileButtonFacts.setEnabled(True)
    
    @QtCore.pyqtSlot()
    def on_closeFileButtonFacts_clicked(self):
        """Slot executed when closeFileButtonFacts is clicked.
        
        """
        if hasattr(self, "factsFrame"):
            self.factsLayout.removeWidget(self.factsFrame)
            self.factsFrame.setParent(None)
            self.factsFrame.destroy()
            self.updateGeometry()
        self.fileLabelFacts.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonFacts.setEnabled(False)
    
    @QtCore.pyqtSlot()
    def on_openFileButtonHaps_clicked(self):
        """Slot executed when openFileButtonHaps is clicked
        
        """
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.tr("Open Haplotypes File"),
            constants.HOME_PATH,
            self.tr("CSV (*.csv)")
        )
        if filename:
            self.on_closeFileButtonHaps_clicked()
            self.fileLabelHaps.setText(filename)
            self.haplotypesFrame = CSVChargeFrame(
                self.hapsPage, CSVChargeFrame.CONTENT_HAPLOTYPES, filename
            )
            self.hapsLayout.addWidget(self.haplotypesFrame)
            self.closeFileButtonHaps.setEnabled(True)
    
    @QtCore.pyqtSlot()
    def on_closeFileButtonHaps_clicked(self):
        """Slot executed when closeFileButtonHaps is clicked
        
        """
        if hasattr(self, "haplotypesFrame"):
            self.hapsLayout.removeWidget(self.haplotypesFrame)
            self.haplotypesFrame.setParent(None)
            self.haplotypesFrame.destroy()
            self.updateGeometry()
        self.fileLabelHaps.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonHaps.setEnabled(False)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

