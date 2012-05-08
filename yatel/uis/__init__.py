
from __future__ import absolute_import

import os
import csv
import cStringIO

from PyQt4 import QtGui, QtCore

import csvcool

import pycante

import yatel
from yatel import constants
from yatel import resources
from yatel import csv2dom


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

UI = pycante.EDir(PATH)


#===============================================================================
# 
#===============================================================================

class ChargeFrame(UI("ChargeFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    
    CONTENT_HAPLOTYPES = "haplotypes"
    CONTENT_FACTS = "facts"
    CONTENT_EDGES = "edges"
    
    CONTENT_IDS = {
        CONTENT_HAPLOTYPES: "ID",
        CONTENT_FACTS: "Hap ID",
        CONTENT_EDGES: "Weight",
    }
    
    def __init__(self, parent, file_content, csv_path):
        assert file_content in ChargeFrame.CONTENT_IDS
        
        super(ChargeFrame, self).__init__(parent)
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
        self.delimiterLineEdit.setText(csv2dom.EXCEL_DIALECT.delimiter or ",")
        self.escapeCharLineEdit.setText(csv2dom.EXCEL_DIALECT.escapechar or "")
        self.doubleQuoteCheckBox.setChecked(csv2dom.EXCEL_DIALECT.doublequote)
        self.skipInitialSpaceCheckBox.setChecked(
            csv2dom.EXCEL_DIALECT.skipinitialspace
        )
        
        self.encodingComboBox.activated.connect(self.on_csvconf_changed)
        self.delimiterLineEdit.textEdited.connect(self.on_csvconf_changed)
        self.escapeCharLineEdit.textEdited.connect(self.on_csvconf_changed)
        self.doubleQuoteCheckBox.stateChanged.connect(self.on_csvconf_changed)
        self.skipInitialSpaceCheckBox.stateChanged.connect(
            self.on_csvconf_changed
        )
        
        # Set the name of the id's of the csv
        iow = ChargeFrame.CONTENT_IDS[self.file_content]
        self.tableTypes.horizontalHeaderItem(1).setText(self.tr(iow))
        
        # refresh all content
        self.on_csvconf_changed()
    
    # SLOTS
    def on_csvconf_changed(self, *args, **kwargs):
        # reload csv conf
        encoding = unicode(self.encodingComboBox.currentText())
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
                or self.file_content != ChargeFrame.CONTENT_HAPLOTYPES
        ]
        selected_id = self.id_column
        if selected_id == None and len(id_candidates):
            selected_id = id_candidates[0]
        all_types = self.cool.discover_types()
        self.tableTypes.setRowCount(len(all_types))
        self.tableTypes.setVerticalHeaderLabels(self.cool.columnnames)
        types = [(t.__name__, QtCore.QVariant(t)) for t in csvcool.types()]
        for cidx, cname in enumerate(self.cool.columnnames):
            column_type = all_types[cname]
            type_idx = csvcool.types().index(column_type)
            
            radiobutton = QtGui.QRadioButton(self)            
            combo = QtGui.QComboBox(self)
            for t in types:
                combo.addItem(*t)
            combo.setCurrentIndex(type_idx)
            
            self.tableTypes.setCellWidget(cidx, 0, combo)
            self.tableTypes.setCellWidget(cidx, 1, radiobutton)
            
            if cname not in id_candidates:
                radiobutton.setEnabled(False)
            elif cname == selected_id:
                radiobutton.setChecked(True)
            
        self.tableTypes.resizeColumnsToContents()
    
    @property
    def types(self):
        tps = {}
        for ridx in range(self.tableTypes.rowCount()):
            header = unicode(self.tableTypes.verticalHeaderItem(ridx).text())
            combo = self.tableTypes.cellWidget(ridx, 0)
            tps[header] = combo.itemData(combo.currentIndex()).toPyObject()
        return tps
    
    @property
    def id_column(self):
        for ridx in range(self.tableTypes.rowCount()):
            radiobutton = self.tableTypes.cellWidget(ridx, 1)
            if radiobutton.isChecked():
                return unicode(
                    self.tableTypes.verticalHeaderItem(ridx).text()
                )


#===============================================================================
# 
#===============================================================================

class ChargeWizard(UI("ChargeWizard.ui")):
    """Wizard for charge csv file as networks
    
    """
    
    # SLOTS
    def on_openFileButtonWeights_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.tr("Open Edges File"),
            constants.HOME_PATH,
            self.tr("CSV (*.csv)")
        )
        if filename:
            self.on_closeFileButtonWeights_pressed()
            self.fileLabelWeights.setText(filename)
            self.weightFrame = ChargeFrame(
                self.weightsPage, ChargeFrame.CONTENT_EDGES, filename
            )
            self.weightsLayout.addWidget(self.weightFrame)
            self.closeFileButtonWeights.setEnabled(True)
    
    def on_closeFileButtonWeights_pressed(self):
        if hasattr(self, "weightFrame"):
            self.weightsLayout.removeWidget(self.weightFrame)
            self.weightFrame.destroy()
            self.updateGeometry()
        self.fileLabelWeights.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonWeights.setEnabled(False)
    
    def on_openFileButtonFacts_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.tr("Open Facts File"),
            constants.HOME_PATH,
            self.tr("CSV (*.csv)")
        )
        if filename:
            self.on_closeFileButtonFacts_pressed()
            self.fileLabelFacts.setText(filename)
            self.factsFrame = ChargeFrame(
                self.factsPage, ChargeFrame.CONTENT_FACTS, filename
            )
            self.factsLayout.addWidget(self.factsFrame)
            self.closeFileButtonFacts.setEnabled(True)
    
    def on_closeFileButtonFacts_pressed(self):
        if hasattr(self, "factsFrame"):
            self.factsLayout.removeWidget(self.factsFrame)
            self.factsFrame.destroy()
            self.updateGeometry()
        self.fileLabelFacts.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonFacts.setEnabled(False)
    
    def on_openFileButtonHaps_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
            self, self.tr("Open Haplotypes File"),
            constants.HOME_PATH,
            self.tr("CSV (*.csv)")
        )
        if filename:
            self.on_closeFileButtonHaps_pressed()
            self.fileLabelHaps.setText(filename)
            self.haplotypesFrame = ChargeFrame(
                self.hapsPage, ChargeFrame.CONTENT_HAPLOTYPES, filename
            )
            self.hapsLayout.addWidget(self.haplotypesFrame)
            self.closeFileButtonHaps.setEnabled(True)
            #self.haplotypesFrame.idSelectedStateChanged.connect()
        
    def on_closeFileButtonHaps_pressed(self):
        if hasattr(self, "haplotypesFrame"):
            self.hapsLayout.removeWidget(self.haplotypesFrame)
            self.haplotypesFrame.destroy()
            self.updateGeometry()
        self.fileLabelHaps.setText(self.tr("<NO-FILE>"))
        self.closeFileButtonHaps.setEnabled(False)
    
            
