#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from yatel import dom, db

reload(db)

DB = "cosito.db"

try:
    os.remove(DB)
except:
    pass

nw = db.YatelNetwork("sqlite", database=DB, mode="w")
nw.add_element(dom.Haplotype(1))
nw.confirm_changes()
del nw

nw = db.YatelNetwork("sqlite", database=DB, mode="a", log=0)
nw.add_element(dom.Haplotype(2, a=1))
nw.add_element(dom.Fact(2, k=1, e="hola"))
nw.confirm_changes()

nw = db.YatelNetwork("sqlite", database=DB, mode="a", log=True)
nw.add_element(dom.Haplotype(3, c=1))
nw.add_element(dom.Edge(23, 2, 3))
nw.add_element(dom.Edge(25, 2, 3, 1))
nw.confirm_changes()
