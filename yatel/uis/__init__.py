
from __future__ import absolute_import

import os

from PyQt4 import QtGui, QtCore

import csvcool

from pycante import EDir, run

import yatel
from yatel import csv_parser
from yatel import csv_parser as sniffer



#===============================================================================
# CONSTANTS
#===============================================================================

try:
    # ...works on at least windows and linux.
    # In windows it points to the user"s folder
    #  (the one directly under Documents and Settings, not My Documents)

    # In windows, you can choose to care about local versus roaming profiles.
    # You can fetch the current user"s through PyWin32.
    #
    # For example, to ask for the roaming "Application Data" directory:
    # CSIDL_APPDATA asks for the roaming, CSIDL_LOCAL_APPDATA for the local one
    from win32com.shell import shellcon, shell
    HOME_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
except ImportError:
   # quick semi-nasty fallback for non-windows/win32com case
    HOME_PATH = os.path.expanduser("~")


PATH = os.path.abspath(os.path.dirname(__file__))

UI = EDir(PATH)

#===============================================================================
# 
#===============================================================================

class ChargeFrame(UI("ChargeFrame.ui")):
    """This is the frame to show for select types of given csv file
    
    """
    def __init__(self, parent, file_content, csv_path):
        super(ChargeFrame, self).__init__(parent)
        self.file_content = file_content
        self.path = csv_path
        with open(csv_path) as f: 
            self.cool = csvcool.read(f)
        self.types = csv_parser.discover_types(self.cool)
        self.set_table_cool()
        self.set_table_types()
        self.set_id_of_what()
    
    def set_id_of_what(self):
        iow = None
        msg = "Please Select '{0}' Column"
        if self.file_content in ("haplotypes", "facts"):
            iow = "Hap ID"
        elif self.file_content in ("distances",):
            iow = "Weight"
        self.tableTypes.horizontalHeaderItem(1).setText(self.tr(iow))
        self.selectHapIdLabel.setText(self.tr(msg.format(iow)))
    
    def set_table_cool(self):
        self.tableCool.setColumnCount(len(self.cool.columnnames))
        self.tableCool.setRowCount(len(self.cool))
        self.tableCool.setHorizontalHeaderLabels(self.cool.columnnames)
        for cidx, cname in enumerate(self.cool.columnnames):
            for ridx, row in enumerate(self.cool):
                value = row[cname]
                newitem = QtGui.QTableWidgetItem(value)
                self.tableCool.setItem(ridx, cidx, newitem)
        self.tableCool.resizeColumnsToContents()
                
    def set_table_types(self):
        self.tableTypes.setRowCount(len(self.types))
        self.tableTypes.setVerticalHeaderLabels(self.cool.columnnames)
        types = [(t.__name__, QtCore.QVariant(t)) for t in sniffer.types()]
        for cidx, cname in enumerate(self.cool.columnnames):
            column_type = self.types[cname]
            type_idx = sniffer.types().index(column_type)
            
            radiobutton = QtGui.QRadioButton(self)            
            combo = QtGui.QComboBox(self)
            for type in types:
                combo.addItem(*type)
            combo.setCurrentIndex(type_idx)
            
            self.tableTypes.setCellWidget(cidx, 0, combo)
            self.tableTypes.setCellWidget(cidx, 1, radiobutton)
            
            radiobutton.toggled.connect(self.on_radiobutton_toggled)
        self.tableTypes.resizeColumnsToContents()
    
    # SIGNALS
    def on_tableCool_currentCellChanged(self, ridx, cidx, ordix, ocidx):
        color_high = QtGui.QColor(QtCore.Qt.yellow)
        color_normal = QtGui.QColor(QtCore.Qt.blue)
        for row in range(0, self.tableTypes.rowCount()):
            color = color_high if row == cidx else  color_normal
            for col in range(0, self.tableTypes.columnCount()):
                pass
                #print self.tableTypes.item(1, 1)
        """.setBackgroundColor(color)
        self.tableTypes.item(0, 0).setData(QtCore.Qt.BackgroundRole, QtGui.QColor(QtCore.Qt.blue))"""
    
    def on_radiobutton_toggled(self, boolean):
        self.selectHapIdLabel.setVisible(False)
    
    @property
    def results(self):
        types = {}
        column_hap_id = None
        for ridx in range(self.tableTypes.rowCount()):
            header = self.tableTypes.takeVerticalHeaderItem(ridx).text()
            combo = self.tableTypes.cellWidget(ridx, 0)
            radiobutton = self.tableTypes.cellWidget(ridx, 1)
            types[header] = combo.itemData(combo.currentIndex()).toPyObject()
            if radiobutton.isChecked():
                column_hap_id = header
        return {
            "file_content": self.file_content,
            "path": self.path,
            "cool": self.cool,
            "types": types,
            "id_column": column_hap_id,
        }


#===============================================================================
# 
#===============================================================================

class ChargeWizard(UI("ChargeWizard.ui")):
    """Wizard for charge csv file as networks
    
    """
    def on_openFileButtonDistances_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                       self, self.tr("Open Distances File"),
                       HOME_PATH,
                       self.tr("CSV (*.csv)")
                   )
        if filename:
            if hasattr(self, "distancesFrame"):
                self.distancesLayout.removeWidget(self.distancesFrame)
            self.fileLabelDistances.setText(filename)
            self.distancesFrame = ChargeFrame(self.distancesPage, "distances", filename)
            self.distancesLayout.addWidget(self.distancesFrame)
    
    def on_openFileButtonFacts_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                       self, self.tr("Open Facts File"),
                       HOME_PATH,
                       self.tr("CSV (*.csv)")
                   )
        if filename:
            if hasattr(self, "factsFrame"):
                self.factsLayout.removeWidget(self.factsFrame)
            self.fileLabelFacts.setText(filename)
            self.factsFrame = ChargeFrame(self.factsPage, "facts", filename)
            self.factsLayout.addWidget(self.factsFrame)
    
    def on_openFileButtonHaps_pressed(self):
        filename = QtGui.QFileDialog.getOpenFileName(
                       self, self.tr("Open Haplotypes File"),
                       HOME_PATH,
                       self.tr("CSV (*.csv)")
                   )
        if filename:
            if hasattr(self, "haplotypesFrame"):
                self.hapsLayout.removeWidget(self.haplotypesFrame)
            self.fileLabelHaps.setText(filename)
            self.haplotypesFrame = ChargeFrame(self.hapsPage, "haplotypes", filename)
            self.hapsLayout.addWidget(self.haplotypesFrame)
        
    
            
#===============================================================================
# MAIN WINDOW
#===============================================================================

class MainWindow(UI("MainWindow.ui")):
    """The main window class"""
        
    def setWindowTitle(self, prj=""):
        title = "{0} v.{1} - {2}".format(yatel.__prj__, yatel.__version__, prj)
        super(self.__class__, self).setWindowTitle(title)
    
    def on_actionWizard_triggered(self, *chk):
        if chk:
            self.wizard = ChargeWizard(self)
            self.wizard.exec_()
            facts = None
            if hasattr(self.wizard, "factsFrame"):
                facts = self.wizard.factsFrame.results
            haplotypes = None
            if hasattr(self.wizard, "haplotypesFrame"):
                haplotypes = self.wizard.haplotypesFrame.results
            distances = None
            if hasattr(self.wizard, "distancesFrame"):
                distances = self.wizard.distancesFrame.results
            print facts, distances, haplotypes 
        

#===============================================================================
# MAIN
#===============================================================================
if __name__ == "__main__":
    print(__doc__)

