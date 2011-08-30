import uis
import csvcool

from yatel import csv_parser

cool = csvcool.read(open("tablaEFclusters Oct05.csv"))

ventanita = uis.ChargeFactOrHaplotype(cool, csv_parser.discover_types(cool))
ventanita.show()
uis.run()