#===============================================================================
# MAIN WINDOW
#===============================================================================

class MainWindow(UI("MainWindow.ui")):
    """The main window class"""
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QtGui.QIcon(resources.get("logo.svg")))
    
    def setWindowTitle(self, prj=""):
        title = "{0} v.{1} - {2}".format(yatel.__prj__, yatel.__version__, prj)
        super(self.__class__, self).setWindowTitle(title)
    
    # SLOTS
    def on_actionWizard_triggered(self, *chk):
        if chk:
            self.wizard = ChargeWizard(self)
            self.wizard.exec_()
            
            facts = None
            if hasattr(self.wizard, "factsFrame"):
                factsFrame = self.wizard.factsFrame
                cool = factsFrame.cool.type_corrector(factsFrame.types)
                facts = csv2dom.construct_facts(cool, factsFrame.id_column)
            
            haplotypes = None
            if hasattr(self.wizard, "haplotypesFrame"):
                haplotypesFrame = self.wizard.haplotypesFrame
                cool = haplotypesFrame.cool.type_corrector(
                    haplotypesFrame.types
                )
                haplotypes = csv2dom.construct_haplotypes(
                    cool, haplotypesFrame.id_column
                )
            
            edges = None
            if hasattr(self.wizard, "weightsFrame"):
                weightsFrame = self.wizard.weightsFrame
                cool = weightsFrame.cool.type_corrector(weightsFrame.types)
                edges = csv2dom.construct_edges(cool, weightsFrame.id_column)


class SplashScreen(QtGui.QSplashScreen):
    
    def __init__(self):
        pixmap = QtGui.QPixmap(resources.get("splash.png"))
        super(self.__class__, self).__init__(pixmap)




#===============================================================================
# MAIN
#===============================================================================
if __name__ == "__main__":
    print(__doc__)

