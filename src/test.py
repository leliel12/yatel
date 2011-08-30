import uis
import csvcool

import ycsv

cool = csvcool.read(open("tablaEFclusters Oct05.csv"))

ventanita = uis.ChargeFactOrHaplotype(cool, ycsv.discover_types(cool))
ventanita.show()
uis.run()
