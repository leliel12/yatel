
import os

from PyQt4 import QtGui

from pycante import E, run

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
    
    def __init__(self, cool, types):
        super(ChargeFactOrHaplotype, self).__init__()
        self.cool = cool
        self.types = types
        
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
        for cidx, cname in enumerate(self.cool.columnnames):
            #newitem = QtGui.QTableWidgetItem(self.types[cname].__name__)
            newitem = QtGui.QComboBox()
            newitem.addItems(sniffer.types())
            self.tableTypes.setCellWidget(cidx, 0, newitem)
        
                
                
    def on_buttonBox_accepted(self):
        # buttonBox exist inside "window.ui"
        print "hola"


#===============================================================================
# MAIN
#===============================================================================
if __name__ == "__main__":
    print(__doc__)

