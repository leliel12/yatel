
import os

from PyQt4 import QtGui, QtCore

import csvcool

from pycante import E, run

from yatel import csv_parser
from yatel import csv_parser as sniffer



#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

UI = lambda n: E(os.path.join(PATH, n))

#===============================================================================
# 
#===============================================================================

class ChargeFactOrHaplotype(UI("charge_haps_facts.ui")):
    
    def __init__(self, file_type, csv_path):
        super(ChargeFactOrHaplotype, self).__init__()
        self.setWindowTitle("Yatel - {0}: '{1}'".format(file_type, csv_path))
        
        self.path = csv_path
        with open(csv_path) as f: 
            self.cool = csvcool.read(f)
        self.types = csv_parser.discover_types(self.cool)
        
        self.set_table_cool()
        self.set_table_types()
    
    def set_table_cool(self):
        self.tableCool.setColumnCount(len(self.cool.columnnames))
        self.tableCool.setRowCount(len(self.cool))
        self.tableCool.setHorizontalHeaderLabels(self.cool.columnnames)
        for ridx, row in enumerate(self.cool):
            for cidx, cname in enumerate(self.cool.columnnames):
                value = row[cname]
                newitem = QtGui.QTableWidgetItem(value)
                self.tableCool.setItem(ridx, cidx, newitem)
                
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
        
                
    def on_buttonBox_accepted(self):
        for ridx in range(self.tableTypes.rowcount):
            cname = 0
        self.results = {
            "path": self.path,
            "cool": self.cool,
            "types": types,
            "column_hap_id": column_hap_id,
        }


#===============================================================================
# MAIN
#===============================================================================
if __name__ == "__main__":
    print(__doc__)

